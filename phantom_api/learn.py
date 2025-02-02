from typing import List

import requests

from .core import *

def learn(chain_ids: List[ChainId] = []) -> list:
    """
    Get useful learning resources.

    :param chain_ids: Optional, queried chains. Defaults to `[]` (all).
    :type chain_ids: `List[ChainId]`

    :return: Learning resources.
    :rtype: `list`
    """

    assert isinstance(chain_ids, list) and all(item in ChainId for item in chain_ids), f"Each value in chain_ids must be one of the following values: {', '.join([str(item) for item in ChainId])}."

    if not len(chain_ids):
        chain_ids = list(ChainId)

    chain_ids = "&chainIds[]=".join([str(item) for item in chain_ids])

    url = f"https://api.phantom.app/explore/v1/learn-grid?chainIds[]={chain_ids}&platform=extension&locale=en&appVersion=1.0.0"

    response = requests.get(url=url)

    if response.status_code != 200:
        return []
    
    data = response.json()
    data = data.get("data", [])

    return data