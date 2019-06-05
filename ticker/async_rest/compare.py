"""Compare exchanges for each pair"""
import asyncio
import csv
import logging
from pathlib import Path

# package imports
from .interfaces import Bitfinex, Bittrex, Binance, Huobi, Kraken, Kucoin, Cex, Poloniex

pairs = ['BCH', 'EOS', 'ETC', 'ETH', 'LTC', 'NEO', 'XLM', 'XRP', 'ZEC', 'OMG',
         'IOTA', 'DASH', 'ZIL', 'ZRX']
base = 'BTC'
exchanges = ['Timestamp', 'Bitfinex', 'Bittrex', 'Binance',
             'Huboi', 'Kraken', 'Kucoin', 'Cex', 'Poloniex']

dataPath = Path('./ticker/data')
dataDir = 'bid_ask'

log = logging.getLogger(__name__)


def setupData():
    """ Initialze csv files"""
    for pair in pairs:
        filename = pair.lower() + base.lower() + '.csv'
        f_path = dataPath / dataDir / filename
        print(repr(f_path))
        with f_path.open(mode='w') as csvfile:
            filewriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            filewriter.writerow(exchanges)


class Compare:
    """Compare a pair across all exchanges"""
    setupData()
    tasks = list()
    bfx = Bitfinex(pairs, base)
    bitx = Bittrex(pairs, base)
    binn = Binance(pairs, base)
    huob = Huobi(pairs, base)
    krak = Kraken(pairs, base)
    kuco = Kucoin(pairs, base)
    cex = Cex(pairs, base)
    polo = Poloniex(pairs, base)

    def __init__(self, session):
        self.session = session

    async def addTasks(self):
        """It appears i need to regenerate tasks for each iteration...
        hmmm look into this"""
        self.tasks = list()
        self.tasks.append(asyncio.create_task(asyncio.sleep(65)))
        self.tasks.append(asyncio.create_task(
            self.bfx.fetch(self.session)))
        self.tasks.append(asyncio.create_task(
            self.bitx.fetch(self.session)))
        self.tasks.append(asyncio.create_task(
            self.binn.fetch(self.session)))
        self.tasks.append(asyncio.create_task(
            self.huob.fetch(self.session)))
        self.tasks.append(asyncio.create_task(
            self.krak.fetch(self.session)))

    async def csvData(self, timeStamp: int):
        """ grab the data from each exchange instance and save to csv """
        data = await asyncio.gather(*self.tasks)
        for pair in pairs:
            row = list()
            filename = pair.lower() + base.lower() + '.csv'
            f_path = dataPath / dataDir / filename
            row.append(timeStamp)
            for idx, item in enumerate(data[1:]):
                try:
                    ldata = item[pair][0]
                # KeyError catch exchange which only handle some pairs pair
                except KeyError as err:
                    log.debug(f"exchange: {exchanges[idx+1]} - {repr(err)}")
                else:
                    row.append(ldata)

            with f_path.open(mode='a') as csvfile:
                filewriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
                filewriter.writerow(row)

    def show(self):
        """Show me"""
