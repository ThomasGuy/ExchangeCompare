"""Kick off"""
import time
import logging
import asyncio
from pathlib import Path

import aiohttp

from ticker import Compare, setupData

log = logging.getLogger(__name__)


async def start(loop, dataDir):
    """Contiuous loop collect exchange data"""
    print('Press   Ctrl + c   to exit (and wait a few seconds'
          ' for asyncronous code to complete)\nRunning...')
    client = aiohttp.ClientSession(loop=loop)
    log.info("client session open")
    compare = Compare(client, dataDir)
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


def newDir():
    """Sort out our data storage directory"""
    dataDir = input(" enter data directory ")
    # print("Is this correct")
    if Path(f'./ticker/data/{dataDir}').exists():
        answer = input(
            '\nThis directory already exists. Do you want to overwrite it ?'
            '\n yes, no, exit, or append to it...    ')
        if answer[0] in ['y', 'n', 'e', 'Y', 'N', 'E', 'a', 'A']:
            if answer[0] in ['y', 'Y']:
                print(f'\n{dataDir} directory cleaned')
                setupData(dataDir=dataDir)
                return dataDir
            elif answer[0] in ['a', 'A']:
                print(f'\nappending to {dataDir}')
                return dataDir
            elif answer[0] in ['N', 'n']:
                print('\nTry another directory name...')
                newDir()
            else:
                print('Exiting Exchange Ticker Compare')
                exit()
        else:
            print('Wrong answer mate!')
            exit()
    else:
        print('New directory created')
        setupData(dataDir=dataDir)
        return dataDir


def main():
    """Start here"""
    dataDir = newDir()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop, dataDir))
