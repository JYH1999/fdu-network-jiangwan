import time
import datetime
import random
import base64
import os
import requests
import schedule
import sys

login_url = r'http://10.102.250.13/index.php/index/login'
logout_url = r'http://10.102.250.13/index.php/index/logout'

# 你的登录信息
username = "123456"  # 请使用你实际的用户名
password = "abcdefg"  # 请使用你实际的密码
encoded_password = base64.b64encode(password.encode()).decode()  # 对密码进行base64编码
domain = "unicom-pppoe"  # 中国联通宽带

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
    if response.json()["status"] == 0:
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
    if response.json()["status"] == 0:
        log("Logout Fail: {}".format(response.json()["info"]))
        return False
    else:
        log("Logout successfully")
        return True

def log(msg):
    print("{time}: {msg}".format(time=datetime.datetime.now(), msg=msg))
    sys.stdout.flush()  # 确保立即刷新输出缓冲区

def relogin():
    log("It's time to relogin")
    do_logout()
    log("Wait for 3 seconds")
    time.sleep(3)
    do_login()

schedule.every().day.at("03:14").do(relogin)

if __name__ == '__main__':
    log("Start network auth program")
    log("Relogin at startup:")
    relogin()
    while True:
        schedule.run_pending()
        time.sleep(1)
