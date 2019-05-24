import aiohttp
import asyncio
import json
import logging
from aiohttp import ClientConnectionError, ClientResponseError
from .api import Api
from ..dataStore import NoData

log = logging.getLogger(__name__)

host = "https://api.bittrex.com/api/v1.1/public/getticker"  # 'USD-BTC'
key = '55c8cd76cfbc42af822adc968eec7b49'


class Bittrex(Api):
    """
    Hides the Bittrex interface
    """

    def __init__(self, pairs):
        self.host = host
        self.pairs = pairs
        self.params = {
            'market': ''
        }

    async def fetch(self, session, params=''):
        compData = {}
        for pair in self.pairs:
            self.params['market'] = pair[3:] + '-' + pair[:3]
            url = self.host
            try:
                data = await super().fetch(session, url, self.params)
            except NoData as err:
                log.info(f"No data: {err}")
            except Exception:
                raise
            else:
                attr = data['result']
                compData[pair[:3]] = [attr['Ask'], attr['Bid']]

        return compData
