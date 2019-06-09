"""Import all exchange interfaces"""
from .binance import Binance
from .bitfinex import Bitfinex
from .bittrex import Bittrex
from .huobi import Huobi
from .kraken import Kraken
from .cex import Cex
from .kucoin import Kucoin, auth
from .poloniex import Poloniex
from .coinbase_pro import CoinbasePro

NAME = 'interfaces'
