""" Hides the Cex.io exchange interface """
import logging
from .api import Api, NoData

# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://api.pro.coinbase.com"  # 'USD-BTC'


class CoinbasePro(Api):
    """
    Hides the Coinbase_Pro interface
    """

    def __init__(self, pairs, base):
        self.name = 'Coinbase Pro'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params='', **kwargs):
        """ Hides the Coinbase Pro exchange interface """
        compData = {}
        for pair in self.pairs:

            url = f"{self.host}/products/{pair}-{self.base}/ticker"
            try:
                if pair in ['ADA', 'BSV', 'BTG', 'DASH', 'IOTA', 'NEO',
                            'OMG', 'TRX', 'XEM', 'XTZ', 'XMR']:
                    raise NoData(f"caught {pair} in Coinbase Pro")
                data = await super().fetch(session, url, params, **kwargs)
            except KeyError as err:
                log.debug(f'{self.name}: {pair} {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{pair} {err}")
                compData[pair] = ['na', 'na']

            else:
                try:
                    compData[pair] = [data['ask'], data['bid']]
                except KeyError as err:
                    log.info(f"{self.name} {pair} data: {data['error']}")
                    compData[pair] = ['na', 'na']

        return compData
