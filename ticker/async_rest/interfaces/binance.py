""" Hides the Binance exchange interface """
import logging

from .api import Api, NoData


log = logging.getLogger(__name__)

host = "https://api.binance.com/api/v3/ticker/bookTicker"


class Binance(Api):
    """
    Hides the Binance interface, extends from class Api (api.py)
    """

    def __init__(self, pairs, base):
        self.name = 'Binance'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params='', **kwargs):
        """Trading pairs in market base currency"""
        compData = {}
        for pair in self.pairs:
            sym = pair + self.base
            params = {'symbol': sym}
            url = self.host
            try:
                if pair in ['BCH', 'BSV', 'IOTA', 'EOS', 'XTZ']:
                    raise NoData(f"caught {pair} in Binance.")
                data = await super().fetch(session, url, params, **kwargs)
            except KeyError as err:
                log.debug(f'{self.name}: {sym} {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{sym} {err}")
                compData[pair] = ['na', 'na']

            else:
                compData[pair] = [
                    float(data['askPrice']), float(data['bidPrice'])]

        return compData
