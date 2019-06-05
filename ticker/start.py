import aiohttp
import asyncio
import time
import logging

from . import Compare

log = logging.getLogger(__name__)


async def start(loop):
    client = aiohttp.ClientSession(loop=loop)
    log.info("client session open")
    compare = Compare(client)
    while not client.closed:
        timestamp = int(time.time())
        try:
            await compare.addTasks()
            await compare.csvData(timestamp)
        except KeyboardInterrupt:
            print('Keyboard interrupt')
            await client.close()
            log.debug("client_session closed")
            loop.stop()
        except Exception as err:
            log.error(f"Major Error {err}", exc_info=True)
            await client.close()
            loop.stop()
            exit()
        else:
            compare.show()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop))


if __name__ == '__main__':
    main()
