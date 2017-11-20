import requests
from interface import implements
from PriceInterface import PriceInterface


class BitSquareService(implements(PriceInterface)):
    _api_url = 'https://markets.bisq.network/api/offers?market=btc_eur&direction=SELL&format=json'
    amount = 0
    min_amount = 0
    payment_method = ''
    price = 0
    volume = 0

    def __init__(self):
        data = self._get_data()
        self._process_data(data)

    def _get_data(self):
        response = requests.get(self._api_url)
        return response.json()

    def _process_data(self, data):
        self.price = float(data['btc_eur']['sells'][0]['price'])
        self.amount = float(data['btc_eur']['sells'][0]['amount'])
        self.min_amount = float(data['btc_eur']['sells'][0]['min_amount'])
        self.payment_method = data['btc_eur']['sells'][0]['payment_method']
        self.volume = float(data['btc_eur']['sells'][0]['volume'])

    def get_price(self):
        return float(self.price)

    def get_summary(self):
        summary = ('\nAmount: ' + str(self.amount) +
                   '\nMin Amount: ' + str(self.min_amount) +
                   '\nPayment Method: ' + str(self.payment_method) +
                   '\nPrice: ' + str(self.price) +
                   '\nVolume: ' + str(self.volume))
        return summary
