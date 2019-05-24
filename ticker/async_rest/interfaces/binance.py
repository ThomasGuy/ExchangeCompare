""" Hides the Binance exchange interface """
import logging

from .api import Api, NoData


log = logging.getLogger(__name__)

host = "https://api.binance.com/api/v3/ticker/bookTicker"


class Binance(Api):
    """
    Hides the Binance interface
    """

    def __init__(self, pairs):
        self.host = host
        self.pairs = pairs
        self.params = {
            'symbol': ''
        }

    async def fetch(self, session, params=''):
        """Trading pairs in market currency USDT"""
        compData = {}
        for pair in self.pairs:
            self.params['symbol'] = pair + 'T'
            url = self.host
            try:
                data = await super().fetch(session, url, self.params)
            except NoData as err:
                log.info(f"No data: {err}")
            except Exception:
                raise
            else:
                compData[pair[:3]] = [
                    float(data['askPrice']), float(data['bidPrice'])]

        return compData
