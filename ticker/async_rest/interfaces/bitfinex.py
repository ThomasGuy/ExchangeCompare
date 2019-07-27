""" Hides the Bitfinex exchange interface """
import logging

from .api import Api, NoData


# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://api-pub.bitfinex.com/v2/tickers/"


class Bitfinex(Api):
    """
    Hides the Bitfinex interface, extends from class Api (api.py)
    """

    def __init__(self, pairs, base):
        self.name = 'Bitfinex'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params='', **kwargs):
        """ Trading pairs in market base currency"""
        comp_data = {}
        for pair in self.pairs:
            if pair == 'IOTA':
                sym = 'tIOT'
            elif pair == 'DASH':
                sym = 'tDSH'
            elif pair == 'BCH':
                sym = 'tBAB'
            else:
                sym = 't' + pair

            url = self.host
            params = {'symbols': sym + self.base}
            try:
                if pair in ['ADA', 'XEM']:      # try resrtrict 429 too many requests
                    raise NoData(f"caught {pair} in Bitfinex")
                data = await super().fetch(session, url, params=params, **kwargs)
            except KeyError as err:
                log.warning(f'{self.name}: {pair} {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{pair} {err}")
                comp_data[pair] = ['na', 'na']

            else:
                try:
                    comp_data[pair] = [data[0][3], data[0][1]]    # ['Ask' , 'Bid']
                except IndexError:
                    log.info(f"{self.name} {pair} data: {data}")
                    comp_data[pair] = ['na', 'na']
        return comp_data
