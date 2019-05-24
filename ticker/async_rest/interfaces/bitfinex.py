""" Hides the Bitfinex exchange interface """
import logging

from .api import Api, NoData


# pylint: disable=c0103
log = logging.getLogger(__name__)

host = "https://api-pub.bitfinex.com/v2/"
host2 = "https://api-pub.bitfinex.com/v2/tickers?symbols="


class Bitfinex(Api):
    """
    Hides the Bitfinex interface
    """

    def __init__(self, pairs):
        self.host = host
        self.pairs = pairs

    async def fetch(self, session):
        """ request http """
        comp_data = {}
        for pair in self.pairs:
            url = self.host + 'ticker/' + 't' + pair
            try:
                data = await super().fetch(session, url)
            except NoData as err:
                log.info(f"No data: {err}")
            except Exception:
                raise
            else:
                comp_data[pair[:3]] = [data[2], data[0]]

        return comp_data
