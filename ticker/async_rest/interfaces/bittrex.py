""" Hides the Bittrex exchange interface """
import logging
from .api import Api, NoData

# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://api.bittrex.com/api/v1.1/public/getticker"  # 'USD-BTC'
key = '55c8cd76cfbc42af822adc968eec7b49'


class Bittrex(Api):
    """
    Hides the Bittrex interface
    """

    def __init__(self, pairs, base):
        self.name = 'Bittrex'
        self.host = host
        self.pairs = pairs
        self.base = base

    async def fetch(self, session, url=None, params='', **kwargs):
        """ Hides the Bittrex exchange interface """
        compData = {}
        for pair in self.pairs:
            sym = self.base + '-' + pair
            params = {'market': sym}
            url = self.host
            try:
                if pair in ['BTG', 'EOS', 'IOTA', 'XTZ']:
                    raise NoData(f"caught {pair} in Bittrex.")
                data = await super().fetch(session, url, params=params, **kwargs)
            except KeyError as err:
                log.debug(f'{self.name}: {pair} {repr(err)}')
            except NoData as err:
                log.info(f"{self.name} No data:{sym} {err}")
                compData[pair] = ['na', 'na']

            else:
                attr = data['result']
                if attr:
                    compData[pair] = [attr['Ask'], attr['Bid']]
                else:
                    log.info(f"{self.name} {sym} data: {data}")
                    compData[pair] = ['na', 'na']

        return compData
