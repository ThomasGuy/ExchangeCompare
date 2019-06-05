""" Hides the Cex.io exchange interface """
import logging
from .api import Api, NoData

# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://cex.io/api/ticker"  # 'USD-BTC'


class Cex(Api):
    """
    Hides the Cex.io interface
    """

    def __init__(self, pairs, base):
        self.name = 'Cex.io'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params=''):
        """ Hides the Cex.io exchange interface """
        compData = {}
        for pair in self.pairs:

            url = f"{self.host}/{pair}/{self.base}"
            try:
                data = await super().fetch(session, url, params)
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
