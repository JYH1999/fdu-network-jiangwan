import time
import datetime
import random
import threading
import base64
import os

import requests


login_url = r'http://10.102.250.13/index.php/index/login'
logout_url = r'http://10.102.250.13/index.php/index/logout'

# 你的登录信息
username = "1234567" # 请使用你实际的用户名
password = "abcdefg"  # 请使用你实际的密码
encoded_password = base64.b64encode(password.encode()).decode()  # 对密码进行base64编码
domain = "unicom-pppoe"# 中国联通宽带

random.seed(time.time())

def do_login():
    log("Start login process")

    headers = {
    "Host": "10.102.250.13",
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "DNT": "1",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://10.102.250.13",
    "Referer": "http://10.102.250.13/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }

    payload = {
        "username": username,
        "domain": domain,
        "password": encoded_password,
        "enablemacauth": "0"
    }
    # 发送POST请求
    response = requests.post(login_url, headers=headers, data=payload)
    if response.json()["status"]==0:
        log("Login Fail: {}".format(response.json()["info"]))
        return False
    else:
        log("Login successfully")
        return True
    
def do_logout():
    log("Start logout process")

    # 请求头
    headers = {
        "Host": "10.102.250.13",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "DNT": "1",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://10.102.250.13",
        "Referer": "http://10.102.250.13/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Length": "0",
    }
    response = requests.post(logout_url, headers=headers, data={})
    if response.json()["status"]==0:
        log("Logout Fail: {}".format(response.json()["info"]))
        return False
    else:
        log("Logout successfully")
        return True

def test_network():
    retry_times = 3
    for i in range(retry_times):
        ret_code = os.system("ping www.baidu.com -c 1 -W 1")
        if ret_code == 0:
            log("Ping success")
            return True
    log("Ping failed after {0} times".format(retry_times))
    return False

def log(msg):
    print("{time}: {msg}".format(time=datetime.datetime.now(), msg=msg))

def start_making_request():

    while True:
        if (not test_network()):
            log("Network connection is bad, try to relogin")
            do_logout()
            do_login()
        
        # sleep 1 minute
        sleep_seconds = 60
        time.sleep(sleep_seconds)

if __name__ == '__main__':
    threading.Thread(target=start_making_request).start()
