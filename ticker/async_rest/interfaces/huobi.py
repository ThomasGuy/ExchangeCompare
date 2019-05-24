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

    def __init__(self, pairs):
        self.host = host
        self.pairs = pairs

    async def fetch(self, session):
        """Trading pairs in market currency USDT"""
        compData = {}
        for pair in self.pairs:
            url = self.host
            sym = pair[:3].lower() + "usdt"
            params = {'symbol': sym}
            try:
                data = await super().fetch(session, url, params)
            except NoData as err:
                log.info(f"No data: {err}")
            except Exception:
                raise
            else:
                attr = data['tick']
                compData[pair[:3]] = [attr['ask'][0], attr['bid'][0]]

        return compData
