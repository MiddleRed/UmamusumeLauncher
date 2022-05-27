import os, sys

from colorama import init
init(autoreset=True)

import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import hashlib
from getmac import get_mac_address
import wmi


config = {}
account_info = {}

def reboot(text = "The application will reboot and try to login again."):
    print_warning(text)
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

def print_warning(text):
    print("\033[0;33m" + "WARNING: "+ text + "\033[0m")

def print_error(text, serious = False, reboot = True):
    print("\033[0;31m" + "ERROR: " + text + "\033[0m")
    if serious:
        exit(0)
    if reboot:
        reboot()

def print_green(text):
    print("\033[0;32m" + text + "\033[0m")

def read_setting(file_name):
    with open(file_name, "r", encoding="UTF-8") as f:
        j = json.load(f)
    return j

def read_config_setting(setting, serious = False):
    global config
    if setting not in config:
        print_error("Config setting not found: " + setting, serious=serious, reboot=False)
        return 0
    return config[setting]

def get_user_cookie(login_id, password):
    print("Loading login environment...")
    # GET login url
    session = requests.session()
    
    # try to get login_url in 5 times
    for i in range(5):
        try:
            req = session.get("https://apidgp-gameplayer.games.dmm.com/v5/loginurl", timeout=5)
            break
        except:
            time.sleep(0.5)
            continue
    else:
        print_error("Get login url failed.")
    
    loginurl = json.loads(req.text)["data"]["url"]

    # Initialize webdriver
    try:
        print("Setting up login browser...")
        browser = read_config_setting("browser", True)
        driver_path = read_config_setting("driver_path", True)
        if_headless = not read_config_setting("show_browser_when_login")
        if_stable_login = read_config_setting("stable_login")

        def set_options(option):
            if not if_stable_login:
                if if_headless:
                    option.add_argument("--headless")
                option.add_argument("--disable-gpu")
                option.add_argument("--no-sandbox")
                option.add_argument("--disable-dev-shm-usage")
                option.add_argument("--disable-extensions")
                option.add_argument("blink-settings=imagesEnabled=false")
                prefs = {
                    "profile.managed_default_content_settings.images": 2,
                    "permissions.default.stylesheet": 2
                }
                option.add_experimental_option("prefs", prefs)
                option.add_experimental_option("excludeSwitches", ["enable-logging"])
            if read_config_setting("proxy") != 0:
                option.add_argument("--proxy-server="+read_config_setting("proxy"))
            return option

        if browser == "Chrome":
            from selenium.webdriver.chrome.service import Service
            driver = webdriver.Edge(service=Service(driver_path), options=set_options(webdriver.ChromeOptions()))
        elif browser == "Firefox":
            from selenium.webdriver.firefox.service import Service
            driver = webdriver.Edge(service=Service(driver_path), options=set_options(webdriver.FirefoxOptions()))
        elif browser == "Edge":
            from selenium.webdriver.edge.service import Service
            driver = webdriver.Edge(service=Service(driver_path), options=set_options(webdriver.EdgeOptions()))
        else:
            print_error("Browser not supported: " + browser, serious=True)

    except Exception as e:
        print_error("Initialize webdriver failed: " + str(e), serious=True)

    # Simulate manual login
    print("Connecting to the login website...")
    driver.get(loginurl)

    if driver.page_source.find("not available in your region") != -1:
        print_error("Your IP address is forbidden. Please use Japan IP to login.", serious=True)
    driver.find_element(by=By.ID,value='login_id').send_keys(login_id)
    driver.find_element(by=By.ID,value='password').send_keys(password)
    driver.find_element(by=By.XPATH,value='//*[@id="loginbutton_script_on"]/span/input').click()

    # Wait until get login cookies
    print("Waiting for cookies...")
    while True:
        if driver.get_cookie("login_session_id") != None:
            driver_cookies = driver.get_cookies()
            break

    for cookies in driver_cookies:
        if cookies['name'] == 'login_session_id':
            break
    else:
        print_error("Fail to get login_session_id")

    driver.close()
    user_cookies = {c['name']:c['value'] for c in driver_cookies}
    return user_cookies


