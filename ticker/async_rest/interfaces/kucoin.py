""" Hides the KuCoin exchange interface """
import logging
import time
import hashlib
import hmac
import base64
import os
# import json

from .api import Api, NoData

# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://api.kucoin.com"  # 'ETH-BTC'
an_endpoint = "/api/v1/market/orderbook/level1"


def auth(endpoint, data=''):
    """ Example for get balance of accounts in python"""
    api_key = os.getenv('KUCOIN_KEY') or "api_key"
    api_secret = os.getenv('KUCOIN_SECRET') or "api_secret"
    api_passphrase = os.getenv('KUCOIN_PASSPHRASE') or "api_passphrase"
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + endpoint + data

    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": api_passphrase
    }
    return headers


class Kucoin(Api):
    """
    Hides the KuCoin interface
    """

    def __init__(self, pairs, base):
        self.name = 'KuCoin'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params='', **kwargs):
        """ Hides the Kucoin exchange interface """
        compData = {}
        for pair in self.pairs:
            sym = f"{pair}-{self.base}"
            params = {"symbol": sym}
            # data_json = json.dumps(params)
            # headers = auth(an_endpoint, data_json)
            url = self.host + an_endpoint

            try:
                if pair in ['ADA', 'BCH', 'BSV', 'BTG', 'IOTA', 'XEM', 'XTZ', 'ZEC']:
                    raise NoData(f"caught {pair} in Kucoin.")
                data = await super().fetch(session, url, params=params, **kwargs)
            except KeyError as err:
                log.debug(f'{self.name}: {pair} {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{pair} {err}")
                compData[pair] = ['na', 'na']
            except TypeError as msg:
                log.error(f"{self.name} {pair} TypeError: {msg}")

            else:
                try:
                    compData[pair] = [data['data']['bestAsk'], data['data']['bestBid']]
                except KeyError:
                    log.info(f"{self.name} {pair} data: {data}")
                    compData[pair] = ['na', 'na']

        return compData
