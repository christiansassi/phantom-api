from typing import List

import requests

from .core import *

def search_token(query: str, chain_ids: List[ChainId] = [], page_size: int = 100, search_context: SearchContext = SearchContext.EXPLORE, all_results: bool = True) -> list:
    """
    Search for tokens.

    :param query: Search query.
    :type query: `str`

    :param chain_ids: Optional list of queried chains. Defaults to `[]` (all).
    :type chain_ids: `List[ChainId]`

    :param page_size: Optional number of results per page. Defaults to `100`.
    :type page_size: `int`

    :param search_context: Optional search context. Defaults to `SearchContext.EXPLORE`.
    :type search_context: `SearchContext`

    :param all_results: Optional flag to load all result pages. Defaults to `True`.
    :type all_results: `bool`

    :return: A list of found tokens.
    :rtype: `list`
    """
    
    assert isinstance(query, str) and len(query), "query cannot be empty."
    assert isinstance(page_size, int) and 1 <= page_size <= 100, "page_size must be between 1 and 100."
    assert isinstance(chain_ids, list) and all(item in ChainId for item in chain_ids), f"Each value in chain_ids must be one of the following: {', '.join([str(item) for item in ChainId])}."
    assert search_context in SearchContext, f"search_context must be one of the following values: {', '.join([str(item) for item in SearchContext])}."

    if not len(chain_ids):
        chain_ids = list(ChainId)

    chain_ids = ",".join([str(item) for item in chain_ids])

    if all_results:
        page_size = 100

    all_results = []

    base_url = f"https://api.phantom.app/search/v1?query={query}&chainIds={chain_ids}&pageSize={page_size}&searchContext={str(search_context)}&platform=extension&searchTypes=fungible"
    url = base_url

    while True:

        response = requests.get(url=url)

        data = response.json()

        has_more = data.get("hasMore", False)

        results = data.get("results", [])
        all_results.extend(results)

        if not has_more or not all_results:
            break
        
        url = f"{base_url}&cursor={data['nextCursor']}"

    return all_results

def get_token(chain_id: ChainId, address: str) -> dict:
    """
    Get token information.

    :param chain_id: The blockchain of the token.
    :type chain_id: `ChainId`

    :param address: The token's address. If the token is native to the selected blockchain (e.g., SOL for Solana), use `NATIVE_TOKEN` as the address.
    :type address: `str`

    :return: A dictionary containing the token's information.
    :rtype: `dict`
    """

    assert chain_id in ChainId, f"chain_id must be one of the following values: {', '.join([str(item) for item in ChainId])}."
    assert isinstance(address, str), "Invalid address."

    if address == NATIVE_TOKEN:
        url = f"https://api.phantom.app/tokens/v1/{str(chain_id)}/{NATIVE_TOKEN}/{get_slip44(chain_id=chain_id)}"
    else:
        url = f"https://api.phantom.app/tokens/v1/{str(chain_id)}/address/{address}"

    response = requests.get(url=url)

    if response.status_code != 200:
        return {}
    
    data = response.json()
    data = data.get("data", {})

    del data["chain"]

    return data

def get_price(chain_id: ChainId, address: str) -> dict:
    """
    Get token price and 24h price change.

    :param chain_id: The blockchain of the token.
    :type chain_id: `ChainId`

    :param address: The token's address. If the token is native to the selected blockchain (e.g., SOL for Solana), use `NATIVE_TOKEN` as the address.
    :type address: `str`

    :return: A dictionary containing the token's price and 24h price change.
    :rtype: `dict`
    """

    assert chain_id in ChainId, f"chain_id must be one of the following values: {', '.join([str(item) for item in ChainId])}."
    assert isinstance(address, str), "Invalid address."

    if address == NATIVE_TOKEN:
        url = f"https://api.phantom.app/price/v1/{str(chain_id)}/{NATIVE_TOKEN}/{get_slip44(chain_id=chain_id)}"
    else:
        url = f"https://api.phantom.app/price/v1/{str(chain_id)}/address/{address}"
    
    response = requests.get(url=url)

    if response.status_code != 200:
        return {}
    
    data = response.json()
    
    return data

def get_price_history(chain_id: ChainId, address: str, timeframe: ChartTimeFrame) -> list:
    """
    Get token price history for a given time frame.

    :param chain_id: The blockchain of the token.
    :type chain_id: `ChainId`

    :param address: The token's address. If the token is native to the selected blockchain (e.g., SOL for Solana), use `NATIVE_TOKEN` as the address.
    :type address: `str`

    :param timeframe: The time frame for price history.
    :type timeframe: `ChartTimeFrame`

    :return: A list of price history for the token.
    :rtype: `list`
    """

    assert chain_id in ChainId, f"chain_id must be one of the following values: {', '.join([str(item) for item in ChainId])}."
    assert isinstance(address, str), "Invalid address."
    assert timeframe in ChartTimeFrame, f"timeframe must be one of the following values: {', '.join([str(item) for item in ChartTimeFrame])}."

    if address == NATIVE_TOKEN:
        url = f"https://api.phantom.app/price-history/v1?token={str(chain_id)}/{NATIVE_TOKEN}:{get_slip44(chain_id=chain_id)}&type={str(timeframe)}"
    else:
        url = f"https://api.phantom.app/price-history/v1?token={str(chain_id)}/address:{address}&type={str(timeframe)}"
    
    response = requests.get(url=url)

    if response.status_code != 200:
        return []
    
    data = response.json()
    data = data.get("history", [])

    return data