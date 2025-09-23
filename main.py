import requests
import json
import os
from datetime import datetime, timezone

# It is recommended to move these to a .env file
LINEA_TOKEN_ADDRESS = "0x1789e0043623282D5DCc7F213d703C6D8BAfBB04"
NETWORK = "linea"

BASE_URL = "https://api.geckoterminal.com/api/v2"


def get_token_pools(network, token_address):
    """Fetches all pools for a given token from the GeckoTerminal API."""
    url = f"{BASE_URL}/networks/{network}/tokens/{token_address}/pools"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.json()


def find_deepest_pool(pools_data):
    """Finds the pool with the deepest liquidity from a list of pools."""
    deepest_pool = None
    max_liquidity = -1

    for pool in pools_data["data"]:
        liquidity_usd = float(pool["attributes"]["reserve_in_usd"])
        if liquidity_usd > max_liquidity:
            max_liquidity = liquidity_usd
            deepest_pool = pool

    return deepest_pool


def get_ohlcv_data(network, pool_address):
    """Fetches OHLCV data for a given pool for the previous full day."""
    # Calculate the timestamp for midnight GMT of the current day.
    now_utc = datetime.now(timezone.utc)
    midnight_utc = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    before_timestamp = int(midnight_utc.timestamp())

    # Fetch 288 5-minute candles before midnight, which covers the entire previous day.
    url = (
        f"{BASE_URL}/networks/{network}/pools/{pool_address}/ohlcv/minute?"
        f"aggregate=5&limit=288&before_timestamp={before_timestamp}"
    )
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def calculate_vwap(ohlcv_data):
    """Calculates the Volume-Weighted Average Price (VWAP)."""
    cumulative_price_volume = 0
    cumulative_volume = 0

    for candle in ohlcv_data["data"]["attributes"]["ohlcv_list"]:
        # timestamp, open, high, low, close, volume
        high = float(candle[2])
        low = float(candle[3])
        close = float(candle[4])
        volume = float(candle[5])

        if volume > 0:
            typical_price = (high + low + close) / 3
            price_volume = typical_price * volume
            cumulative_price_volume += price_volume
            cumulative_volume += volume

    if cumulative_volume == 0:
        return 0

    return cumulative_price_volume / cumulative_volume


def main():
    """Main function to find the deepest pool and calculate VWAP."""
    print(f"Fetching pools for token {LINEA_TOKEN_ADDRESS} on {NETWORK} network...")
    try:
        pools_data = get_token_pools(NETWORK, LINEA_TOKEN_ADDRESS)
        with open("pools.json", "w") as f:
            json.dump(pools_data, f, indent=4)
        print("Saved pools data to pools.json")

        deepest_pool = find_deepest_pool(pools_data)
        if deepest_pool:
            with open("deepest_pool.json", "w") as f:
                json.dump(deepest_pool, f, indent=4)
            pool_address = deepest_pool["attributes"]["address"]
            print(f"Deepest pool found: {deepest_pool['attributes']['name']} ({pool_address})")
            print(f"Liquidity: ${float(deepest_pool['attributes']['reserve_in_usd']):,.2f}")

            print(f"Fetching OHLCV data for pool {pool_address}...")
            ohlcv_data = get_ohlcv_data(NETWORK, pool_address)
            with open("ohlcv_data.json", "w") as f:
                json.dump(ohlcv_data, f, indent=4)
            print("Saved OHLCV data to ohlcv_data.json")

            vwap = calculate_vwap(ohlcv_data)
            print(f"Daily VWAP: ${vwap:,.4f}")

        else:
            print("No pools found for the given token.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
