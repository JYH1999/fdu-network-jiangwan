# 江湾新园区宽带网络登录脚本

## 简介
这是一个自动登录脚本，用于复旦大学江湾新园区宽带网络登录。脚本会定期检查网络连接状态，如果连接中断，则会自动尝试重新登录。

## 特点
- 自动检测网络连接状态。
- 自动登录和登出功能。
- 基于Python和Requests库实现。

## 使用方法

### 前提条件
- 安装Python 3.x
- 安装必要的库: `requests`

### 安装库
在终端或命令行中运行以下命令来安装`requests`库：
```bash
pip install requests
```

### 配置脚本
在`network_auth.py`脚本中找到以下部分并填入你的登录信息：
```python
username = "1234567"  # 请使用你实际的用户名
password = "abcdefg"  # 请使用你实际的密码
```

### 运行脚本
在终端或命令行中运行以下命令来启动脚本：
```bash
python network_auth.py
```

### 后台运行脚本
使用以下命令在后台运行脚本，并将输出日志保存到`network_auth.log`文件中：
```bash
nohup python network_auth.py > network_auth.log 2>&1 &
```

## 脚本功能详解

### 自动登录
脚本会发送一个POST请求到登录接口，并携带用户名、域名和编码后的密码。如果登录成功，会输出 "Login successfully"。

### 自动登出
脚本会发送一个POST请求到登出接口，并在成功登出时输出 "Logout successfully"。

### 网络检测
脚本会定期通过`ping`命令检测网络连接状态。如果检测失败，会尝试重新登录。

### 循环执行
脚本会持续运行，每隔60秒检测一次网络状态，并根据检测结果决定是否重新登录。

---

# Broadband Network Login Script for Jiangwan New Campus of Fudan University

## Introduction
This is an auto-login script designed for the broadband network of the Jiangwan New Campus at Fudan University. The script periodically checks the network connection status and attempts to re-login if the connection is lost.

## Features
- Automatic network connection status detection.
- Automatic login and logout functionality.
- Implemented using Python and the Requests library.

## Usage Instructions

### Prerequisites
- Python 3.x installed
- Required library: `requests`

### Installing the Library
Run the following command in the terminal or command line to install the `requests` library:
```bash
pip install requests
```

### Configuring the Script
Locate the following section in the `network_auth.py` script and fill in your login details:
```python
username = "1234567"  # Replace with your actual username
password = "abcdefg"  # Replace with your actual password
```

### Running the Script
Run the following command in the terminal or command line to start the script:
```bash
python network_auth.py
```

### Running the Script in the Background
Use the following command to run the script in the background and save the output log to the `network_auth.log` file:
```bash
nohup python network_auth.py > network_auth.log 2>&1 &
```

## Script Functionality Explained

### Auto Login
The script sends a POST request to the login URL with the username, domain, and encoded password. If the login is successful, it will output "Login successfully".

### Auto Logout
The script sends a POST request to the logout URL and outputs "Logout successfully" upon a successful logout.

### Network Detection
The script periodically uses the `ping` command to check the network connection status. If the connection fails, it will attempt to re-login.

### Continuous Execution
The script runs continuously, checking the network status every 60 seconds and re-logging in if necessary.