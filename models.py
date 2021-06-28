import json
import requests

from decorators import retry
from exceptions import APIKeyError
from typing import Tuple
from urllib.parse import urljoin


class Client():
    """
    Base client for receiving exchange rates from OpenExchangeRates.org
    """
    BASE_URL = 'https://openexchangerates.org/api/'
    LATEST = urljoin(BASE_URL, 'latest.json')
    HISTORICAL = urljoin(BASE_URL, 'historical/%s.json')

    def __init__(self, api_key,):
        self.api_key = self.check_key(api_key)

    def check_key(self, api_key):
        if not api_key.strip():
            raise ValueError('Your API key cannot be empty.')
        return api_key

    def get(self, args):
        query_type = args.type
        currencies = args.currencies
        if query_type == 'latest':
            return self.latest(currencies)
        elif query_type == 'historical':
            y, m, d = args.year, args.month, args.day
            if not (y and m and d):
                raise ValueError('Specify the full date by the following arguments: '
                                 '-y YYYY -m MM -d DD, where YYYY, MM, DD are an year, '
                                 'a month and a day of your date, respectively.')
            date = f'{y}-{m:02}-{d:02}'
            return self.historical(date, currencies)

    def receive(self, url, currencies) -> Tuple[str, int]:
        """
        Receives exchange rates by the passed url.
        """
        params = {'app_id': self.api_key}
        if currencies:
            params['symbols'] = ','.join(currencies)

        r = requests.get(url, params)
        if r.status_code == 200:
            j = json.loads(r.text)
            rates = j['rates']
            ts = j['timestamp']
            if currencies:
                self.check_currencies(rates, currencies)
            return (rates, ts)
        elif r.status_code == 401:
            raise APIKeyError
        else: 
            raise Exception('Something went wrong. Try again later.')
        
    @retry
    def latest(self, currencies) -> Tuple[str, int]:
        """
        Receives the latest exchange rates.
        """
        url = self.LATEST
        return self.receive(url, currencies)
    
    @retry
    def historical(self, date, currencies) -> Tuple[str, int]:
        """
        Receives exchange rates for a specific date.
        """
        url = self.HISTORICAL % date
        return self.receive(url, currencies)

    def check_currencies(self, rates, curr_list):
        """
        Checks the presence of the specified currencies 
        in the received exchange rates.

        Displays a list of missing currencies.
        """
        missing = [curr for curr in curr_list if curr not in rates]
        if missing:
            print(f"[{', '.join(missing)}] "
                  f"{'is' if len(missing) == 1 else 'are'} "
                  f"missing from the received exchange rates.")
