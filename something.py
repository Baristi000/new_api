import requests

import requests
data={
    "username":"1",
    "password":"secret"
}
x = requests.post('http://localhost:8000/login/token',data=data)

print(x.text)