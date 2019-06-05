""" Hides the KuCoin exchange interface """
import logging
from .api import Api, NoData

# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://api.kucoin.com/api/v1/market/orderbook/level1"  # 'ETH-BTC'


class Kucoin(Api):
    """
    Hides the KuCoin interface
    """

    def __init__(self, pairs, base):
        self.name = 'KuCoin'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params=''):
        """ Hides the Kucoin exchange interface """
        compData = {}
        for pair in self.pairs:
            params = {'symbol': f'{pair}-{self.base}'}
            url = self.host
            try:
                data = await super().fetch(session, url, params)
            except KeyError as err:
                log.debug(f'{self.name}: {pair} {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{pair} {err}")
                compData[pair] = ['na', 'na']

            else:
                try:
                    compData[pair] = [data['data']['bestAsk'], data['data']['bestBid']]
                except KeyError as err:
                    log.info(f"{self.name} {pair} data: {err}")
                    compData[pair] = ['na', 'na']

        return compData
