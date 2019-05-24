"""Generic http request handler"""
import json
import logging
import asyncio
from aiohttp import ClientConnectionError, ClientResponseError

# pylint: disable=c0103
log = logging.getLogger(__name__)


class NoData(Exception):
    """ custom exception"""


class Api:
    """
    Aiohttp ClientSession
    """

    async def fetch(self, session, url=None, params=''):
        """Generic http request handler"""
        # timeout = aiohttp.ClientTimeout(total=10)
        try:
            async with session.get(url, timeout=10, params=params) as resp:
                resp.raise_for_status()
                text = await resp.text()
        except KeyError as err:
            log.error(f"KeyError: {err}")
        except (ClientConnectionError, ClientResponseError, asyncio.TimeoutError) as err:
            raise NoData(err)
        else:
            return json.loads(text)
