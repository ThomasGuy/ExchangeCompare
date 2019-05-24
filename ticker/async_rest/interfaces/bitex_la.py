""" Hides the Bitex.la interface, only on BTC """
import logging
from .api import Api, NoData


log = logging.getLogger(__name__)

host = "https://bitex.la/api/tickers/"


class Bitex_la(Api):
    """
    Hides the Bitex.la interface, only on BTC
    """

    def __init__(self, pairs):
        self.host = host
        self.pairs = pairs

    async def fetch(self, session, url=None):
        """Generate URL"""
        compData = {}
        for pair in self.pairs:
            url = self.host + pair[:3].lower() + '_' + pair[3:].lower()
            try:
                data = await super().fetch(session, url)
            except NoData as err:
                log.warning(f"No data: {err}")
            except Exception:
                raise
            else:
                attr = data['data']['attributes']
                compData[pair[:3]] = [attr['ask'], attr['bid']]

        return compData
