from typing import List

import requests
import json

from .tokens import *
from .core import *

def get_balance(wallet_addresses: List[tuple[ChainId, str]]) -> dict:
    """
    Retrieve balances for multiple wallets.

    :param wallet_addresses: List of wallet addresses to query, where each address is paired with its corresponding ChainId.
    :type wallet_addresses: `List[tuple[ChainId, str]]`

    :return: A dictionary containing the balances for the specified wallets.
    :rtype: `dict`
    """

    assert isinstance(wallet_addresses, list), "Wallet addresses object must be a list."
    assert all(wallet_address[0] in ChainId and isinstance(wallet_address[1], str) for wallet_address in wallet_addresses), "Invalid wallet addresses format: each wallet address must be a tuple of (ChainId, str)."

    url = f"https://api.phantom.app/tokens/v1"

    payload = {"addresses": [{"chainId": str(wallet_address[0]), "address": format_address(*wallet_address)} for wallet_address in wallet_addresses]}

    response = requests.post(url=url, data=json.dumps(payload))

    return response.json()

def get_quotes(from_chain_id: ChainId, from_token: str, from_taker: str, to_chain_id: ChainId, to_token: str, to_taker: str, sell_amount: float | int, auto_slippage: bool = True, slippage: float | int = 0) -> dict:
    """
    Retrieve quotes for a specific swap, including cross-chain swaps.

    :param from_chain_id: The chain ID of the initial chain for the swap.
    :type from_chain_id: `ChainId`

    :param from_token: The token to swap from. If the token is native to the selected blockchain (e.g., SOL for Solana), use `NATIVE_TOKEN` as the address.
    :type from_token: `str`

    :param from_taker: The wallet address initiating the swap.
    :type from_taker: `str`

    :param to_chain_id: The chain ID of the destination chain for the swap.
    :type to_chain_id: `ChainId`

    :param to_token: The token to swap to. If the token is native to the selected blockchain (e.g., SOL for Solana), use `NATIVE_TOKEN` as the address.
    :type to_token: `str`

    :param to_taker: The wallet address receiving the swapped tokens.
    :type to_taker: `str`

    :param sell_amount: The amount of the `from_token` to swap.
    :type sell_amount: `float` or `int`

    :param auto_slippage: Whether to automatically set slippage to ensure the transaction succeeds. Defaults to `True`.
    :type auto_slippage: `bool`

    :param slippage: The slippage tolerance for the swap. Ignored if `auto_slippage` is enabled. Defaults to `0`.
    :type slippage: `float`

    :return: A dictionary containing quotes for the requested swap.
    :rtype: `dict`
    """

    assert from_chain_id in ChainId, f"from_chain_id must be one of the following values: {', '.join([str(item) for item in ChainId])}."
    assert isinstance(from_token, str), "Invalid from_token."
    assert isinstance(from_taker, str), "Invalid from_taker."

    assert from_chain_id in ChainId, f"to_chain_id must be one of the following values: {', '.join([str(item) for item in ChainId])}."
    assert isinstance(from_token, str), "Invalid to_token."
    assert isinstance(from_taker, str), "Invalid to_taker."

    assert isinstance(sell_amount, (float, int)), "Invalid sell_amount."
    assert sell_amount > 0, "sell_amount must be greater than 0."

    if not auto_slippage:
        assert isinstance(slippage, (float, int)), "Invalid slippage."
        assert slippage >= 0, "slippage must be a positive value."

    from_token = get_token(chain_id=from_chain_id, address=from_token)

    url = f"https://api.phantom.app/swap/v2/quotes"

    if not from_token.get("address"):
        sell_token = {
            "chainId": str(from_chain_id),
            "slip44": get_slip44(chain_id=from_chain_id),
            "resourceType": NATIVE_TOKEN
        }
    
    else:
        sell_token = {
            "chainId": str(from_chain_id),
            "address": from_token["address"],
            "resourceType": "address"
        }
    
    if to_token == NATIVE_TOKEN:
        buy_token = {
            "chainId": str(to_chain_id),
            "slip44": get_slip44(chain_id=to_chain_id),
            "resourceType": NATIVE_TOKEN
        }
    
    else:
        buy_token = {
            "chainId": str(to_chain_id),
            "address": to_token["address"],
            "resourceType": "address"
        }

    payload = {
        "sellToken": sell_token,

        "buyToken": buy_token,

        "taker": {
            "chainId": str(from_chain_id),
            "address": format_address(chain_id=from_chain_id, address=from_taker),
            "resourceType": "address"
        },

        "exactOut": False,
        "sellAmount": str(sell_amount * pow(10, from_token["decimals"])).split(".")[0],
        "autoSlippage": auto_slippage,
    }

    if not auto_slippage:
        payload["slippageTolerance"] = slippage

    if from_chain_id != to_chain_id:
        payload["takerDestination"] = {
            "chainId": str(to_chain_id),
            "address": format_address(chain_id=to_chain_id, address=to_taker),
            "resourceType": "address"
        }
    
        payload["refuel"] = 1
        payload["ignoreRefuelFailures"] = True

    response = requests.post(url=url, headers={"x-phantom-version": PHANTOM_VERSION}, data=json.dumps(payload))

    return response.json()

