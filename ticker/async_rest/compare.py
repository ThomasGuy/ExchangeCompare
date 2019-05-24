"""Compare exchanges for each pair"""
import asyncio
import csv
import os
import logging

# package imports
from .interfaces import Binance, Bittrex, Bitfinex, Huobi, Bitex_la

# pylint: disable=C0103
pairs = ['BTCUSD', 'ETHUSD', 'LTCUSD']
exchanges = ["Timestamp", "Bitfinex",
             "Bittrex", "Binance", "Huboi", "Bitex_la"]
current_dir = os.path.dirname(os.path.realpath(__file__))
package_dir = os.path.realpath(os.path.join(current_dir, os.pardir))

log = logging.getLogger(__name__)


def setupData():
    """ Initialze csv files"""
    for pair in pairs:
        path = package_dir + '\\data\\' + pair[:3].lower() + '.csv'
        with open(path, mode='w') as csvfile:
            filewriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            filewriter.writerow(exchanges)


class Compare:
    """Compare a pair across all exchanges"""
    # setupData()
    tasks = list()
    bfx = Bitfinex(pairs)
    bitx = Bittrex(pairs)
    binn = Binance(pairs)
    huob = Huobi(pairs)
    bitla = Bitex_la(['BTCUSD'])

    def __init__(self, session):
        self.session = session

    async def addTasks(self):
        """It appears i need to regenerate tasks for each iteration...
        hmmm look into this"""
        self.tasks = list()
        self.tasks.append(asyncio.create_task(asyncio.sleep(10)))
        self.tasks.append(asyncio.create_task(
            self.bfx.fetch(self.session)))
        self.tasks.append(asyncio.create_task(
            self.bitx.fetch(self.session)))
        self.tasks.append(asyncio.create_task(
            self.binn.fetch(self.session)))
        self.tasks.append(asyncio.create_task(
            self.huob.fetch(self.session)))
        self.tasks.append(asyncio.create_task(
            self.bitla.fetch(self.session)))

    async def csvData(self, timeStamp: int):
        """ grbe the data from each exchange instance and save to csv """
        data = await asyncio.gather(*self.tasks)
        path = package_dir + '\\data\\'
        for pair in pairs:
            row = list()
            filename = pair[:3].lower() + '.csv'
            row.append(timeStamp)
            for idx, item in enumerate(data[1:]):
                try:
                    ldata = item[pair[:3]][0]
                except KeyError as err:
                    log.debug(f"exchange {exchanges[idx+1]} KeyError: {err}")
                else:
                    row.append(ldata)

            with open(path + filename, mode='w') as csvfile:
                filewriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
                filewriter.writerow(row)

# pylint: enable=C0103
