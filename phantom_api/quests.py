from typing import List

import requests
import json

from .core import *

def get_quests(wallet_addresses: List[tuple[ChainId, str]]) -> list:
    """
    Get available quests.

    :param wallet_addresses: Queried wallets for finding available quests.
    :type wallet_addresses: `List[tuple[ChainId, str]]`

    :return: Available quests.
    :rtype: `list`
    """

    assert isinstance(wallet_addresses, list) and all(isinstance(wallet_address, (list, tuple)) and len(wallet_address) == 2 and wallet_address[0] in ChainId and isinstance(wallet_address[1], str) for wallet_address in wallet_addresses), "Each account must consist of a valid chain ID and address."

    url = f"https://api.phantom.app/quests/v1"

    payload = {
        "platform": "extension",
        "locale": "en",
        "appVersion": "1.0.0",
        "isOptedOut": False,
        "identifiers": [],
        "selectedAccountAddresses": [
            {"chainId": str(account[0]), "address": format_address(*wallet_addresses), "resourceType": "address"}
            for account in wallet_addresses
        ]
    }

    response = requests.post(url=url, data=json.dumps(payload))

    data = response.json()
    data = data.get("quests", [])

    return data