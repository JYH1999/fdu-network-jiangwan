# 复旦校园网认证脚本（适用于复旦大学江湾新园区的有线/无线校园网络连接）

该项目是一个使用 Selenium 自动化浏览器操作的 Python 脚本，主要实现复旦大学江湾新园区的有线/无线校园网络自动登录功能。脚本可以自动填写用户名和密码，点击登录按钮，完成网页认证，并支持在需要时执行登出操作。支持浏览器操作的日志记录，并能在出错时提供截图，帮助调试和问题排查。在合理部署本脚本（如定时运行）的情况下，可实现住宿园区校园网的自动重连（避免登录24h后手动重新登录）。

本仓库包含用于网络认证的Python脚本：
- `network_auth.py`

## 部署要求

### 1. 安装 Python

首先，确保你已经安装了 Python 3.x 版本。可以使用以下命令检查 Python 版本：

```bash
python --version
```

### 2. 安装依赖库

脚本依赖 `selenium` 库来操作浏览器，以及 `logging` 和 `time` 等标准库。你可以通过 `pip` 安装所需的依赖：

```bash
pip install selenium
```

### 3. 安装浏览器驱动

本脚本使用 Firefox 浏览器进行自动化操作。你需要安装 [GeckoDriver](https://github.com/mozilla/geckodriver/releases)，这是 Firefox 浏览器的 WebDriver。

下载后，将其路径添加到系统环境变量中，或者在脚本中指定驱动路径。例如：

```python
service = FirefoxService(executable_path='/path/to/geckodriver')
```

### 4. 安装 Firefox 浏览器

本脚本使用的是 Firefox 浏览器进行自动化。你可以从 [Firefox 官方网站](https://www.mozilla.org/firefox/) 下载并安装 Firefox。

## 配置脚本

### 1. 修改登录凭据

在脚本中，修改以下常量来配置你的登录信息：

```python
USERNAME = 'your_username'  # 替换为你的用户名
PASSWORD = 'your_password'  # 替换为你的密码
```

### 2. 定位元素的 XPath

脚本中有多个地方需要用到 XPath 来定位页面上的元素，比如登录按钮、用户名输入框等。你可以使用浏览器的开发者工具来获取这些元素的 XPath。项目中的脚本默认已经完成除选择`网络出口`外的其他操作按钮的XPath获取。脚本目前默认使用`中国联通`作为网络出口，若您的网络出口不是`中国联通`，请参照本节自行获取XPath并修改脚本中的`xpath`变量。

### 获取 XPath 的方法

#### 1. 使用浏览器开发者工具

##### 1.1. 打开开发者工具
在浏览器中打开你需要获取 XPath 的网页，然后按下 `F12` 键，或者右键点击页面上的任意位置并选择 `检查` 或 `Inspect`，这将打开浏览器的开发者工具。

##### 1.2. 选择目标元素
在开发者工具打开后，选择你想要获取 XPath 的元素。可以通过两种方式来选中元素：

- **方法 1：点击 "元素" 标签**  
  在开发者工具中选择 `Elements` 或 `元素` 标签，浏览器会显示页面的 HTML 代码结构。你可以手动浏览代码，找到你要查找的元素。

- **方法 2：使用 "选择器" 工具**  
  点击开发者工具左上角的一个图标，它看起来像一个鼠标指针，点击它后你可以在页面上直接选择要获取 XPath 的元素，浏览器会高亮显示该元素在 HTML 中的位置。

##### 1.3. 获取 XPath
当你选中目标元素时，可以通过以下两种方式来复制其 XPath：

- **方法 1：右键点击元素**  
  在开发者工具中右键点击选中的元素标签，然后选择 `Copy` -> `Copy XPath`（在 Chrome 中）。对于 Firefox，选择 `Copy` -> `Copy XPath`。这会将该元素的完整 XPath 复制到剪贴板。

- **方法 2：手动构建 XPath**  
  你也可以手动根据页面的结构构建 XPath。XPath 可以通过标签名、类名、ID、属性等多种方式来定位元素。例如：
  
  - 通过元素的标签名：
    ```xpath
    //button
    ```
  
  - 通过元素的 ID：
    ```xpath
    //button[@id='login']
    ```

  - 通过元素的 class 名称：
    ```xpath
    //button[@class='btn-primary']
    ```

  - 通过包含文本的元素：
    ```xpath
    //button[contains(text(), 'Login')]
    ```

  - 通过父子关系：
    ```xpath
    //div[@id='login-container']/button
    ```

  - 通过相邻元素定位：
    ```xpath
    //input[@name='username']/following-sibling::input[@name='password']
    ```

##### 1.4. 验证 XPath 是否有效
你可以在浏览器的控制台中验证 XPath 是否正确。进入 `Console` 标签，使用以下命令来查找元素：

```javascript
$x("//button[@id='login']")
```

这将返回匹配 XPath 的所有元素。

#### 2. 使用绝对 XPath 和相对 XPath

- **绝对 XPath**：从 HTML 文档的根节点开始定位元素。例如：

  ```xpath
  /html/body/div/div/div[2]/button
  ```

- **相对 XPath**：从任意节点开始定位，通常以 ID 或 class 等唯一标识符开始。例如：

  ```xpath
  //button[@id='login-btn']
  ```

相对 XPath 更加灵活，也更能容忍页面结构的变化。

## 运行脚本

### 1. 启动脚本

确保你已经按照上述步骤安装了所有依赖，并且正确配置了浏览器驱动和登录凭据。然后可以通过以下命令来运行脚本：

```bash
python auto_login.py
```

脚本会自动启动 Firefox 浏览器，打开登录页面，填写用户名和密码，执行登录操作。如果登录成功，脚本会记录日志并截图。如果已经登录，脚本会执行登出操作后再重新登录。

### 2. 查看日志和截图

脚本会将操作日志保存到名为 `auto_login.log` 的文件中，所有截图会保存在脚本运行目录下。每当发生错误或操作失败时，脚本会生成相应的截图，以便调试。

## 常见问题

### 1. Firefox 浏览器驱动（geckodriver）无法启动？

请确保你已经正确安装了 GeckoDriver，并且已经将其路径添加到系统环境变量中，或者在脚本中直接指定其路径：

```python
service = FirefoxService(executable_path='/path/to/geckodriver')
```

### 2. 登录失败？

请检查以下几点：

- 确保 `USERNAME` 和 `PASSWORD` 设置正确。
- 确保 XPath 路径正确，特别是页面结构发生变化时。
- 使用浏览器开发者工具手动验证 XPath。

### 3. 脚本运行很慢？

脚本中的 `time.sleep()` 调用会导致等待时间增加。你可以根据需要调整这些时间，或使用显式等待（`WebDriverWait`）来优化性能。

## 法律免责声明

此脚本按“原样”提供，不提供任何保证或担保。使用风险自负。作者不对因使用此脚本而导致的任何损害或损失负责。使用此脚本即表示您同意遵守所有相关法律法规，包括复旦大学有关校园网络的所有管理规定。

## 许可证

此项目基于AGPL-3.0许可进行分发和使用。更多信息请参见[LICENSE](./LICENSE)文件。

---

# Fudan Campus Network Authentication Script (For Wired/Wireless Network Connection in Fudan University's Jiangwan New Campus)

This project is a Python script that uses Selenium to automate browser operations, primarily designed to enable automatic login for wired/wireless campus network connections at Fudan University's Jiangwan New Campus. The script can automatically fill in the username and password, click the login button, complete the web authentication, and support logout operations when needed. It also logs browser actions and provides screenshots in case of errors to aid debugging and troubleshooting. With reasonable deployment (e.g., scheduled runs), the script can achieve automatic reconnection to the campus network in dormitory areas, avoiding the need to manually log in after 24 hours.

This repository contains the Python script used for network authentication:
- `network_auth.py`

## Deployment Requirements

### 1. Install Python

First, ensure that Python 3.x is installed. You can check the Python version with the following command:

```bash
python --version
```

### 2. Install Required Libraries

The script depends on the `selenium` library for browser automation, as well as standard libraries such as `logging` and `time`. You can install the necessary dependencies using `pip`:

```bash
pip install selenium
```

### 3. Install Browser Driver

The script uses the Firefox browser for automation. You need to install [GeckoDriver](https://github.com/mozilla/geckodriver/releases), which is the WebDriver for Firefox.

After downloading, add the path to your system's environment variables or specify the driver path in the script. For example:

```python
service = FirefoxService(executable_path='/path/to/geckodriver')
```

### 4. Install Firefox Browser

This script uses the Firefox browser for automation. You can download and install Firefox from the [official website](https://www.mozilla.org/firefox/).

## Script Configuration

### 1. Modify Login Credentials

In the script, modify the following constants to configure your login information:

```python
USERNAME = 'your_username'  # Replace with your username
PASSWORD = 'your_password'  # Replace with your password
```

### 2. Locate Elements' XPath

There are several places in the script that require XPath to locate elements on the page, such as the login button and the username input field. You can use the browser's developer tools to get these elements' XPath. The script already contains XPath for most operations, except for selecting the `Network Exit`. The script defaults to using `China Unicom` as the network exit, so if your network exit is different, you should manually retrieve the XPath and modify the `xpath` variable in the script.

### How to Retrieve XPath

#### 1. Use Browser Developer Tools

##### 1.1. Open Developer Tools  
Open the webpage where you need to get the XPath, then press `F12`, or right-click anywhere on the page and select `Inspect` to open the browser's developer tools.

##### 1.2. Select the Target Element  
Once the developer tools are open, select the element you want to get the XPath for. You can select elements in two ways:

- **Method 1: Click the "Elements" Tab**  
  In the developer tools, select the `Elements` tab. The browser will show the HTML structure of the page, and you can browse through it to find the element you're looking for.

- **Method 2: Use the "Selector" Tool**  
  Click the icon in the top-left corner of the developer tools (which looks like a mouse pointer). After clicking it, you can select the element directly on the page, and the browser will highlight the corresponding HTML structure.

##### 1.3. Get XPath  
When the target element is selected, you can copy its XPath using one of the following two methods:

- **Method 1: Right-click the Element**  
  In the developer tools, right-click the selected element tag and choose `Copy` -> `Copy XPath` (in Chrome). In Firefox, choose `Copy` -> `Copy XPath`. This will copy the full XPath of the element to the clipboard.

- **Method 2: Manually Construct XPath**  
  You can also manually construct the XPath based on the page structure. XPath can locate elements using tag names, class names, IDs, attributes, and other criteria. For example:

  - By tag name:
    ```xpath
    //button
    ```

  - By element ID:
    ```xpath
    //button[@id='login']
    ```

  - By element class name:
    ```xpath
    //button[@class='btn-primary']
    ```

  - By text content:
    ```xpath
    //button[contains(text(), 'Login')]
    ```

  - By parent-child relationship:
    ```xpath
    //div[@id='login-container']/button
    ```

  - By sibling element:
    ```xpath
    //input[@name='username']/following-sibling::input[@name='password']
    ```

##### 1.4. Validate XPath  
You can validate the XPath in the browser's console. Go to the `Console` tab and use the following command to find the element:

```javascript
$x("//button[@id='login']")
```

This will return all elements that match the XPath.

#### 2. Use Absolute XPath and Relative XPath

- **Absolute XPath**: This starts from the root node of the HTML document. For example:

  ```xpath
  /html/body/div/div/div[2]/button
  ```

- **Relative XPath**: This starts from any node, usually starting with an ID or class. For example:

  ```xpath
  //button[@id='login-btn']
  ```

Relative XPath is more flexible and can tolerate changes in the page structure better.

## Running the Script

### 1. Start the Script

Make sure that you have installed all dependencies and correctly configured the browser driver and login credentials. Then, run the script with the following command:

```bash
python auto_login.py
```

The script will automatically start the Firefox browser, open the login page, fill in the username and password, and perform the login operation. If the login is successful, the script will log the actions and take a screenshot. If already logged in, the script will log out and then log in again.

### 2. View Logs and Screenshots

The script will save the operation logs in a file named `auto_login.log`, and all screenshots will be saved in the directory where the script is run. Whenever an error occurs or an operation fails, the script will generate corresponding screenshots to aid in debugging.

## Frequently Asked Questions

### 1. GeckoDriver (Firefox Driver) Does Not Start?

Ensure that you have installed GeckoDriver correctly and added its path to the system environment variables, or directly specify its path in the script:

```python
service = FirefoxService(executable_path='/path/to/geckodriver')
```

### 2. Login Fails?

Check the following:

- Ensure that `USERNAME` and `PASSWORD` are correctly set.
- Verify that the XPath paths are correct, especially if the page structure has changed.
- Manually validate the XPath using the browser's developer tools.

### 3. The Script Runs Slowly?

The `time.sleep()` calls in the script might increase the waiting time. You can adjust these times as needed or use explicit waits (`WebDriverWait`) to optimize performance.

## Legal Disclaimer

This script is provided "as is," without any guarantees or warranties. Use at your own risk. The author is not responsible for any damages or losses caused by the use of this script. By using this script, you agree to comply with all relevant laws and regulations, including all management rules of Fudan University's campus network.

## License

This project is distributed under the AGPL-3.0 license. For more information, please refer to the [LICENSE](./LICENSE) file.