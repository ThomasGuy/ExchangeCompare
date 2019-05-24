from dataclasses import dataclass
import asyncio
import csv
import os

# package imports
from .interfaces import Binance, Bittrex, Bitfinex, Huobi, Bitex_la
# from ticker import package_dir

pairs = ['BTCUSD', 'ETHUSD', 'LTCUSD']
exchanges = ["Timestamp", "Bitfinex",
             "Bittrex", "Binance", "Huboi", "Bitex_la"]
current_dir = os.path.dirname(os.path.realpath(__file__))
package_dir = os.path.realpath(os.path.join(current_dir, os.pardir))


def setupData():
    for pair in pairs:
        path = package_dir + '\\data\\' + pair[:3].lower() + '.csv'
        with open(path, mode='w') as csvfile:
            filewriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            filewriter.writerow(exchanges)


class Compare:
    """Compare a pair across all exchanges"""
    # setupData()
    tasks = []
    bfx = Bitfinex(pairs)
    bitx = Bittrex(pairs)
    binn = Binance(pairs)
    huob = Huobi(pairs)
    bitla = Bitex_la(pairs)

    def __init__(self, session):
        self.session = session

    async def addTasks(self):
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
        data = await asyncio.gather(*self.tasks)
        for pair in pairs:
            row = list()
            path = package_dir + '\\data\\mk2\\' + pair[:3].lower() + '.csv'
            row.append(timeStamp)
            for item in data[1:]:
                try:
                    ldata = item[pair[:3]]
                except KeyError:
                    pass
                else:
                    row += ldata

            with open(path, mode='a') as csvfile:
                filewriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
                filewriter.writerow(row)

    async def show(self):
        # print()
        # for val in self.data.values():
        #     print(
        #         f"{val.symbol}:\n Bitfinex: {val.bitfinex[-1:]}\n Bittrex: {val.bittrex[-1:]}\n"
        #         f" Binance: {val.binance[-1:]}\n Huobi: {val.huobi[-1:]}\n Bitex_la: {val.bitex_la[-1:]}\n")
        pass
