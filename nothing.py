from provider import vietnamobile, viettel, vinaphone, mobifone, sim_processing, error_handler
from fastapi import FastAPI, Header
import mysql.connector, responses, requests, json
import serial, os, time, re, queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from core.config import settings

sim = sim_processing
class Device():
    data = {}
    status = {}
list_port = sim.gsm_name()

def e(port_url):
        t = 0
        while t<4:
            path = "/dev/{}".format(port_url)
            port = serial.Serial(path, settings.BAUDRATE, timeout=2)
            port.write("ATI\r".encode())
            time.sleep(float(0.1+t*t))
            res = port.readlines()
            if len(res) != 0 :
                break
            else:
                t += 1
        if t<4:
            Device.status["port"] = port
            Device.status["tries"] = 3
            Device.status["provider"] = sim.check_provider(port)
            Device.data["phone_number"] = Device.status["provider"].get_num(Device)
            Device.status["cThread"] = []
            return(Device)
        else:
            return(False)

def open_port():
    #check working
    #check all port
    list_Device = []
    q = queue.Queue()
    arr = []
    for port_url in list_port:
        t = Thread(target = lambda q,e,port_url: q.put(e(port_url)),args=(q,e,port_url,))
        t.start()
        arr.append(t)
    for t in arr:
        t.join()
    for t in arr:
        Device = q.get()
        if Device != False:
            print(Device.status["port"].name)
            list_Device.append(Device)
        else:
            pass
    for Device in list_Device:
        print(Device.status["port"].name+" : "+Device.data["phone_number"])

open_port()
