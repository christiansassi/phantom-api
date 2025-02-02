from enum import Enum

import requests
import re

# Retrieve the extension version from the Chrome Web Store (required for certain requests)
PHANTOM_VERSION: str = re.search(r'\\"version\\"(?:\s*):(?:\s*)\\"([\d.]+)\\"', requests.get(f"https://chromewebstore.google.com/detail/phantom/bfnaelmomeimhlpmgjnjophhpkkoljpa").text).group(1)

# Solana -> SOL
# Ethereum -> ETH
# POLYGON -> MATIC
# BASE -> ETH
# BITCOIN -> BTC
NATIVE_TOKEN: str = "nativeToken"

class ChainId(Enum):
    SOLANA = "solana:101"
    ETHEREUM = "eip155:1"
    POLYGON = "eip155:137"
    SUI = "sui:mainnet"
    BASE = "eip155:8453"

    BITCOIN = "bip122:000000000019d6689c085ae165831e93"

    # PHOENIX = "eip155:143" #! Currently unsupported
    # LINEA = "eip155:41454" #! Currently unsupported

    def __str__(self):
        return self.value

class ChartTimeFrame(Enum):
    DAY = "1D"
    WEEK = "1W"
    MONTH = "1M"
    YEAR = "YTD"
    ALL = "ALL"

    def __str__(self):
        return self.value

class RankBy(Enum):
    TOP = "top"
    TRENDING = "trending"

    def __str__(self):
        return self.value

class SearchContext(Enum):
    SWAPPER = "swapper"
    EXPLORE = "explore"

class SortBy(Enum):
    VOLUME = "volume"
    MARKET_CAP = "market-cap"
    PRICE_CHANGE = "price-change"
    PRICE = "price"
    RANK = "rank"

    def __str__(self):
        return self.value

class SortDirection(Enum):
    DESC = "desc"
    ASC = "asc"

    def __str__(self):
        return self.value

class TimeFrame(Enum):
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"

    def __str__(self):
        return self.value

class TokenTimeFrame(Enum):
    HOUR = "1h"
    DAY = "24h"
    WEEK = "7d"
    MONTH = "30d"
    HALF_YEAR = "6mo"
    YEAR = "1y"

    def __str__(self):
        return self.value

get_slip44 = lambda chain_id: {
    ChainId.SOLANA: "501",
    ChainId.ETHEREUM: "60",
    ChainId.BASE: "8453",
    ChainId.POLYGON: "966",
    ChainId.SUI: "784"
}.get(chain_id, Exception("Chain not supported!"))

format_address = lambda chain_id, address: address if chain_id in [ChainId.SOLANA, ChainId.BITCOIN] else address.lower()