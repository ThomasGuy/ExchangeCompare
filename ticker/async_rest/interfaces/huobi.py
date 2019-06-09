""" Hides the Huboi exchange interface """
import logging
from .api import Api, NoData

# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://api.huobi.pro/market/detail/merged"
key = '7b641835-fa60a6e4-ez2xc4vb6n-f5f99'


class Huobi(Api):
    """
    Hides the Huobi interface
    """

    def __init__(self, pairs, base):
        self.name = 'Huobi'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params='', **kwargs):
        """Trading pairs in market currency USDT"""
        compData = {}
        for pair in self.pairs:
            url = self.host
            sym = pair.lower() + self.base.lower()
            params = {'symbol': sym}
            try:
                data = await super().fetch(session, url, params, **kwargs)
                attr = data['tick']
            except KeyError as err:
                log.debug(f'{self.name}: {sym}\n data:{data} {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{sym} {err}")
                compData[pair] = ['na', 'na']

            else:
                compData[pair] = [attr['ask'][0], attr['bid'][0]]

        return compData
