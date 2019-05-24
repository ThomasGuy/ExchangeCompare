import asyncio
import aiohttp
import json
import logging

from asyncio import TimeoutError
from aiohttp import ClientConnectionError, ClientResponseError
from ..dataStore import NoData

log = logging.getLogger(__name__)


class Api:
    """
    Aiohttp ClientSession
    """

    async def fetch(self, session, url, params=''):
        timeout = aiohttp.ClientTimeout(total=10)
        try:
            async with session.get(url, timeout=timeout, params=params) as resp:
                resp.raise_for_status()
                text = await resp.text()
        except KeyError as err:
            log.error(f"KeyError: {err}")
        except ClientConnectionError as err:
            raise NoData(err)
        except ClientResponseError as err:
            # log.warning(f"ClientResonseError: {err}")
            raise NoData(err)
        except TimeoutError as err:
            raise NoData(err)

        else:
            return json.loads(text)
