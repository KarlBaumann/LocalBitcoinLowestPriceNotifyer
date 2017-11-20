import requests
from interface import implements
from PriceInterface import PriceInterface


class LocalBitcoinService(implements(PriceInterface)):
    _api_url = "https://localbitcoins.com/buy-bitcoins-online/eur/.json"
    name = ''
    location_string = ''
    online_provider = ''
    bank_name = ''
    temp_price = 0

    def __init__(self):
        data = self._get_data()
        self._process_data(data)

    def _get_data(self):
        response = requests.get(self._api_url)
        return response.json()

    def get_price(self):
        return float(self.temp_price)

    def _process_data(self, data):
        self.name = data["data"]["ad_list"][0]["data"]['profile']['name']
        self.location_string = data["data"]["ad_list"][0]["data"]['location_string']
        self.online_provider = data["data"]["ad_list"][0]["data"]['online_provider']
        self.bank_name = data["data"]["ad_list"][0]["data"]['bank_name']
        self.temp_price = data["data"]["ad_list"][0]["data"]["temp_price"]

    def get_summary(self):
        summary = ('\n\nName: ' + str(self.name) +
                   '\nLoc: ' + str(self.location_string) +
                   '\nOnline provider: ' + str(self.online_provider) +
                   '\nBank: ' + str(self.bank_name) +
                   '\nPrice: ' + str(self.temp_price))
        return summary
