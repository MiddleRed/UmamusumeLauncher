# UmamusumeLauncher
English | 中文
Launching Umamusume Pretty Derby game directly without DMM Game Player.  
Theoretically support other games on DMM Game Player.
## Usage
We assume that your operating system is Windows 10 or higher.
1. Install Python 3.7+
2. Download the source code, unzip it.
3. Open `Powershell` or `cmd` at the folder you unzip the code and execute this command 
```
pip install -r requirement.txt
```
4. Download Microsoft Edge WebDriver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/  
Put `msedgedriver.exe` in this folder.
5. Create `config.json` and `account_info.json` in this folder and filling the necessary information.   
In `config.json` :
```
{
    "game_exe_path": "C:/Users/Umamusume/umamusume.exe",

    "game_info": {
        "product_id": "umamusume",
        "game_type": "GCL",
        "launch_type": "LIB"
    },

    "proxy": "http://127.0.0.1:1234",

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
Change the setting base on your own occasion.
5. Run `launch.py`.  
Tips: If you don't want to see the python window pop up every time you boot the launcher, rename `launch.py` as `launch.pyw`.
