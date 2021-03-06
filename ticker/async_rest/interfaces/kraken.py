""" Hides the Bitex.la interface, only on BTC """
import logging
from .api import Api, NoData


log = logging.getLogger(__name__)

host = "https://api.kraken.com/0/public/Ticker"


class Kraken(Api):
    """
    Hides the Kraken interface, only on BTC, extends from class Api (api.py)
    """

    def __init__(self, pairs, base):
        self.name = 'Kraken'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params='', **kwargs):
        """Trading pairs in market base currency"""
        compData = {}
        for pair in self.pairs:
            url = self.host
            sym = pair + 'XBT'
            params = {'pair': sym}
            try:
                if pair in ['BTG', 'BSV', 'IOTA', 'NEO', 'OMG', 'TRX', 'XEM', 'ZRX']:
                    raise NoData(f"caught {pair} in Kraken")
                data = await super().fetch(session, url, params, **kwargs)
            except KeyError as err:
                log.debug(f'{self.name}: {sym}\n data: {data}\n {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{sym} {err}")
                compData[pair] = ['na', 'na']

            else:
                if not data['error']:
                    attr = data['result']
                    key = list(attr.keys())[0]
                    compData[pair] = [attr[key]['a'][0], attr[key]['b'][0]]
                else:
                    log.info(f"Kraken data error {sym} data: {data}")
                    compData[pair] = ['na', 'na']

        return compData
