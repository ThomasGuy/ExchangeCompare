from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Pair:
    """
    Ticker data for a pair i.e. 'BTCUSD' across all exchanges holds
    a list of tuples ('ask', 'bid') attributes
    """
    symbol: str
    bitfinex: List[Tuple] = field(default_factory=list)     # bitfinex
    bittrex: List[Tuple] = field(default_factory=list)    # Bittrex
    binance: List[Tuple] = field(default_factory=list)    # Binance
    huobi: List[Tuple] = field(default_factory=list)      # Huobi
    bitex_la: List[Tuple] = field(default_factory=list)      # Huobi


class NoData(Exception):
    pass