def get_game_launch_args(game_info,user_cookies,mac_address,hdd_serial,motherboard):
    print("Get game launching arguments...")
    if read_config_setting("proxy") == 0:
        proxy = {}
    else:
        proxy = {
            "https":read_config_setting("proxy"),
            "http":read_config_setting("proxy")
        }

    header = {
        "Accept-Encoding" : "gzip, deflate, br",
        "User-Agent": "DMMGamePlayer5-Win/5.0.119 Electron/17.2.0",
        "Client-App": "DMMGamePlayer5",
        "Client-version": "5.0.119",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"no-cors",
        "Sec-Fetch-Site":"none"
    }

    get_game_info_json = {
        "product_id": game_info["product_id"],
        "game_type": game_info["game_type"],
        "game_os": "win",
        "launch_type": game_info["launch_type"],
        "mac_address": mac_address,
        "hdd_serial": hdd_serial,
        "motherboard": motherboard,
        "user_os": "win"
    }
    
    def cope_request_fail(response,text):
        if response["result_code"] != 100:
            if response["error"] == "DMM session has expired":
                with open("account_info.json", "w", encoding="UTF-8") as f:
                    account_info["cookies"] = {}
                    json.dump(account_info, f, indent=4)
                print_error("DMM session has expired.", reboot = False)
                reboot("The application will reboot and try to login without cookies.")
            raise print_error(response["error"])

    session = requests.session()
    req = session.post(
        "https://apidgp-gameplayer.games.dmm.com/v5/gameinfo",
        json = get_game_info_json,
        headers = header,
        cookies = user_cookies,
        proxies = proxy
    )
    cope_request_fail(json.loads(req.text),"Get game info failed: ")

    args = session.post(
        "https://apidgp-gameplayer.games.dmm.com/v5/launch/cl",
        json = get_game_info_json,
        headers = header,
        cookies = user_cookies,
        proxies = proxy
    )
    cope_request_fail(json.loads(args.text),"Get game start argument failed: ")

    req = session.post(
        "https://apidgp-gameplayer.games.dmm.com/v5/report", 
        json=
        {
            "type":"start",
            "product_id":game_info["product_id"],
            "game_type":game_info["game_type"]
        },
        headers = header,
        cookies = user_cookies,
        proxies = proxy
    )
    cope_request_fail(json.loads(req.text),"Report failed: ")

    return json.loads(args.text)["data"]["execute_args"]

if __name__ == "__main__":
    try:
        os.chdir(sys.path[0])

        config = read_setting("config.json")
        account_info = read_setting("account_info.json")

        if "user" not in account_info:
            print_error("Cannot read user info in account_info.json.")

        if "game_exe_path" not in config:
            print_error("Cannot read the game exe path in config.json.",serious=True)

        account = account_info["user"]
        if "mac_address" not in account:
            account_info["user"]["mac_address"] = get_mac_address()
        if "hdd_serial" not in account:
            account_info["user"]["hdd_serial"] = hashlib.sha256((",".join(
                item.SerialNumber.strip(" ") for item in wmi.WMI().Win32_PhysicalMedia()
            )).encode('UTF-8')).hexdigest() # not real hdd serial
        if "motherboard" not in account:
            account_info["user"]["motherboard"] = hashlib.sha256((account["hdd_serial"] + account["mac_address"])
            .encode('UTF-8')).hexdigest() # not real motherboard
        
        use_cookies = False
        if "cookies" in account_info:
            cookies = account_info["cookies"]
            if "login_session_id" in cookies and "login_secure_id" in cookies:
                print("Program will use cookies in account_info.json")
                use_cookies = True
            else:
                print_warning("Cookies is missing or invalid. Program will generate new cookies.")
        else:
            print_warning("Cookies is not exist. Program will generate new cookies.")
        

        def load_cookies():
            if "login_id" not in account:
                print_error("Account info is not exist or incompleted: Missing login_id",serious=True)
            if "password" not in account:
                print_error("Account info is not exist or incompleted: Missing password",serious=True)

            user_cookies = get_user_cookie(account_info["user"]["login_id"], account_info["user"]["password"])
            account_info["cookies"] = user_cookies
            if not read_config_setting("not_store_cookies"):
                with open("account_info.json", "w", encoding="UTF-8") as f:
                    json.dump(account_info, f, indent=4)

        if not use_cookies:
            load_cookies()
            print_green("Succesfully get user cookies.")

        args = get_game_launch_args(read_config_setting("game_info", True), 
            account_info["cookies"],
            account_info["user"]["mac_address"],
            account_info["user"]["hdd_serial"],
            account_info["user"]["motherboard"])

        os.system('start "" {} {} '.format(config["game_exe_path"], args))
        print_green("Succesfully get game launching arguments.")
        print("Program will exit 3 seconds later.")
        time.sleep(3)
        
        exit(0)
    except Exception as e:
        print_error(str(e))
        exit(1)