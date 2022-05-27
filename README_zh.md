# UmamusumeLauncher
不需要启动 DMM Game Player ，直接从外部启动赛马娘游戏  
理论上支持所有从 DMM Game Player 启动的游戏
## Usage
默认你的系统是 Windows 10 或者更高版本
1. 安装 Python 3.7+
2. 下载项目源码，解压全部文件
3. 在解压的文件夹里打开 `Powershell` 或者 `cmd` ，并执行下面的命令 
```
pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
4. 下载 Edge 浏览器的 WebDriver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/  
把下载完成的 `msedgedriver.exe` 放到此文件中.
5. 在此文件夹中创建 `config.json` 和 `account_info.json` ，并填入必要的信息。结合你自己的具体情况填写     

在 `config.json` 中, 复制以下的样例到此文件中，并填写 `game_exe_path`（游戏exe的文件位置） 和 `proxy`（所使用的代理或者加速器地址，不知道的请看下面的教程）:
```
{
    "game_exe_path": "A:/The/file/path/to/umamusume.exe",

    "game_info": {
        "product_id": "umamusume",
        "game_type": "GCL",
        "launch_type": "LIB"
    },

    "proxy": "proxyAddressThatUsedToPlayGame://127.0.0.1:1234",

    "browser": "Edge",
    "driver_path": "msedgedriver.exe"
}
```
在 `account_info.json` 中填写你的 DMM 账号邮箱以及密码:
```
{
    "user": {
        "login_id": "enterYourDMMAccountEmail@example.com",
        "password": "enterYourDMMAccountPassword",
    }
}
```
5. 如果一切设置妥当，你之后只需要启动 `launch.py` 文件就能启动游戏了 

Tips: 如果你不想每次点开 `launch.py` 都弹出 Python 的窗口，可以将 `launch.py` 重命名为 `launch.pyw`。但这也会导致如果启动过程中出现了问题，你不知道问题是什么。  

记得将所有 `\` 符号替换为 `/` 或者 `\\` ，否则启动器无法读取 json 文件。

**注意：启动器无法自动下载游戏更新。你需要手动通过 DMM Game Player 下载安装。**    
 
## 如何设置代理
启动器不能让游戏启动后自己走代理或者加速器。如果出现了网络错误，你需要用 netch 或者 Proxifier 等软件来让游戏走代理。具体请查看此教程：https://github.com/MiddleRed/UmamusumeLauncher/issues/1

## 配置参数
````
{
    "game_exe_path": "C:/Umamusume/umamusume.exe",
    // 游戏 exe 目录

    "game_info": {
        "product_id": "umamusume",
        "game_type": "GCL",
        "launch_type": "LIB"
    },
    // 除非你知道这是什么意思，否则不要动这个设置

    "proxy": "http://127.0.0.1:8123",
    // 你用来玩游戏的代理服务器的地址
    // DMM 会拦截所有非日本 IP 的连接，所以你需要提供一个代理服务器地址来让启动器能访问 DMM 
    // 如果你不需要通过代理访问，请将此选项删除

    "not_store_cookies": false,
    // 是否不存储登录 cookies
    // 存储 cookies 可以让启动速度加快 

    "browser": "Edge",
    // 用来模拟登录流程的浏览器
    // 目前支持的： Chrome, Firefox, Edge
    // 注意：不论你选择哪个浏览器，你都需要下载对应的浏览的 Webdriver
    // 下载 Chrome 的 Webdriver ：https://chromedriver.chromium.org/downloads
    // 下载 Firefox 的 Webdriver : https://github.com/mozilla/geckodriver/releases/
    // 记得更改 `driver_path` 

    "driver_path": "msedgedriver.exe",
    // Webdriver 的文件地址

    "show_browser_when_login": false,
    // 是否显示模拟登录时的浏览器
    // 主要用于 debug

    "stable_login": false
    // 去除所有优化项，原生处理登录流程
    // 如果启动器无法正常登录，请尝试将此项设置为 true
}
````
## 技术细节
启动器使用 `requests` 来处理简单的网络请求  
当遇到像登录等比较复杂的情况时，启动器使用 `selenium` 来模拟这个流程，并保存登录成功后的 `cookies`。`selenium` 需要 Webdriver 才能控制浏览器     
Cookies 存储于 `account_info.json` 中。当 Cookies 存在时，启动器就可以请求服务器返回启动游戏所需的启动参数
