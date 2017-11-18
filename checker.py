import time
import requests
import mailer
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def get_price():
    try:
        response = requests.get("https://localbitcoins.com/buy-bitcoins-online/eur/.json")
        data = response.json()
        return float(data["data"]["ad_list"][0]["data"]["temp_price"])
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        print("Error: {}".format(e))


def run():
    old_price = 0

    while True:
        new_price = get_price()

        if new_price != old_price:
            if new_price < old_price:
                message = "price decreased to " + str(new_price)
            elif new_price > old_price:
                message = "price increased to " + str(new_price)

            old_price = new_price
            mailer.send_mail(config['DEFAULT']['receiver'], message, "")

        time.sleep(30)


try:
    run()
except (KeyboardInterrupt, SystemExit):
    print(time.asctime(), "Bitcoin Checker Stopped")
