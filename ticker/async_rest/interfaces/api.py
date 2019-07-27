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
    Generic Aiohttp ClientSession, this asybcronous client fetchs exchange ticker data
    """

    async def fetch(self, session, url, params='', **kwargs):
        """Generic http request handler"""
        try:
            async with session.get(url, timeout=10, params=params,
                                   raise_for_status=True, **kwargs) as resp:
                text = await resp.text()
        except KeyError as err:
            log.info(f"ClientError: {err}")
            raise NoData
        except (ClientConnectionError, asyncio.TimeoutError) as err:
            log.info(f"ClientConnectionError: {err}")
            raise NoData
        except ClientResponseError as err:
            log.info(f"ClientResponseError: {err} {params}")
            raise NoData
        else:
            # if succesful return exchange data
            return json.loads(text)
