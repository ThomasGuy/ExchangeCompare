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

    async def fetch(self, session, url, params='', **kwargs):
        """Generic http request handler"""
        try:
            async with session.get(url, timeout=10, params=params,
                                   raise_for_status=True, **kwargs) as resp:
                # if resp.status >= 400:
                #     log.error(f"status:{resp.status} {resp.url}")
                text = await resp.text()
        # except TypeError as msg:
        #     log.error(f"{params} {msg}")
        #     raise NoData
        except KeyError as err:
            log.info(f"ClientError: {err}")
            raise NoData
        except (ClientConnectionError, ClientResponseError, asyncio.TimeoutError) as err:
            log.info(f"ClientError: {err}")
            raise NoData
        else:
            return json.loads(text)