def get_best_quote(from_chain_id: ChainId, from_token: str, from_taker: str, to_chain_id: ChainId, to_token: str, to_taker: str, sell_amount: float | int, auto_slippage: bool = True, slippage: float | int = 0) -> dict:
    """
    Retrieve the best quote for a specific swap, including cross-chain swaps.

    :param from_chain_id: The chain ID of the initial chain for the swap.
    :type from_chain_id: `ChainId`

    :param from_token: The token to swap from.
    :type from_token: `str`

    :param from_taker: The wallet address initiating the swap.
    :type from_taker: `str`

    :param to_chain_id: The chain ID of the destination chain for the swap.
    :type to_chain_id: `ChainId`

    :param to_token: The token to swap to.
    :type to_token: `str`

    :param to_taker: The wallet address receiving the swapped tokens.
    :type to_taker: `str`

    :param sell_amount: The amount of the `from_token` to swap.
    :type sell_amount: `float` or `int`

    :param auto_slippage: Whether to automatically set slippage to ensure the transaction succeeds. Defaults to `True`.
    :type auto_slippage: `bool`

    :param slippage: The slippage tolerance for the swap. Ignored if `auto_slippage` is enabled. Defaults to `0`.
    :type slippage: `float` or `int`

    :return: A dictionary containing the best quote for the requested swap.
    :rtype: `dict`
    """

    quotes = get_quotes(
        from_chain_id=from_chain_id, 
        from_token=from_token, 
        from_taker=from_taker, 
        to_chain_id=to_chain_id, 
        to_token=to_token, 
        to_taker=to_taker, 
        sell_amount=sell_amount, 
        auto_slippage=auto_slippage, 
        slippage=slippage
    )

    if len(quotes["quotes"]):
        quotes["quotes"] = [max(quotes["quotes"], key=lambda x: float(x["buyAmount"]))]

    return quotes

def get_history(wallet_addresses: List[tuple[ChainId, str]], all_results: bool = True) -> list:
    """
    Retrieve transaction history for multiple wallets.

    :param wallet_addresses: List of wallet addresses to query, where each address is paired with its corresponding ChainId.
    :type wallet_addresses: `List[tuple[ChainId, str]]`

    :param all_results: Whether to fetch all transaction history pages or only the first page.
    :type all_results: `bool`. Defaults to `True`

    :return: A dictionary containing the transaction history for the specified wallets.
    :rtype: `dict`
    """

    assert isinstance(wallet_addresses, list), "Wallet addresses object must be a list."
    assert all(wallet_address[0] in ChainId and isinstance(wallet_address[1], str) for wallet_address in wallet_addresses), "Invalid wallet addresses format: each wallet address must be a tuple of (ChainId, str)."

    base_url = f"https://api.phantom.app/history/v2"

    payload = {"accounts": [{"chainId": str(wallet_address[0]), "address": format_address(*wallet_address)} for wallet_address in wallet_addresses]}
    payload["isSpam"] = False

    url = base_url
    history = []

    while True:
        response = requests.post(url=url, data=json.dumps(payload))
        results = response.json()

        history.extend(results["results"])
        return history
    
        # TODO Implement seamless navigation between multiple transaction pages
        if results["next"] is None:
            break

        url = f"{base_url}?next={results['next']}" # next or cursor?

    return history

def get_pending_transactions(wallet_addresses: List[tuple[ChainId, str]]) -> list:
    """
    Retrieve pending transactions for multiple wallets.

    :param wallet_addresses: List of wallet addresses to query, where each address is paired with its corresponding ChainId.
    :type wallet_addresses: `List[tuple[ChainId, str]]`

    :return: A dictionary containing the pending transactions for the specified wallets.
    :rtype: `dict`
    """

    assert isinstance(wallet_addresses, list), "Wallet addresses object must be a list."
    assert all(wallet_address[0] in ChainId and isinstance(wallet_address[1], str) for wallet_address in wallet_addresses), "Invalid wallet addresses format: each wallet address must be a tuple of (ChainId, str)."

    url = f"https://api.phantom.app/pending-transactions/v1"

    payload = {"addresses": [{"chainId": str(wallet_address[0]), "address": format_address(*wallet_address), "resourceType": "address"} for wallet_address in wallet_addresses]}

    response = requests.post(url=url, data=json.dumps(payload))
    
    return response.json()["transactions"]
