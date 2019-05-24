import aiohttp
import asyncio
import json

from aiohttp import ClientResponseError, ClientConnectionError
from .api import Api
from ..dataStore import NoData

import logging

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
        compData = {}
        for pair in self.pairs:
            url = self.host + 'ticker/' + 't' + pair
            try:
                data = await super().fetch(session, url)
            except NoData as err:
                log.info(f"No data: {err}")
            except Exception:
                raise
            else:
                compData[pair[:3]] = [data[2], data[0]]

        return compData
