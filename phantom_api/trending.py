from typing import List

import requests

from .core import *

def get_trending_tokens(timeframe: TokenTimeFrame = TokenTimeFrame.DAY, sort_by: SortBy = SortBy.RANK, sort_direction: SortDirection = SortDirection.ASC, limit: int = 100, chain_ids: List[ChainId] = []) -> list:
    """
    Get trending tokens.

    :param timeframe: Optional, time frame for trending ranking. Defaults to `TokenTimeFrame.DAY`.
    :type timeframe: `TokenTimeFrame`

    :param sort_by: Optional, sorting criteria. Defaults to `SortBy.RANK`.
    :type sort_by: `SortBy`

    :param sort_direction: Optional, sort direction. Defaults to `SortDirection.ASC`.
    :type sort_direction: `SortDirection`

    :param limit: Optional, maximum number of results. Defaults to `100`.
    :type limit: `int`

    :param chain_ids: Optional list of queried chains. Defaults to `[]` (all).
    :type chain_ids: `List[ChainId]`

    :return: A list of trending tokens.
    :rtype: `list`
    """

    assert timeframe in TokenTimeFrame, f"timeframe must be one of the following values: {', '.join([str(item) for item in TokenTimeFrame])}."
    assert sort_by in SortBy, f"sort_by must be one of the following values: {', '.join([str(item) for item in SortBy])}."
    assert sort_direction in SortDirection, f"sort_direction must be one of the following values: {', '.join([str(item) for item in SortDirection])}."
    assert isinstance(limit, int) and 1 <= limit <= 100, "limit must be between 1 and 100."
    assert isinstance(chain_ids, list) and all(item in ChainId for item in chain_ids), f"Each value in chain_ids must be one of the following: {', '.join([str(item) for item in ChainId])}."

    if not len(chain_ids):
        chain_ids = list(ChainId)

    chain_ids = "&chainIds[]=".join([str(item) for item in ChainId])
    
    url = f"https://api.phantom.app/explore/v2/trending-tokens?timeFrame={str(timeframe)}&sortBy={str(sort_by)}&sortDirection={str(sort_direction)}&limit={limit}&chainIds[]={chain_ids}"

    response = requests.get(url=url)

    if response.status_code != 200:
        return []

    data = response.json()
    data = data.get("results", [])

    return data

def get_trending_dapps(limit: int = 50, rank_by: RankBy = RankBy.TRENDING, timeframe: TimeFrame = TimeFrame.DAY, chain_ids: List[ChainId] = []) -> list:
    """
    Get trending DApps.

    :param limit: Optional, results limit. Defaults to `50`.
    :type limit: `int`

    :param rank_by: Optional, ranking criteria. Defaults to `RankBy.TRENDING`.
    :type rank_by: `RankBy`

    :param timeframe: Optional, time frame for trending ranking. Defaults to `TimeFrame.DAY`.
    :type timeframe: `TimeFrame`

    :param chain_ids: Optional, queried chains. Defaults to `[]` (all).
    :type chain_ids: `List[ChainId]`

    :return: Trending DApps.
    :rtype: `list`
    """

    assert isinstance(limit, int) and 1 <= limit <= 50, "limit must not be lower than 1 or greater than 50."
    assert rank_by in RankBy, f"rank_by must be one of the following values: {', '.join([str(item) for item in RankBy])}."
    assert timeframe in TimeFrame, f"timeframe must be one of the following values: {', '.join([str(item) for item in TimeFrame])}."
    assert isinstance(chain_ids, list) and all(item in ChainId for item in chain_ids), f"Each value in chain_ids must be one of the following values: {', '.join([str(item) for item in ChainId])}."

    if not len(chain_ids):
        chain_ids = list(ChainId)

    chain_ids = "&chainIds[]=".join([str(item) for item in chain_ids])

    url = f"https://api.phantom.app/explore/v1/trending-dapps?limit={limit}&rankBy={str(rank_by)}&timeframe={str(timeframe)}&chainIds[]={chain_ids}&rankAlgo=default&platform=extension&locale=en&appVersion=1.0.0"

    response = requests.get(url=url)

    if response.status_code != 200:
        return []
    
    data = response.json()
    data = data.get("data", [])

    return data

def get_trending_collections(limit: int = 50, rank_by: RankBy = RankBy.TRENDING, timeframe: TimeFrame = TimeFrame.DAY, chain_ids: List[ChainId] = []) -> list:
    """
    Get trending collections.

    :param limit: Optional, results limit. Defaults to `50`.
    :type limit: `int`

    :param rank_by: Optional, ranking criteria. Defaults to `RankBy.TRENDING`.
    :type rank_by: `RankBy`

    :param timeframe: Optional, time frame for trending ranking. Defaults to `TimeFrame.DAY`.
    :type timeframe: `TimeFrame`

    :param chain_ids: Optional, queried chains. Defaults to `[]` (all).
    :type chain_ids: `List[ChainId]`

    :return: Trending collections.
    :rtype: `list`
    """

    assert isinstance(limit, int) and 1 <= limit <= 50, "limit must not be lower than 1 or greater than 50."
    assert rank_by in RankBy, f"rank_by must be one of the following values: {', '.join([str(item) for item in RankBy])}."
    assert timeframe in TimeFrame, f"timeframe must be one of the following values: {', '.join([str(item) for item in TimeFrame])}."
    assert isinstance(chain_ids, list) and all(item in ChainId for item in chain_ids), f"Each value in chain_ids must be one of the following values: {', '.join([str(item) for item in ChainId])}."

    if not len(chain_ids):
        chain_ids = [ChainId.SOLANA, ChainId.ETHEREUM, ChainId.POLYGON, ChainId.BITCOIN]

    chain_ids = f"&chainIds[]=".join([str(item) for item in chain_ids])

    url = f"https://api.phantom.app/explore/v1/trending-collections?limit={limit}&rankBy={str(rank_by)}&timeframe={str(timeframe)}&chainIds[]={chain_ids}&rankAlgo=default&platform=extension&locale=en&appVersion=1.0.0"

    response = requests.get(url=url)

    if response.status_code != 200:
        return []
    
    data = response.json()
    data = data.get("data", [])

    return data