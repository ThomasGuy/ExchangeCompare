""" Hides the Poloniex exchange interface """
import logging
from .api import Api, NoData

# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://poloniex.com/public"  # 'USD-ETH'


class Poloniex(Api):
    """
    Hides the Poloniex interface, extends from class Api (api.py)
    """

    def __init__(self, pairs, base):
        self.name = 'Poloniex'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params='', **kwargs):
        """ Trading pairs in market base currency """
        compData = {}
        for pair in self.pairs:
            params = {'command': 'returnOrderBook',
                      'currencyPair': f'{self.base}_{pair}',
                      'depth': '1'
                      }
            url = self.host
            try:
                if pair in ['ADA', 'BCH', 'BSV', 'BTG', 'IOTA', 'TRX', 'NEO', 'XLM', 'XTZ']:
                    raise NoData(f"caught {pair} in Poloniex.")
                data = await super().fetch(session, url, params)
            except KeyError as err:
                log.debug(f'{self.name}: {pair} {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{pair} {err}")
                compData[pair] = ['na', 'na']

            else:
                try:
                    compData[pair] = [float(data['asks'][0][0]), float(data['bids'][0][0])]
                except KeyError:
                    log.info(f"{self.name} {pair} data: {data['error']}")
                    compData[pair] = ['na', 'na']

        return compData
