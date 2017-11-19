#!/usr/bin/env python3.6

import time
import requests
import mailer
import pusher
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_price():
    try:
        response = requests.get("https://localbitcoins.com/buy-bitcoins-online/eur/.json")
        data = response.json()

        print('\n\nName: ' + data["data"]["ad_list"][0]["data"]['profile']['name'])
        print('Loc: ' + data["data"]["ad_list"][0]["data"]['location_string'])
        print('Online provider: ' + data["data"]["ad_list"][0]["data"]['online_provider'])
        print('Bank: ' + data["data"]["ad_list"][0]["data"]['bank_name'])
        print('Price: ' + data["data"]["ad_list"][0]["data"]["temp_price"])

        return float(data["data"]["ad_list"][0]["data"]["temp_price"])
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        print("Error: {}".format(e))


def run():
    minimal_price_for_push = float(config["GENERAL"]["push_notification_price"])
    old_price = minimal_price_for_push + 1

    while True:
        new_price = get_price()

        if new_price != old_price:

            if new_price < old_price:
                message = "price decreased to " + str(new_price)
            elif new_price > old_price:
                message = "price increased to " + str(new_price)
            else:
                print('Price is the same.\n\n')

            if new_price < minimal_price_for_push:
                pusher.push(
                    "Buy Bitcoin! Current price " + str(new_price) + ", that is below " + str(minimal_price_for_push))

            old_price = new_price
            mailer.send_mail(config['GMAIL']['receiver'], message, "")

        time.sleep(30)


try:
    run()
except (KeyboardInterrupt, SystemExit):
    print(time.asctime(), "Bitcoin Checker Stopped")
