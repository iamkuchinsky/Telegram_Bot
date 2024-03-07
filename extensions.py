import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        quote = str.lower(quote)
        base = str.lower(base)
        amount = str.lower(amount)
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые курсы валют {base}\n/help - помощь')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}\n/help - помощь')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}\n/help - помощь')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}\n/help - помощь')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[str.lower(base)]]

        return total_base
