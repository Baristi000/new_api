import time, re, requests, json, serial, os
import mysql.connector
from core.config import settings
from provider import vinaphone, mobifone, viettel, vietnamobile, error_handler

providers = settings.providers

#port#
#open mysql connection
def connection():
    cnx = mysql.connector.connect(user='trieu', 
                                    password='T123',
                                    host='localhost',
                                    database='sim_card_management')
    return cnx
#execute query 
def get_info(q):
    cnx = connection()
    cursor = cnx.cursor()
    cursor.execute(q)
    if q.split()[0].upper()=="SELECT":
        r = cursor.fetchall();
        cnx.close()
        cursor.close()
        return(r)
    else:
        cnx.commit()
        cnx.close()
        cursor.close()
#check signal in realtime
def check_signal(port):
    r = 0
    while r == 0:
        r = port.inWaiting()
    time.sleep(2)
#write script into port
def port_write(port,script:str):
    port.write(script.encode())
    check_signal(port)
    res = port.readlines()
    return(res)

#trying to get response in tries time
def get_data(script,port,tries:int):
    while tries > 0 :
        res = port_write(port, script)
        #print all res
        """for r in res:
            print(r.decode("utf-8",errors = "ignore").strip("\n"))
        print("=========================")"""
        metadata = error_handler.is_error(res)
        if metadata["status"] == True:
            break
        tries = tries-1
        time.sleep(1)
    if tries == 0:
        return ({"status":False})
    else:
        res = error_handler.Cinterion(res,metadata["type"])
    return ({"status":True,
            "data":res})
#check provider
def check_provider(port):
    while True:
        str = 'AT+CIMI\r'
        res = port_write(port, str)
        if res != []:
            break
    res = res[1].decode("utf-8", errors="ignore")[0:5]
    if providers[res] == "vinaphone":
        print("vinaphone")
        return(vinaphone)
    elif providers[res] == "mobifone":
        print("mobifone")
        return(mobifone)
    elif providers[res] == "viettel":
        print("viettel")
        return(viettel)
    elif providers[res] == "vietnamobile":
        print("vietnamobile")
        return(vietnamobile)
#
#get message-------------------------
def get_message(Device, index, cb =None):
    script = "AT+CMGR={}\r".format(index)
    res = port_write(Device.status["port"],script)
    info = sms_info(res)
    if cb != None:
        res = cb(res)
    raw_sms = ""
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        raw_sms = raw_sms + r
    otp = get_otp(Device,res)
    if otp == "":
        print("message is stored without otp")
    else:
        print("message is stored with otp: "+otp)
    q = "insert into  message values(\""+Device.data["phone_number"]+"\",\""+info["time"]+"\",\""+otp+"\",\""+raw_sms+"\",\""+info["phone"]+"\",\""+info["date"]+","+info["time"]+"\",\"1\");"
    #get_info(q)
    print(q)
    isfull(Device.status["port"],index)
    return(res)
#check sim store full or not and remove all messages when full
def isfull(port,index):
    index = int(index)
    if index > 30:
        while True:
            str = "AT+CMGD=1,4\r"
            res = port_write(port,str)
            for r in res:
                if "OK" in r:
                    return True
                    break
    else:
        return False
#check and get otp:
def get_otp(Device, res:list):
    otp = ""
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        if len(re.findall('\d{6}', r))!=0:
            otp = re.findall('\d{6}', r)[0]
            break
    if otp != "":
        passport_url = "https://api-staging-passport.epsilo.io/receive-otp/shopee"
        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        passport_payload = "{\"phone\": \"" + Device.data["phone_number"] + "\", \"otp\": \"" + otp + \
                                           "\", \"timestamp\": \"" + time_stamp + "\"}"
        passport_headers = {
            'accept': "application/json",
            'cache-control': "no-cache"
        }
        passport_response = connect_with_retry(passport_url, passport_payload, passport_headers)
        print("passport_response: ", passport_response)
        passport_response_error_code = int(passport_response["response_code"])
        error_message = passport_response["response_message"]
        slack_url = settings.SLACK_URL[1]
        slack_headers = {
            'accept': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        if passport_response_error_code == 1:
            print("send success")
            passport_response_data = dict(passport_response["response_data"])
            shop_name = passport_response_data["shopName"]
            country = passport_response_data["country"]
            slack_payload = "{\"channel\": \"#alert-otp\", \"text\": \"\n>Phone number: " \
                            + Device.data["phone_number"] + "\n>OTP: *" + otp + "*\n>Time: " + time_stamp \
                            + "\n>Shop: " + shop_name + "\n>Country: " + country + "\n>\"}"
        else:
            print("send failed")
            slack_payload = "{\"channel\": \"#alert-otp\", \"text\": \"\n>Phone number: " \
                + Device.data["phone_number"] + "\n>OTP: *" + otp + "*\n>Time: " + time_stamp \
                + "\n>Error: " + error_message + "\n>\"}"
        print("slack_url", slack_url, "slack_payload", slack_payload, "slack_headers", slack_headers)
        response_slack = requests.request("POST", slack_url, data=slack_payload
                                                           , headers=slack_headers)
        print(response_slack.text)
    return otp
#check expire date:
def is_expired(res:list):
    date = []
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        if len(re.findall("[0-9]+/[0-9]+/[0-9]+",r))!=0:
            date = re.findall("[0-9]+/[0-9]+/[0-9]+",r)
            break
    if date == []:
        return ("")
    else:
        return date[0]
#get message infor
def sms_info(res:list):
    for r in res:
        r = r.decode("utf-8",errors="ignore")
        if "+CMGR:" in r:
            phone = re.findall("[0-9]+",r)[0]
            date = re.findall("[0-9]+/[0-9]+/[0-9]+",r)[0]
            time = re.findall("[0-9]+:[0-9]+:[0-9]+",r)[0]
            return ({"phone":phone,
                     "date":date,
                     "time":time})
#try to send request to server
def connect_with_retry(url, payload, headers):
    retry = 3
    response = {}
    while retry > 0:
        try:
            response = requests.request("POST", url, data=payload,
                                        headers=headers)
        except requests.exceptions.RequestException:
            print("Connect to passport failed, retrying...")
            retry = retry - 1
            time.sleep(40)
        else:
            break
    data_parse = parse_response(response)
    print("try: ", retry, "data_parse: ", data_parse)
    if retry > 0 and int(data_parse["response_code"]) == 0:
        zero_code_retry_times = 3
        while zero_code_retry_times > 0:
            print("zero code, retrying...")
            response = requests.request("POST", url, data=payload, headers=headers)
            data_parse = parse_response(response)
            if data_parse["response_code"] == 1:
                break
            else:
                zero_code_retry_times = zero_code_retry_times - 1
            # time.sleep(40)
    return data_parse
#parse res
def parse_response(response):
    error_message = ""
    error_code = 0
    data = []
    print(response.text)
    if hasattr(response, 'text'):
        try:
            response_data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            error_code = 500
            error_message = "Something wrong with Passport server"
        else:
            error_code = int(response_data["code"])
            error_message = response_data["message"]
            data = response_data["data"]
    return {
        "response_code": error_code,
        "response_message": error_message,
        "response_data": data
    }
#get gsm name
def gsm_name():
    result = os.popen('ls -al /dev/ | awk \'{print $10}\'').read()
    result =result.split("\n")
    list_path = []
    for r in result:
#       if "tty.usbmodem" in r:
        if "ttyACM" in r:
            list_path.append(r)
    return (list_path)
