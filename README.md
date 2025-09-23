# Linea Token VWAP Calculator

This script calculates the Daily Volume-Weighted Average Price (VWAP) for a given token on the Linea network using the GeckoTerminal API.

## Features

- Fetches all liquidity pools for a specified token.
- Identifies the pool with the deepest liquidity (in USD).
- Fetches 5-minute OHLCV (Open, High, Low, Close, Volume) data for the last 24 hours for the deepest pool.
- Calculates the Daily VWAP based on the OHLCV data.
- Saves the fetched pools data, the selected deepest pool, and the OHLCV data into JSON files for verification.

## How to Use

1. **Clone the repository.**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script:**
   ```bash
   python main.py
   ```

## Output

The script will print the following information to the console:
- The name and address of the deepest liquidity pool.
- The total liquidity of that pool in USD.
- The calculated Daily VWAP for the token.

It will also create the following JSON files in the project directory:
- `pools.json`: A list of all pools for the token.
- `deepest_pool.json`: The data for the pool with the highest liquidity.
- `ohlcv_data.json`: The OHLCV data used for the VWAP calculation.

## API Rate Limits

Please be aware of the GeckoTerminal API rate limits. The free tier allows for 30 calls per minute. This script makes two calls per execution, which is well within the limits. However, if you plan to extend the script to run more frequently or for multiple tokens, you may need to consider a more advanced plan or implement rate limiting in your code.
