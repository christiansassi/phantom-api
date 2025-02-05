# Phantom Wallet API

<p align="center">
  <img src="assets/logo/logo.png" width="50%" title="logo">
</p>

## Table of contents

-   [Introduction](#introduction)
    -   [Supported Chains](#supported-chains)
-   [Functionalities](#functionalities)
    -   [Learn - learn.py](#learn---learnpy)
    -   [Quests - quests.py](#quests---questspy)
    -   [Tokens - tokens.py](#tokens---tokenspy)
    -   [Trending - trending.py](#trending---trendingpy)
    -   [Wallet - wallet.py](#wallet---walletpy)
-   [Project Structure](#project-structure)
-   [Getting Started](#getting-started)
-   [What's Missing](#whats-missing)

## Introduction

Unofficial library for interacting with the [Phantom Wallet](https://phantom.app) API.  

### Supported Chains
<div style="display: flex; gap: 10px; align-items: center;">
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="assets/solana/solana-dark.png">
        <img alt="https://phantom.app" src="assets/solana/solana-light.png" width="5%">
    </picture>
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="assets/ethereum/ethereum-dark.png">
        <img alt="https://phantom.app" src="assets/solana/ethereum-light.png" width="5%">
    </picture>
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="assets/base/base-dark.png">
        <img alt="https://phantom.app" src="assets/base/base-light.png" width="5%">
    </picture>
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="assets/sui/sui-dark.png">
        <img alt="https://phantom.app" src="assets/sui/sui-light.png" width="5%">
    </picture>
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="assets/polygon/polygon-dark.png">
        <img alt="https://phantom.app" src="assets/solana/polygon-light.png" width="5%">
    </picture>
    <picture>
        <source media="(prefers-color-scheme: dark)" srcset="assets/bitcoin/bitcoin-dark.png">
        <img alt="https://phantom.app" src="assets/bitcoin/bitcoin-light.png" width="5%">
    </picture>
</div>




## Functionalities

### Learn - <a href="phantom_api/learn.py">learn.py</a>

- `learn`: Provides useful learning resources based on queried chains.

### Quests - <a href="phantom_api/quests.py">quests.py</a>

- `get_quests`: Retrieves available quests for specific wallets.

### Tokens - <a href="phantom_api/tokens.py">tokens.py</a>

- `search_token`: Searches for tokens based on a query, chain IDs, and other filters.
- `get_token`: Retrieves information about a specific token based on its chain ID and address.
- `get_price`: Fetches the current price and 24-hour price change for a specific token.
- `get_price_history`: Retrieves price history of a token over a given time frame.

### Trending - <a href="phantom_api/trending.py">trending.py</a>

- `get_trending_tokens`: Returns a list of trending tokens based on various filters like time frame and sort criteria.
- `get_trending_dapps`: Fetches a list of trending decentralized applications (DApps).
- `get_trending_collections`: Gets trending collections based on ranking and time frame.

### Wallet - <a href="phantom_api/wallet.py">wallet.py</a>

- `get_balance`: Retrieve balances for multiple wallets.
- `get_quotes`: Retrieve quotes for a specific swap, including cross-chain swaps.
- `get_best_quote`: Retrieve the best quote for a specific swap, including cross-chain swaps.
- `get_history`: Retrieve transaction history for multiple wallets.
- `get_pending_transactions`: Retrieve pending transactions for multiple wallets.

## Project Structure

```
.
└── phantom_api
    ├── core          # Constants, enums, and core configurations
    ├── learn         # Script related to learning resources
    ├── quests        # Script to interact with quests
    ├── tokens        # Scripts for token-related functionalities
    ├── trending      # Scripts to fetch trending data (tokens, DApps, collections)
    └── wallet        # Scripts for wallet-related features
```

## Getting Started

1. Set up the workspace:

    ```bash
    git clone https://github.com/christiansassi/phantom_api
    cd phantom_api
    pip install -r requirements.txt
    ```

2. You can now use the library in your Python script by importing the necessary modules from the `phantom_api` directory.

## What's Missing

- [TODO](https://github.com/christiansassi/phantom-api/blob/64f8a6ce7ab748b544578124c95d2466c928823e/phantom_api/wallet.py#L230) Implement seamless navigation between multiple transaction pages.
- This project does not yet support all RPC-based functions, such as token swapping.
