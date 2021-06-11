import datetime
import json
import requests

from decorators import retry
from typing import Tuple
from urllib.parse import urlencode


class GrabberMixin():
    """Universal implementation for a free plan for receiving exchange rates."""

    def receive(self, url: str) -> Tuple[str, int]:
        """Receives exchange rates by the passed url"""
        r = requests.get(url)
        if r.status_code == 200:
            j = json.loads(r.text)
            rates = j['rates']
            ts = j['timestamp']
            return (rates, ts)


class Grabber(GrabberMixin):
    """Base setup of receiving exchange rates from OpenExchangeRates.org"""

    BASE_URL = 'https://openexchangerates.org/api/'
    LATEST = BASE_URL + 'latest.json/'
    HISTORICAL = BASE_URL + 'historical/%s.json/'

    def __init__(self, api_key,):
        self.api_key = api_key
        
    @retry
    def latest(self) -> Tuple[str, int]:
        """Receives the latest exchange rates."""
        params = {'app_id=': self.api_key}
        url = self.LATEST + '?' + urlencode(params)
        return super().receive(url)
    
    @retry
    def historical(self, date: str, alt='false', prprint='false') -> Tuple[str, int]:
        """Receives exchange rates for a concrete date."""
        params = {
            'app_id': self.api_key,
            'prettyprint': prprint,
            'show_alternative': alt,
        }
        url = self.HISTORICAL % date + '?' + urlencode(params)
        return super().receive(url)
