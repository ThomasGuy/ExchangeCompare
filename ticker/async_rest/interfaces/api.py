"""Generic http request handler"""
import json
import logging
import asyncio
from aiohttp import ClientConnectionError, ClientResponseError

log = logging.getLogger(__name__)


class NoData(Exception):
    """ custom exception"""


class Api:
    """
    Generic Aiohttp ClientSession
    """

    async def fetch(self, session, url, params):
        """Generic http request handler"""
        try:
            async with session.get(url, timeout=10, params=params) as resp:
                resp.raise_for_status()
                text = await resp.text()

        except KeyError as err:
            raise
        except (ClientConnectionError, ClientResponseError, asyncio.TimeoutError) as err:
            raise NoData(err)
        else:
            return json.loads(text)
