#!/usr/bin/env python3.6
from LocalBitcoinService import LocalBitcoinService
from BitSquareService import BitSquareService
import configparser
import pusher
import time

config = configparser.ConfigParser()
config.read('config.ini')
minimal_price_for_push = float(config["GENERAL"]["push_notification_price"])

old_local_bitcoin_price = minimal_price_for_push + 1
old_bit_square_price = minimal_price_for_push + 1


def run():
    global old_local_bitcoin_price, old_bit_square_price

    while True:
        local_bitcoin = LocalBitcoinService()
        bit_square = BitSquareService()

        new_local_bitcoin_price = local_bitcoin.get_price()
        new_bit_square_price = bit_square.get_price()

        if old_local_bitcoin_price != new_local_bitcoin_price:
            old_local_bitcoin_price = new_local_bitcoin_price
            if new_local_bitcoin_price < minimal_price_for_push:
                pusher.push(
                    "Buy LocalBitcoin! Current price " + str(new_local_bitcoin_price) +
                    ", that is below " + str(minimal_price_for_push) +
                    '\n\nSummary: ' + local_bitcoin.get_summary())

        if old_bit_square_price != new_bit_square_price:
            old_bit_square_price = new_bit_square_price
            if new_bit_square_price < minimal_price_for_push:
                pusher.push(
                    "Buy bit_square! Current price " + str(new_bit_square_price) +
                    ", that is below " + str(minimal_price_for_push) +
                    '\n\nSummary: ' + bit_square.get_summary())

        time.sleep(30)


try:
    run()
except (KeyboardInterrupt, SystemExit):
    print(time.asctime(), "Bitcoin Checker Stopped")
