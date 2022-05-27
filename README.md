# UmamusumeLauncher
English | [中文](README_zh.md) 

Launching Umamusume Pretty Derby game directly without opening DMM Game Player.  
Theoretically support all the games that need to be launched by DMM Game Player.
## Usage
Assume that your operating system is Windows 10 or higher.
1. Install Python 3.7+
2. Download the source code, unzip it.
3. Open `Powershell` or `cmd` at the folder you unzip it and execute this command 
```
pip install -r requirement.txt
```
4. Download Microsoft Edge WebDriver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/  
Put `msedgedriver.exe` in this folder.
5. Create `config.json` and `account_info.json` in this folder and filling the necessary information. Change the settings base on your own occasion.     

In `config.json` , copy the following example to it, and fill the `game_exe_path` and `proxy`:
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
In `account_info.json`:
```
{
    "user": {
        "login_id": "enterYourDMMAccountEmail@example.com",
        "password": "enterYourDMMAccountPassword",
    }
}
```
5. If everything fine, you can now boot the game directly by just runing the `launch.py` file.  

Tips: If you don't want to see the python window pops up every time you boot the launcher, rename `launch.py` as `launch.pyw` . But it will cause you cannot get the detailed information when the launcher meets problems.    

Remember to replace all the `\` character with `/` or `\\` , or the launcher cannot read the json file.  

**Note: The launcher cannot automatically update the game. If there is a game update, you need to download it in DMM Game Player mannually.**    

The game launched by this program cannot automatically connect to the proxy server, so you may need to use software such as netch or Proxifier to redirect the game network to it.  

## Config setting
````
{
    "game_exe_path": "C:/Umamusume/umamusume.exe",
    // File path of game exe

    "game_info": {
        "product_id": "umamusume",
        "game_type": "GCL",
        "launch_type": "LIB"
    },
    // Do not change it if you don't know what it is

    "proxy": "http://127.0.0.1:8123",
    // The proxy that you are using to play the game
    // DMM blocks all non-Japan IP addresses' connections, so you have to provide a proxy server for the launcher to connect it 
    // Delete this setting if you don't need a proxy server

    "not_store_cookies": false,
    // Whether store the user cookies
    // Store the login cookies can make the launching process faster

    "browser": "Edge",
    // Browser that program use to simulate login process
    // Support browser: Chrome, Firefox, Edge
    // Note: you must download the corresponding webdriver mannully, regardless of which browser you choose
    // For Chrome: https://chromedriver.chromium.org/downloads
    // For Firefox: https://github.com/mozilla/geckodriver/releases/
    // Remember change the `driver_path` setting

    "driver_path": "msedgedriver.exe",
    // File path of the webdriver

    "show_browser_when_login": false,
    // Whether show the browser during login
    // Mainly for debugging

    "stable_login": false
    // Used for disabling all the optimizations during login
    // Enable it if the launcher can't login normally
}
````
## Technical details
The program uses `requests` to handle simple network connections.  
When it comes to complex occasions such as user login, the program uses `selenium` to simulate the login process, and get the user cookies from it. `selenium` requires webdriver to control the browser.     
The cookies is stored in `account_info.json` , and after we get the cookies, the program can use it to request the launching parameters, which is used to boot the game.  
