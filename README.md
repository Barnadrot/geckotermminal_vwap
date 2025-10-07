# Linea Token VWAP Calculator

This script calculates the Daily Volume-Weighted Average Price (VWAP) for a given token on the Linea network using the GeckoTerminal API.

## Features

- Fetches all liquidity pools for a specified token.
- Identifies the pool with the deepest liquidity (in USD).
- Fetches 5-minute OHLCV (Open, High, Low, Close, Volume) data for the last 24 hours for the deepest pool.
- Calculates the Daily VWAP based on the OHLCV data.
- Saves the fetched pools data, the selected deepest pool, and the OHLCV data into JSON files for verification.

## Methodology 
### VWAP Calculation 
This script calculates the daily Volume-Weighted Average Price (VWAP) for a given token by analyzing its most liquid trading pool. The calculation is based on 288 five-minute OHLCV (Open, High, Low, Close, Volume) candles, covering a full 24-hour period.

### Formula
The VWAP is calculated using the following formula, which weights the price by the volume traded in each interval:
<img width="327" height="85" alt="image" src="https://github.com/user-attachments/assets/64c77655-988e-4422-8bb0-539346827b2c" />


Breakdown of the Formula
VWAP: Volume-Weighted Average Price.

n: The total number of periods (candles) considered, which is 288 for a full day of 5-minute intervals.

i: Represents each individual 5-minute period.

H<sub>i</sub>: The High price during period i.

L<sub>i</sub>: The Low price during period i.

C<sub>i</sub>: The Close price during period i.

V<sub>i</sub>: The trading Volume during period i.

The term (H_i + L_i + C_i) / 3 is the Typical Price for that period. In short, the formula calculates the total value traded (approximated by Typical Price × Volume) and divides it by the total volume traded.


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
