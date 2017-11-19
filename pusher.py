#!/usr/bin/env python3.6

import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def push(message):
    id = config["ONTOP"]["id"]
    key = config["ONTOP"]["key"]

    params = {"id": id,
              "key": key,
              "message": message}

    try:
        response = requests.get("https://ontop.tech/api/push", params)
        data = response.json()
        print(data)
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        print("Error: {}".format(e))
