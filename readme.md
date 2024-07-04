# 网络认证脚本（适用于复旦大学江湾新校区的有线/无线网络连接）

本仓库包含两个用于网络认证的Python脚本：
- `network_auth.py`
- `network_auth_timer.py`

## 描述

### `network_auth.py`

此脚本旨在自动处理网络登录和注销过程。它会定期检查网络连接，并在必要时重新认证。

#### 主要功能:
- 使用提供的凭据登录网络。
- 注销网络。
- 通过ping指定地址检查网络连接。
- 如果网络连接丢失，自动重新认证。

### `network_auth_timer.py`

此脚本使用`schedule`库在每天的指定时间安排登录和注销过程。

#### 主要功能:
- 使用提供的凭据登录网络。
- 注销网络。
- 在每天的特定时间安排重新登录。
- 使用base64编码密码。

## 使用方法

### 前提条件
- Python 3.x
- 所需库：`requests`，`schedule`

使用以下命令安装所需库：
```bash
pip install requests schedule
```

### 配置
在脚本中更新以下变量以使用您的实际登录信息：
- `username`
- `password`
- `domain`

### 运行脚本

#### `network_auth.py`
```bash
python network_auth.py
```

#### `network_auth_timer.py`
```bash
python network_auth_timer.py
```

### 使用`nohup`在后台运行脚本

您可以使用`nohup`命令在后台运行这些脚本，以确保它们即使在关闭终端后仍然运行。

#### `network_auth.py`
```bash
nohup python network_auth.py > network_auth.log 2>&1 &
```

#### `network_auth_timer.py`
```bash
nohup python network_auth_timer.py > network_auth_timer.log 2>&1 &
```

## 法律免责声明

此脚本按“原样”提供，不提供任何保证或担保。使用风险自负。作者不对因使用此脚本而导致的任何损害或损失负责。使用此脚本即表示您同意遵守所有相关法律法规。

## 许可证

此项目基于AGPL-3.0许可进行分发和使用。更多信息请参见[LICENSE](./LICENSE)文件。

---

# Network Authentication Scripts (For Fudan University Jiangwan New Campus Wired/Wireless Network Connection)

This repository contains two Python scripts designed for network authentication:
- `network_auth.py`
- `network_auth_timer.py`

## Description

### `network_auth.py`

This script is designed to handle network login and logout processes automatically. It periodically checks the network connection and re-authenticates if necessary.

#### Key Features:
- Logs into the network using provided credentials.
- Logs out from the network.
- Checks network connectivity by pinging a specified address.
- Automatically re-authenticates if the network connection is lost.

### `network_auth_timer.py`

This script schedules the login and logout processes at specified times daily using the `schedule` library.

#### Key Features:
- Logs into the network using provided credentials.
- Logs out from the network.
- Schedules re-login at a specific time every day.
- Uses base64 encoding for the password.

## Usage

### Prerequisites
- Python 3.x
- Required libraries: `requests`, `schedule`

Install the required libraries using:
```bash
pip install requests schedule
```

### Configuration
Update the following variables in the scripts with your actual login information:
- `username`
- `password`
- `domain`

### Running the Scripts

#### `network_auth.py`
```bash
python network_auth.py
```

#### `network_auth_timer.py`
```bash
python network_auth_timer.py
```

### Running the Scripts in Background using `nohup`

You can run these scripts in the background using the `nohup` command to ensure they continue running even after the terminal is closed.

#### `network_auth.py`
```bash
nohup python network_auth.py > network_auth.log 2>&1 &
```

#### `network_auth_timer.py`
```bash
nohup python network_auth_timer.py > network_auth_timer.log 2>&1 &
```

## Legal Disclaimer

This script is provided as-is without any guarantees or warranty. Use it at your own risk. The authors will not be held responsible for any damages or losses that arise from the use of this script. By using this script, you agree to comply with all relevant laws and regulations.

## License

This project is licensed under the AGPL-3.0 License. For more information, see the [LICENSE](./LICENSE) file.
