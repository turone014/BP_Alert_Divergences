# -*- coding: utf-8 -*-


#1hr BP long with 3-5 crosses

import ccxt
import pandas as pd
import requests
import time
import os
from ta.momentum import RSIIndicator
from ta.trend import MACD
from datetime import datetime
from zoneinfo import ZoneInfo  # For Python 3.9 and above

# Configuration
DISCORD_WEBHOOK_URL = os.getenv("ONE_HOUR_BP_LONG_WEBHOOK")  # Replace with your Discord webhook URL
#SYMBOLS = ['1INCH-USDT-SWAP','AAVE-USDT-SWAP','ACE-USDT-SWAP','ACH-USDT-SWAP','ACT-USDT-SWAP','ADA-USDT-SWAP','AEVO-USDT-SWAP','AGLD-USDT-SWAP','AI16Z-USDT-SWAP','AIDOGE-USDT-SWAP','AIXBT-USDT-SWAP','ALCH-USDT-SWAP','ALGO-USDT-SWAP','ALPHA-USDT-SWAP','ANIME-USDT-SWAP','APE-USDT-SWAP','API3-USDT-SWAP','APT-USDT-SWAP','ARB-USDT-SWAP','ARC-USDT-SWAP','ARKM-USDT-SWAP','AR-USDT-SWAP','ATH-USDT-SWAP','ATOM-USDT-SWAP','AUCTION-USDT-SWAP','A-USDT-SWAP','AVAAI-USDT-SWAP','AVAX-USDT-SWAP','AXS-USDT-SWAP','BABY-USDT-SWAP','BADGER-USDT-SWAP','BAL-USDT-SWAP','BAND-USDT-SWAP','BAT-USDT-SWAP','BCH-USDT-SWAP','BERA-USDT-SWAP','BICO-USDT-SWAP','BIGTIME-USDT-SWAP','BIO-USDT-SWAP','BLUR-USDT-SWAP','BNB-USDT-SWAP','BNT-USDT-SWAP','BOME-USDT-SWAP','BONK-USDT-SWAP','BRETT-USDT-SWAP','BTC-USDT-SWAP','BTC-USDT-SWAP','CATI-USDT-SWAP','CAT-USDT-SWAP','CELO-USDT-SWAP','CETUS-USDT-SWAP','CFX-USDT-SWAP','CHZ-USDT-SWAP','COMP-USDT-SWAP','COOKIE-USDT-SWAP','CORE-USDT-SWAP','CRO-USDT-SWAP','CRV-USDT-SWAP','CSPR-USDT-SWAP','CTC-USDT-SWAP','CVC-USDT-SWAP','CVX-USDT-SWAP','DEGEN-USDT-SWAP','DGB-USDT-SWAP','DOGE-USDT-SWAP','DOGS-USDT-SWAP','DOG-USDT-SWAP','DOOD-USDT-SWAP','DOT-USDT-SWAP','DUCK-USDT-SWAP','DYDX-USDT-SWAP','EGLD-USDT-SWAP','EIGEN-USDT-SWAP','ENJ-USDT-SWAP','ENS-USDT-SWAP','ETC-USDT-SWAP','ETHFI-USDT-SWAP','ETH-USDT-SWAP','ETHW-USDT-SWAP','FARTCOIN-USDT-SWAP','FIL-USDT-SWAP','FLM-USDT-SWAP','FLOKI-USDT-SWAP','FLOW-USDT-SWAP','FXS-USDT-SWAP','GALA-USDT-SWAP','GAS-USDT-SWAP','GLM-USDT-SWAP','GMT-USDT-SWAP','GMX-USDT-SWAP','GOAT-USDT-SWAP','GODS-USDT-SWAP','GPS-USDT-SWAP','GRASS-USDT-SWAP','GRIFFAIN-USDT-SWAP','GRT-USDT-SWAP','HBAR-USDT-SWAP','HMSTR-USDT-SWAP','HOME-USDT-SWAP','HUMA-USDT-SWAP','HYPE-USDT-SWAP','ICP-USDT-SWAP','ICX-USDT-SWAP','ID-USDT-SWAP','IMX-USDT-SWAP','INIT-USDT-SWAP','INJ-USDT-SWAP','IOST-USDT-SWAP','IOTA-USDT-SWAP','IP-USDT-SWAP','JELLYJELLY-USDT-SWAP','JOE-USDT-SWAP','JST-USDT-SWAP','JTO-USDT-SWAP','JUP-USDT-SWAP','KAITO-USDT-SWAP','KMNO-USDT-SWAP','KNC-USDT-SWAP','KSM-USDT-SWAP','LAUNCHCOIN-USDT-SWAP','LA-USDT-SWAP','LAYER-USDT-SWAP','LDO-USDT-SWAP','LINK-USDT-SWAP','LOOKS-USDT-SWAP','LPT-USDT-SWAP','LQTY-USDT-SWAP','LRC-USDT-SWAP','LSK-USDT-SWAP','LTC-USDT-SWAP','LUNA-USDT-SWAP','LUNC-USDT-SWAP','MAGIC-USDT-SWAP','MAJOR-USDT-SWAP','MANA-USDT-SWAP','MASK-USDT-SWAP','MEME-USDT-SWAP','MERL-USDT-SWAP','METIS-USDT-SWAP','ME-USDT-SWAP','MEW-USDT-SWAP','MINA-USDT-SWAP','MKR-USDT-SWAP','MOODENG-USDT-SWAP','MORPHO-USDT-SWAP','MOVE-USDT-SWAP','MUBARAK-USDT-SWAP','NC-USDT-SWAP','NEAR-USDT-SWAP','NEIROETH-USDT-SWAP','NEIRO-USDT-SWAP','NEO-USDT-SWAP','NIL-USDT-SWAP','NMR-USDT-SWAP','NOT-USDT-SWAP','NXPC-USDT-SWAP','OL-USDT-SWAP','OM-USDT-SWAP','ONDO-USDT-SWAP','ONE-USDT-SWAP','ONT-USDT-SWAP','OP-USDT-SWAP','ORBS-USDT-SWAP','ORDI-USDT-SWAP','PARTI-USDT-SWAP','PENGU-USDT-SWAP','PEOPLE-USDT-SWAP','PEPE-USDT-SWAP','PERP-USDT-SWAP','PIPPIN-USDT-SWAP','PI-USDT-SWAP','PLUME-USDT-SWAP','PNUT-USDT-SWAP','POL-USDT-SWAP','POPCAT-USDT-SWAP','PRCL-USDT-SWAP','PROMPT-USDT-SWAP','PYTH-USDT-SWAP','QTUM-USDT-SWAP','RAY-USDT-SWAP','RDNT-USDT-SWAP','RENDER-USDT-SWAP','RESOLV-USDT-SWAP','RSR-USDT-SWAP','RVN-USDT-SWAP','SAND-USDT-SWAP','SATS-USDT-SWAP','SCR-USDT-SWAP','SHELL-USDT-SWAP','SHIB-USDT-SWAP','SIGN-USDT-SWAP','SLERF-USDT-SWAP','SLP-USDT-SWAP','SNX-USDT-SWAP','SOL-USDT-SWAP','SOLV-USDT-SWAP','SONIC-USDT-SWAP','SOON-USDT-SWAP','SOPH-USDT-SWAP','SSV-USDT-SWAP','STORJ-USDT-SWAP','STRK-USDT-SWAP','STX-USDT-SWAP','SUI-USDT-SWAP','S-USDT-SWAP','SUSHI-USDT-SWAP','SWARMS-USDT-SWAP','TAO-USDT-SWAP','THETA-USDT-SWAP','TIA-USDT-SWAP','TNSR-USDT-SWAP','TON-USDT-SWAP','TRB-USDT-SWAP','TRUMP-USDT-SWAP','TRX-USDT-SWAP','TURBO-USDT-SWAP','T-USDT-SWAP','UMA-USDT-SWAP','UNI-USDT-SWAP','USDC-USDT-SWAP','USTC-USDT-SWAP','UXLINK-USDT-SWAP','VANA-USDT-SWAP','VINE-USDT-SWAP','VIRTUAL-USDT-SWAP','WAL-USDT-SWAP','WAXP-USDT-SWAP','WCT-USDT-SWAP','WIF-USDT-SWAP','WLD-USDT-SWAP','WOO-USDT-SWAP','W-USDT-SWAP','XAUT-USDT-SWAP','XCH-USDT-SWAP','XLM-USDT-SWAP','XRP-USDT-SWAP','XTZ-USDT-SWAP','YFI-USDT-SWAP','YGG-USDT-SWAP','ZENT-USDT-SWAP','ZEREBRO-USDT-SWAP','ZETA-USDT-SWAP','ZIL-USDT-SWAP','ZK-USDT-SWAP','ZRO-USDT-SWAP','ZRX-USDT-SWAP']  # Add your desired trading pairs
from crypto_pairs import SYMBOLS

RSI_PERIOD = 25
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

RSI_OVERSOLD_LOW = 30
RSI_OVERSOLD_HIGH = 38

TIMEFRAME_RSI = '15m'
TIMEFRAME_MACD = '5m'
CANDLE_LIMIT = 150

exchange = ccxt.okx({
    'options': {'defaultType': 'swap'}  # Ensure we're using Futures
})

def fetch_candles(symbol, timeframe, limit):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if not ohlcv:
            print(f"[ERROR] No data received for {symbol} on {timeframe} timeframe.")
            return None
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {symbol} on {timeframe} timeframe: {e}")
        return None

def add_indicators(df):
    if df.empty:
        return df
    df['rsi'] = RSIIndicator(close=df['close'], window=RSI_PERIOD).rsi()
    macd = MACD(close=df['close'], window_fast=MACD_FAST, window_slow=MACD_SLOW, window_sign=MACD_SIGNAL)
    df['macd_line'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def is_rsi_oversold(value):
    return RSI_OVERSOLD_LOW <= value <= RSI_OVERSOLD_HIGH

def detect_bullish_macd_divergence(df, num_crosses):
    crosses = []
    macd_line = df['macd_line']
    macd_signal = df['macd_signal']

    for i in range(1, len(df)):
        prev_line = macd_line.iloc[i - 1]
        prev_signal = macd_signal.iloc[i - 1]
        curr_line = macd_line.iloc[i]
        curr_signal = macd_signal.iloc[i]

        if (prev_line < prev_signal and curr_line > curr_signal) or (prev_line > prev_signal and curr_line < curr_signal):
            crosses.append((df.index[i], curr_line, df['low'].iloc[i]))

    if len(crosses) < num_crosses:
        return False

    recent_crosses = crosses[-num_crosses:]
    prices = [price for _, _, price in recent_crosses]
    macds = [macd for _, macd, _ in recent_crosses]

    return prices[-1] < prices[0] and macds[-1] > macds[0]

def send_discord_alert(symbol):
    now = datetime.now(ZoneInfo("Asia/Manila")).strftime('%Y-%m-%d %H:%M %Z')
    message = f"""🔔 **1HR BP - 5 minutes Right Hand**🟢

**Symbol**: {symbol}
**Time**: {now}
===============================
"""
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print(f"[ALERT SENT] {symbol} at {now}")
    else:
        print(f"[ERROR] Failed to send alert for {symbol}: {response.status_code}")

def check_symbol(symbol):
    print(f"Checking {symbol}...")

    # 15M RSI check
    df_rsi = fetch_candles(symbol, TIMEFRAME_RSI, CANDLE_LIMIT)
    if df_rsi is None or df_rsi.empty:
        print(f"[ERROR] No data or empty DataFrame for {symbol} on 15M timeframe.")
        return
    df_rsi = add_indicators(df_rsi)

    if df_rsi['rsi'].isna().all():
        print(f"[ERROR] RSI data is not available for {symbol}.")
        return

    latest_rsi = df_rsi['rsi'].dropna().iloc[-1]

    if not is_rsi_oversold(latest_rsi):
        print(f"[{symbol}] 15M RSI not in oversold range: {latest_rsi:.2f}")
        return

    # 5M MACD divergence check
    df_macd = fetch_candles(symbol, TIMEFRAME_MACD, CANDLE_LIMIT)
    if df_macd is None or df_macd.empty:
        print(f"[ERROR] No data or empty DataFrame for {symbol} on 5M timeframe.")
        return
    df_macd = add_indicators(df_macd)

    if df_macd['macd_line'].isna().all() or df_macd['macd_signal'].isna().all():
        print(f"[ERROR] MACD data is not available for {symbol}.")
        return

    # Attempt with 3 crosses
    if detect_bullish_macd_divergence(df_macd, 3):
        send_discord_alert(symbol)
        time.sleep(1)
    # If not found, attempt with 4 crosses
    elif detect_bullish_macd_divergence(df_macd, 4):
        send_discord_alert(symbol)
        time.sleep(1)
    # If still not found, attempt with 5 crosses
    elif detect_bullish_macd_divergence(df_macd, 5):
        send_discord_alert(symbol)
        time.sleep(1)

def main():
    for symbol in SYMBOLS:
        check_symbol(symbol)

if __name__ == "__main__":
    main()


#=====================================================================================
#1HR BP Short Setups


import ccxt
import pandas as pd
import requests
import os
from ta.momentum import RSIIndicator
from ta.trend import MACD
from datetime import datetime
from zoneinfo import ZoneInfo

# Configuration
DISCORD_WEBHOOK_URL = os.getenv("ONE_HOUR_BP_SHORT_WEBHOOK") # Replace with your actual webhook
#SYMBOLS = ['1INCH-USDT-SWAP','AAVE-USDT-SWAP','ACE-USDT-SWAP','ACH-USDT-SWAP','ACT-USDT-SWAP','ADA-USDT-SWAP','AEVO-USDT-SWAP','AGLD-USDT-SWAP','AI16Z-USDT-SWAP','AIDOGE-USDT-SWAP','AIXBT-USDT-SWAP','ALCH-USDT-SWAP','ALGO-USDT-SWAP','ALPHA-USDT-SWAP','ANIME-USDT-SWAP','APE-USDT-SWAP','API3-USDT-SWAP','APT-USDT-SWAP','ARB-USDT-SWAP','ARC-USDT-SWAP','ARKM-USDT-SWAP','AR-USDT-SWAP','ATH-USDT-SWAP','ATOM-USDT-SWAP','AUCTION-USDT-SWAP','A-USDT-SWAP','AVAAI-USDT-SWAP','AVAX-USDT-SWAP','AXS-USDT-SWAP','BABY-USDT-SWAP','BADGER-USDT-SWAP','BAL-USDT-SWAP','BAND-USDT-SWAP','BAT-USDT-SWAP','BCH-USDT-SWAP','BERA-USDT-SWAP','BICO-USDT-SWAP','BIGTIME-USDT-SWAP','BIO-USDT-SWAP','BLUR-USDT-SWAP','BNB-USDT-SWAP','BNT-USDT-SWAP','BOME-USDT-SWAP','BONK-USDT-SWAP','BRETT-USDT-SWAP','BTC-USDT-SWAP','BTC-USDT-SWAP','CATI-USDT-SWAP','CAT-USDT-SWAP','CELO-USDT-SWAP','CETUS-USDT-SWAP','CFX-USDT-SWAP','CHZ-USDT-SWAP','COMP-USDT-SWAP','COOKIE-USDT-SWAP','CORE-USDT-SWAP','CRO-USDT-SWAP','CRV-USDT-SWAP','CSPR-USDT-SWAP','CTC-USDT-SWAP','CVC-USDT-SWAP','CVX-USDT-SWAP','DEGEN-USDT-SWAP','DGB-USDT-SWAP','DOGE-USDT-SWAP','DOGS-USDT-SWAP','DOG-USDT-SWAP','DOOD-USDT-SWAP','DOT-USDT-SWAP','DUCK-USDT-SWAP','DYDX-USDT-SWAP','EGLD-USDT-SWAP','EIGEN-USDT-SWAP','ENJ-USDT-SWAP','ENS-USDT-SWAP','ETC-USDT-SWAP','ETHFI-USDT-SWAP','ETH-USDT-SWAP','ETHW-USDT-SWAP','FARTCOIN-USDT-SWAP','FIL-USDT-SWAP','FLM-USDT-SWAP','FLOKI-USDT-SWAP','FLOW-USDT-SWAP','FXS-USDT-SWAP','GALA-USDT-SWAP','GAS-USDT-SWAP','GLM-USDT-SWAP','GMT-USDT-SWAP','GMX-USDT-SWAP','GOAT-USDT-SWAP','GODS-USDT-SWAP','GPS-USDT-SWAP','GRASS-USDT-SWAP','GRIFFAIN-USDT-SWAP','GRT-USDT-SWAP','HBAR-USDT-SWAP','HMSTR-USDT-SWAP','HOME-USDT-SWAP','HUMA-USDT-SWAP','HYPE-USDT-SWAP','ICP-USDT-SWAP','ICX-USDT-SWAP','ID-USDT-SWAP','IMX-USDT-SWAP','INIT-USDT-SWAP','INJ-USDT-SWAP','IOST-USDT-SWAP','IOTA-USDT-SWAP','IP-USDT-SWAP','JELLYJELLY-USDT-SWAP','JOE-USDT-SWAP','JST-USDT-SWAP','JTO-USDT-SWAP','JUP-USDT-SWAP','KAITO-USDT-SWAP','KMNO-USDT-SWAP','KNC-USDT-SWAP','KSM-USDT-SWAP','LAUNCHCOIN-USDT-SWAP','LA-USDT-SWAP','LAYER-USDT-SWAP','LDO-USDT-SWAP','LINK-USDT-SWAP','LOOKS-USDT-SWAP','LPT-USDT-SWAP','LQTY-USDT-SWAP','LRC-USDT-SWAP','LSK-USDT-SWAP','LTC-USDT-SWAP','LUNA-USDT-SWAP','LUNC-USDT-SWAP','MAGIC-USDT-SWAP','MAJOR-USDT-SWAP','MANA-USDT-SWAP','MASK-USDT-SWAP','MEME-USDT-SWAP','MERL-USDT-SWAP','METIS-USDT-SWAP','ME-USDT-SWAP','MEW-USDT-SWAP','MINA-USDT-SWAP','MKR-USDT-SWAP','MOODENG-USDT-SWAP','MORPHO-USDT-SWAP','MOVE-USDT-SWAP','MUBARAK-USDT-SWAP','NC-USDT-SWAP','NEAR-USDT-SWAP','NEIROETH-USDT-SWAP','NEIRO-USDT-SWAP','NEO-USDT-SWAP','NIL-USDT-SWAP','NMR-USDT-SWAP','NOT-USDT-SWAP','NXPC-USDT-SWAP','OL-USDT-SWAP','OM-USDT-SWAP','ONDO-USDT-SWAP','ONE-USDT-SWAP','ONT-USDT-SWAP','OP-USDT-SWAP','ORBS-USDT-SWAP','ORDI-USDT-SWAP','PARTI-USDT-SWAP','PENGU-USDT-SWAP','PEOPLE-USDT-SWAP','PEPE-USDT-SWAP','PERP-USDT-SWAP','PIPPIN-USDT-SWAP','PI-USDT-SWAP','PLUME-USDT-SWAP','PNUT-USDT-SWAP','POL-USDT-SWAP','POPCAT-USDT-SWAP','PRCL-USDT-SWAP','PROMPT-USDT-SWAP','PYTH-USDT-SWAP','QTUM-USDT-SWAP','RAY-USDT-SWAP','RDNT-USDT-SWAP','RENDER-USDT-SWAP','RESOLV-USDT-SWAP','RSR-USDT-SWAP','RVN-USDT-SWAP','SAND-USDT-SWAP','SATS-USDT-SWAP','SCR-USDT-SWAP','SHELL-USDT-SWAP','SHIB-USDT-SWAP','SIGN-USDT-SWAP','SLERF-USDT-SWAP','SLP-USDT-SWAP','SNX-USDT-SWAP','SOL-USDT-SWAP','SOLV-USDT-SWAP','SONIC-USDT-SWAP','SOON-USDT-SWAP','SOPH-USDT-SWAP','SSV-USDT-SWAP','STORJ-USDT-SWAP','STRK-USDT-SWAP','STX-USDT-SWAP','SUI-USDT-SWAP','S-USDT-SWAP','SUSHI-USDT-SWAP','SWARMS-USDT-SWAP','TAO-USDT-SWAP','THETA-USDT-SWAP','TIA-USDT-SWAP','TNSR-USDT-SWAP','TON-USDT-SWAP','TRB-USDT-SWAP','TRUMP-USDT-SWAP','TRX-USDT-SWAP','TURBO-USDT-SWAP','T-USDT-SWAP','UMA-USDT-SWAP','UNI-USDT-SWAP','USDC-USDT-SWAP','USTC-USDT-SWAP','UXLINK-USDT-SWAP','VANA-USDT-SWAP','VINE-USDT-SWAP','VIRTUAL-USDT-SWAP','WAL-USDT-SWAP','WAXP-USDT-SWAP','WCT-USDT-SWAP','WIF-USDT-SWAP','WLD-USDT-SWAP','WOO-USDT-SWAP','W-USDT-SWAP','XAUT-USDT-SWAP','XCH-USDT-SWAP','XLM-USDT-SWAP','XRP-USDT-SWAP','XTZ-USDT-SWAP','YFI-USDT-SWAP','YGG-USDT-SWAP','ZENT-USDT-SWAP','ZEREBRO-USDT-SWAP','ZETA-USDT-SWAP','ZIL-USDT-SWAP','ZK-USDT-SWAP','ZRO-USDT-SWAP','ZRX-USDT-SWAP']  # Add your desired trading pairs
from crypto_pairs import SYMBOLS

RSI_PERIOD = 30
RSI_OVERBOUGHT_LOW = 60
RSI_OVERBOUGHT_HIGH = 70

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

TIMEFRAME_RSI = '15m'
TIMEFRAME_MACD = '5m'
CANDLE_LIMIT = 150

exchange = ccxt.okx({'options': {'defaultType': 'swap'}})

def fetch_candles(symbol, timeframe, limit):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if not ohlcv:
            return None
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] {symbol} ({timeframe}): {e}")
        return None

def add_indicators(df):
    if df.empty:
        return df
    df['rsi'] = RSIIndicator(close=df['close'], window=RSI_PERIOD).rsi()
    macd = MACD(close=df['close'], window_fast=MACD_FAST, window_slow=MACD_SLOW, window_sign=MACD_SIGNAL)
    df['macd_line'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def is_rsi_overbought(value):
    return RSI_OVERBOUGHT_LOW <= value <= RSI_OVERBOUGHT_HIGH

def find_macd_crosses(df):
    crosses = []
    for i in range(1, len(df)):
        prev_macd = df['macd_line'].iloc[i-1]
        prev_signal = df['macd_signal'].iloc[i-1]
        curr_macd = df['macd_line'].iloc[i]
        curr_signal = df['macd_signal'].iloc[i]
        if (prev_macd < prev_signal and curr_macd > curr_signal) or (prev_macd > prev_signal and curr_macd < curr_signal):
            crosses.append((df.index[i], df['macd_line'].iloc[i], df['high'].iloc[i]))
    return crosses

def detect_bearish_divergence(df, num_crosses):
    crosses = find_macd_crosses(df)
    if len(crosses) < num_crosses:
        return False
    recent = crosses[-num_crosses:]
    prices = [price for _, _, price in recent]
    macds = [macd for _, macd, _ in recent]
    return prices[-1] > prices[0] and macds[-1] < macds[0]

def send_discord_alert(symbol):
    now = datetime.now(ZoneInfo("Asia/Manila")).strftime('%Y-%m-%d %H:%M:%S %Z')
    message = f"""🔔 **1HR BP - 5 minutes Left Hand**🔴

**Symbol**: {symbol}
**Time**: {now}
==============================="""
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print(f"[ALERT SENT] {symbol} at {now}")
    else:
        print(f"[ERROR] Discord alert failed for {symbol}: {response.status_code}")

def check_symbol(symbol):
    print(f"Checking {symbol}...")

    df_rsi = fetch_candles(symbol, TIMEFRAME_RSI, CANDLE_LIMIT)
    if df_rsi is None or df_rsi.empty:
        return
    df_rsi = add_indicators(df_rsi)
    if df_rsi['rsi'].isna().all():
        return
    latest_rsi = df_rsi['rsi'].dropna().iloc[-1]
    if not is_rsi_overbought(latest_rsi):
        return

    df_macd = fetch_candles(symbol, TIMEFRAME_MACD, CANDLE_LIMIT)
    if df_macd is None or df_macd.empty:
        return
    df_macd = add_indicators(df_macd)
    if df_macd['macd_line'].isna().all() or df_macd['macd_signal'].isna().all():
        return

    for num in range(3, 10):
        if detect_bearish_divergence(df_macd, num):
            send_discord_alert(symbol)
            break

if __name__ == "__main__":
    for symbol in SYMBOLS:
        check_symbol(symbol)

#============================================================================

#4hr bp long with 3-5 crosses

import ccxt
import pandas as pd
import requests
import os
import time
from ta.momentum import RSIIndicator
from ta.trend import MACD
from datetime import datetime
from zoneinfo import ZoneInfo

# Configuration
DISCORD_WEBHOOK_URL = os.getenv("FOUR_HOUR_BP_LONG_WEBHOOK")  # Replace with your actual webhook
#SYMBOLS = ['1INCH-USDT-SWAP','AAVE-USDT-SWAP','ACE-USDT-SWAP','ACH-USDT-SWAP','ACT-USDT-SWAP','ADA-USDT-SWAP','AEVO-USDT-SWAP','AGLD-USDT-SWAP','AI16Z-USDT-SWAP','AIDOGE-USDT-SWAP','AIXBT-USDT-SWAP','ALCH-USDT-SWAP','ALGO-USDT-SWAP','ALPHA-USDT-SWAP','ANIME-USDT-SWAP','APE-USDT-SWAP','API3-USDT-SWAP','APT-USDT-SWAP','ARB-USDT-SWAP','ARC-USDT-SWAP','ARKM-USDT-SWAP','AR-USDT-SWAP','ATH-USDT-SWAP','ATOM-USDT-SWAP','AUCTION-USDT-SWAP','A-USDT-SWAP','AVAAI-USDT-SWAP','AVAX-USDT-SWAP','AXS-USDT-SWAP','BABY-USDT-SWAP','BADGER-USDT-SWAP','BAL-USDT-SWAP','BAND-USDT-SWAP','BAT-USDT-SWAP','BCH-USDT-SWAP','BERA-USDT-SWAP','BICO-USDT-SWAP','BIGTIME-USDT-SWAP','BIO-USDT-SWAP','BLUR-USDT-SWAP','BNB-USDT-SWAP','BNT-USDT-SWAP','BOME-USDT-SWAP','BONK-USDT-SWAP','BRETT-USDT-SWAP','BTC-USDT-SWAP','BTC-USDT-SWAP','CATI-USDT-SWAP','CAT-USDT-SWAP','CELO-USDT-SWAP','CETUS-USDT-SWAP','CFX-USDT-SWAP','CHZ-USDT-SWAP','COMP-USDT-SWAP','COOKIE-USDT-SWAP','CORE-USDT-SWAP','CRO-USDT-SWAP','CRV-USDT-SWAP','CSPR-USDT-SWAP','CTC-USDT-SWAP','CVC-USDT-SWAP','CVX-USDT-SWAP','DEGEN-USDT-SWAP','DGB-USDT-SWAP','DOGE-USDT-SWAP','DOGS-USDT-SWAP','DOG-USDT-SWAP','DOOD-USDT-SWAP','DOT-USDT-SWAP','DUCK-USDT-SWAP','DYDX-USDT-SWAP','EGLD-USDT-SWAP','EIGEN-USDT-SWAP','ENJ-USDT-SWAP','ENS-USDT-SWAP','ETC-USDT-SWAP','ETHFI-USDT-SWAP','ETH-USDT-SWAP','ETHW-USDT-SWAP','FARTCOIN-USDT-SWAP','FIL-USDT-SWAP','FLM-USDT-SWAP','FLOKI-USDT-SWAP','FLOW-USDT-SWAP','FXS-USDT-SWAP','GALA-USDT-SWAP','GAS-USDT-SWAP','GLM-USDT-SWAP','GMT-USDT-SWAP','GMX-USDT-SWAP','GOAT-USDT-SWAP','GODS-USDT-SWAP','GPS-USDT-SWAP','GRASS-USDT-SWAP','GRIFFAIN-USDT-SWAP','GRT-USDT-SWAP','HBAR-USDT-SWAP','HMSTR-USDT-SWAP','HOME-USDT-SWAP','HUMA-USDT-SWAP','HYPE-USDT-SWAP','ICP-USDT-SWAP','ICX-USDT-SWAP','ID-USDT-SWAP','IMX-USDT-SWAP','INIT-USDT-SWAP','INJ-USDT-SWAP','IOST-USDT-SWAP','IOTA-USDT-SWAP','IP-USDT-SWAP','JELLYJELLY-USDT-SWAP','JOE-USDT-SWAP','JST-USDT-SWAP','JTO-USDT-SWAP','JUP-USDT-SWAP','KAITO-USDT-SWAP','KMNO-USDT-SWAP','KNC-USDT-SWAP','KSM-USDT-SWAP','LAUNCHCOIN-USDT-SWAP','LA-USDT-SWAP','LAYER-USDT-SWAP','LDO-USDT-SWAP','LINK-USDT-SWAP','LOOKS-USDT-SWAP','LPT-USDT-SWAP','LQTY-USDT-SWAP','LRC-USDT-SWAP','LSK-USDT-SWAP','LTC-USDT-SWAP','LUNA-USDT-SWAP','LUNC-USDT-SWAP','MAGIC-USDT-SWAP','MAJOR-USDT-SWAP','MANA-USDT-SWAP','MASK-USDT-SWAP','MEME-USDT-SWAP','MERL-USDT-SWAP','METIS-USDT-SWAP','ME-USDT-SWAP','MEW-USDT-SWAP','MINA-USDT-SWAP','MKR-USDT-SWAP','MOODENG-USDT-SWAP','MORPHO-USDT-SWAP','MOVE-USDT-SWAP','MUBARAK-USDT-SWAP','NC-USDT-SWAP','NEAR-USDT-SWAP','NEIROETH-USDT-SWAP','NEIRO-USDT-SWAP','NEO-USDT-SWAP','NIL-USDT-SWAP','NMR-USDT-SWAP','NOT-USDT-SWAP','NXPC-USDT-SWAP','OL-USDT-SWAP','OM-USDT-SWAP','ONDO-USDT-SWAP','ONE-USDT-SWAP','ONT-USDT-SWAP','OP-USDT-SWAP','ORBS-USDT-SWAP','ORDI-USDT-SWAP','PARTI-USDT-SWAP','PENGU-USDT-SWAP','PEOPLE-USDT-SWAP','PEPE-USDT-SWAP','PERP-USDT-SWAP','PIPPIN-USDT-SWAP','PI-USDT-SWAP','PLUME-USDT-SWAP','PNUT-USDT-SWAP','POL-USDT-SWAP','POPCAT-USDT-SWAP','PRCL-USDT-SWAP','PROMPT-USDT-SWAP','PYTH-USDT-SWAP','QTUM-USDT-SWAP','RAY-USDT-SWAP','RDNT-USDT-SWAP','RENDER-USDT-SWAP','RESOLV-USDT-SWAP','RSR-USDT-SWAP','RVN-USDT-SWAP','SAND-USDT-SWAP','SATS-USDT-SWAP','SCR-USDT-SWAP','SHELL-USDT-SWAP','SHIB-USDT-SWAP','SIGN-USDT-SWAP','SLERF-USDT-SWAP','SLP-USDT-SWAP','SNX-USDT-SWAP','SOL-USDT-SWAP','SOLV-USDT-SWAP','SONIC-USDT-SWAP','SOON-USDT-SWAP','SOPH-USDT-SWAP','SSV-USDT-SWAP','STORJ-USDT-SWAP','STRK-USDT-SWAP','STX-USDT-SWAP','SUI-USDT-SWAP','S-USDT-SWAP','SUSHI-USDT-SWAP','SWARMS-USDT-SWAP','TAO-USDT-SWAP','THETA-USDT-SWAP','TIA-USDT-SWAP','TNSR-USDT-SWAP','TON-USDT-SWAP','TRB-USDT-SWAP','TRUMP-USDT-SWAP','TRX-USDT-SWAP','TURBO-USDT-SWAP','T-USDT-SWAP','UMA-USDT-SWAP','UNI-USDT-SWAP','USDC-USDT-SWAP','USTC-USDT-SWAP','UXLINK-USDT-SWAP','VANA-USDT-SWAP','VINE-USDT-SWAP','VIRTUAL-USDT-SWAP','WAL-USDT-SWAP','WAXP-USDT-SWAP','WCT-USDT-SWAP','WIF-USDT-SWAP','WLD-USDT-SWAP','WOO-USDT-SWAP','W-USDT-SWAP','XAUT-USDT-SWAP','XCH-USDT-SWAP','XLM-USDT-SWAP','XRP-USDT-SWAP','XTZ-USDT-SWAP','YFI-USDT-SWAP','YGG-USDT-SWAP','ZENT-USDT-SWAP','ZEREBRO-USDT-SWAP','ZETA-USDT-SWAP','ZIL-USDT-SWAP','ZK-USDT-SWAP','ZRO-USDT-SWAP','ZRX-USDT-SWAP']  # Add your desired trading pairs
from crypto_pairs import SYMBOLS

RSI_PERIOD = 30
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

RSI_OVERSOLD_LOW = 25
RSI_OVERSOLD_HIGH = 42

TIMEFRAME_RSI = '1h'
TIMEFRAME_MACD = '15m'
CANDLE_LIMIT = 150

exchange = ccxt.okx({'options': {'defaultType': 'swap'}})

def fetch_candles(symbol, timeframe, limit):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if not ohlcv:
            print(f"[ERROR] No data received for {symbol} on {timeframe} timeframe.")
            return None
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {symbol}: {e}")
        return None

def add_indicators(df):
    if df.empty:
        return df
    df['rsi'] = RSIIndicator(close=df['close'], window=RSI_PERIOD).rsi()
    macd = MACD(close=df['close'], window_fast=MACD_FAST, window_slow=MACD_SLOW, window_sign=MACD_SIGNAL)
    df['macd_line'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def is_rsi_oversold(value):
    return RSI_OVERSOLD_LOW <= value <= RSI_OVERSOLD_HIGH

def detect_bullish_macd_divergence(df, num_crosses):
    crosses = []
    macd_line = df['macd_line']
    macd_signal = df['macd_signal']
    lows = df['low']

    for i in range(1, len(df)):
        prev_line = macd_line.iloc[i - 1]
        prev_signal = macd_signal.iloc[i - 1]
        curr_line = macd_line.iloc[i]
        curr_signal = macd_signal.iloc[i]

        if (prev_line < prev_signal and curr_line > curr_signal) or (prev_line > prev_signal and curr_line < curr_signal):
            crosses.append((df.index[i], curr_line, lows.iloc[i]))

    if len(crosses) < num_crosses:
        return False

    selected = crosses[-num_crosses:]
    prices = [price for _, _, price in selected]
    macds = [macd for _, macd, _ in selected]

    return prices[-1] < prices[0] and macds[-1] > macds[0]

def send_discord_alert(symbol):
    now = datetime.now(ZoneInfo("Asia/Manila")).strftime('%Y-%m-%d %H:%M %Z')
    message = f"""🔔 **4HR BP - 15 minutes Right Hand** 🟢

**Symbol**: {symbol}
**Time**: {now}
==============================="""
    response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
    if response.status_code == 204:
        print(f"[ALERT SENT] {symbol} at {now}")
    else:
        print(f"[ERROR] Failed to send alert for {symbol}: {response.status_code}")

def check_symbol(symbol):
    print(f"Checking {symbol}...")

    df_rsi = fetch_candles(symbol, TIMEFRAME_RSI, CANDLE_LIMIT)
    if df_rsi is None or df_rsi.empty:
        print(f"[ERROR] No RSI data for {symbol}.")
        return

    df_rsi = add_indicators(df_rsi)
    if df_rsi['rsi'].isna().all():
        print(f"[ERROR] RSI not available for {symbol}.")
        return

    latest_rsi = df_rsi['rsi'].dropna().iloc[-1]
    if not is_rsi_oversold(latest_rsi):
        print(f"[{symbol}] 1H RSI not oversold: {latest_rsi:.2f}")
        return

    df_macd = fetch_candles(symbol, TIMEFRAME_MACD, CANDLE_LIMIT)
    if df_macd is None or df_macd.empty:
        print(f"[ERROR] No MACD data for {symbol}.")
        return

    df_macd = add_indicators(df_macd)
    if df_macd['macd_line'].isna().all() or df_macd['macd_signal'].isna().all():
        print(f"[ERROR] MACD not available for {symbol}.")
        return

    for crosses in [3, 4, 5]:
        if detect_bullish_macd_divergence(df_macd, crosses):
            send_discord_alert(symbol)
            time.sleep(1)
            return
    print(f"[{symbol}] No bullish divergence detected in last 3-5 MACD crosses.")

if __name__ == "__main__":
    for symbol in SYMBOLS:
        check_symbol(symbol)

#==================================================================

#4HR BP short setup with 3-9 cross

import ccxt
import pandas as pd
import requests
import time
import os
from ta.momentum import RSIIndicator
from ta.trend import MACD
from datetime import datetime
from zoneinfo import ZoneInfo

# Configuration
DISCORD_WEBHOOK_URL = os.getenv("FOUR_HOUR_BP_SHORT_WEBHOOK")  # Replace with your webhook
#SYMBOLS = ['1INCH-USDT-SWAP','AAVE-USDT-SWAP','ACE-USDT-SWAP','ACH-USDT-SWAP','ACT-USDT-SWAP','ADA-USDT-SWAP','AEVO-USDT-SWAP','AGLD-USDT-SWAP','AI16Z-USDT-SWAP','AIDOGE-USDT-SWAP','AIXBT-USDT-SWAP','ALCH-USDT-SWAP','ALGO-USDT-SWAP','ALPHA-USDT-SWAP','ANIME-USDT-SWAP','APE-USDT-SWAP','API3-USDT-SWAP','APT-USDT-SWAP','ARB-USDT-SWAP','ARC-USDT-SWAP','ARKM-USDT-SWAP','AR-USDT-SWAP','ATH-USDT-SWAP','ATOM-USDT-SWAP','AUCTION-USDT-SWAP','A-USDT-SWAP','AVAAI-USDT-SWAP','AVAX-USDT-SWAP','AXS-USDT-SWAP','BABY-USDT-SWAP','BADGER-USDT-SWAP','BAL-USDT-SWAP','BAND-USDT-SWAP','BAT-USDT-SWAP','BCH-USDT-SWAP','BERA-USDT-SWAP','BICO-USDT-SWAP','BIGTIME-USDT-SWAP','BIO-USDT-SWAP','BLUR-USDT-SWAP','BNB-USDT-SWAP','BNT-USDT-SWAP','BOME-USDT-SWAP','BONK-USDT-SWAP','BRETT-USDT-SWAP','BTC-USDT-SWAP','BTC-USDT-SWAP','CATI-USDT-SWAP','CAT-USDT-SWAP','CELO-USDT-SWAP','CETUS-USDT-SWAP','CFX-USDT-SWAP','CHZ-USDT-SWAP','COMP-USDT-SWAP','COOKIE-USDT-SWAP','CORE-USDT-SWAP','CRO-USDT-SWAP','CRV-USDT-SWAP','CSPR-USDT-SWAP','CTC-USDT-SWAP','CVC-USDT-SWAP','CVX-USDT-SWAP','DEGEN-USDT-SWAP','DGB-USDT-SWAP','DOGE-USDT-SWAP','DOGS-USDT-SWAP','DOG-USDT-SWAP','DOOD-USDT-SWAP','DOT-USDT-SWAP','DUCK-USDT-SWAP','DYDX-USDT-SWAP','EGLD-USDT-SWAP','EIGEN-USDT-SWAP','ENJ-USDT-SWAP','ENS-USDT-SWAP','ETC-USDT-SWAP','ETHFI-USDT-SWAP','ETH-USDT-SWAP','ETHW-USDT-SWAP','FARTCOIN-USDT-SWAP','FIL-USDT-SWAP','FLM-USDT-SWAP','FLOKI-USDT-SWAP','FLOW-USDT-SWAP','FXS-USDT-SWAP','GALA-USDT-SWAP','GAS-USDT-SWAP','GLM-USDT-SWAP','GMT-USDT-SWAP','GMX-USDT-SWAP','GOAT-USDT-SWAP','GODS-USDT-SWAP','GPS-USDT-SWAP','GRASS-USDT-SWAP','GRIFFAIN-USDT-SWAP','GRT-USDT-SWAP','HBAR-USDT-SWAP','HMSTR-USDT-SWAP','HOME-USDT-SWAP','HUMA-USDT-SWAP','HYPE-USDT-SWAP','ICP-USDT-SWAP','ICX-USDT-SWAP','ID-USDT-SWAP','IMX-USDT-SWAP','INIT-USDT-SWAP','INJ-USDT-SWAP','IOST-USDT-SWAP','IOTA-USDT-SWAP','IP-USDT-SWAP','JELLYJELLY-USDT-SWAP','JOE-USDT-SWAP','JST-USDT-SWAP','JTO-USDT-SWAP','JUP-USDT-SWAP','KAITO-USDT-SWAP','KMNO-USDT-SWAP','KNC-USDT-SWAP','KSM-USDT-SWAP','LAUNCHCOIN-USDT-SWAP','LA-USDT-SWAP','LAYER-USDT-SWAP','LDO-USDT-SWAP','LINK-USDT-SWAP','LOOKS-USDT-SWAP','LPT-USDT-SWAP','LQTY-USDT-SWAP','LRC-USDT-SWAP','LSK-USDT-SWAP','LTC-USDT-SWAP','LUNA-USDT-SWAP','LUNC-USDT-SWAP','MAGIC-USDT-SWAP','MAJOR-USDT-SWAP','MANA-USDT-SWAP','MASK-USDT-SWAP','MEME-USDT-SWAP','MERL-USDT-SWAP','METIS-USDT-SWAP','ME-USDT-SWAP','MEW-USDT-SWAP','MINA-USDT-SWAP','MKR-USDT-SWAP','MOODENG-USDT-SWAP','MORPHO-USDT-SWAP','MOVE-USDT-SWAP','MUBARAK-USDT-SWAP','NC-USDT-SWAP','NEAR-USDT-SWAP','NEIROETH-USDT-SWAP','NEIRO-USDT-SWAP','NEO-USDT-SWAP','NIL-USDT-SWAP','NMR-USDT-SWAP','NOT-USDT-SWAP','NXPC-USDT-SWAP','OL-USDT-SWAP','OM-USDT-SWAP','ONDO-USDT-SWAP','ONE-USDT-SWAP','ONT-USDT-SWAP','OP-USDT-SWAP','ORBS-USDT-SWAP','ORDI-USDT-SWAP','PARTI-USDT-SWAP','PENGU-USDT-SWAP','PEOPLE-USDT-SWAP','PEPE-USDT-SWAP','PERP-USDT-SWAP','PIPPIN-USDT-SWAP','PI-USDT-SWAP','PLUME-USDT-SWAP','PNUT-USDT-SWAP','POL-USDT-SWAP','POPCAT-USDT-SWAP','PRCL-USDT-SWAP','PROMPT-USDT-SWAP','PYTH-USDT-SWAP','QTUM-USDT-SWAP','RAY-USDT-SWAP','RDNT-USDT-SWAP','RENDER-USDT-SWAP','RESOLV-USDT-SWAP','RSR-USDT-SWAP','RVN-USDT-SWAP','SAND-USDT-SWAP','SATS-USDT-SWAP','SCR-USDT-SWAP','SHELL-USDT-SWAP','SHIB-USDT-SWAP','SIGN-USDT-SWAP','SLERF-USDT-SWAP','SLP-USDT-SWAP','SNX-USDT-SWAP','SOL-USDT-SWAP','SOLV-USDT-SWAP','SONIC-USDT-SWAP','SOON-USDT-SWAP','SOPH-USDT-SWAP','SSV-USDT-SWAP','STORJ-USDT-SWAP','STRK-USDT-SWAP','STX-USDT-SWAP','SUI-USDT-SWAP','S-USDT-SWAP','SUSHI-USDT-SWAP','SWARMS-USDT-SWAP','TAO-USDT-SWAP','THETA-USDT-SWAP','TIA-USDT-SWAP','TNSR-USDT-SWAP','TON-USDT-SWAP','TRB-USDT-SWAP','TRUMP-USDT-SWAP','TRX-USDT-SWAP','TURBO-USDT-SWAP','T-USDT-SWAP','UMA-USDT-SWAP','UNI-USDT-SWAP','USDC-USDT-SWAP','USTC-USDT-SWAP','UXLINK-USDT-SWAP','VANA-USDT-SWAP','VINE-USDT-SWAP','VIRTUAL-USDT-SWAP','WAL-USDT-SWAP','WAXP-USDT-SWAP','WCT-USDT-SWAP','WIF-USDT-SWAP','WLD-USDT-SWAP','WOO-USDT-SWAP','W-USDT-SWAP','XAUT-USDT-SWAP','XCH-USDT-SWAP','XLM-USDT-SWAP','XRP-USDT-SWAP','XTZ-USDT-SWAP','YFI-USDT-SWAP','YGG-USDT-SWAP','ZENT-USDT-SWAP','ZEREBRO-USDT-SWAP','ZETA-USDT-SWAP','ZIL-USDT-SWAP','ZK-USDT-SWAP','ZRO-USDT-SWAP','ZRX-USDT-SWAP']  # Add your desired trading pairs
from crypto_pairs import SYMBOLS

RSI_PERIOD = 30
RSI_OVERBOUGHT_LOW = 60
RSI_OVERBOUGHT_HIGH = 70

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

TIMEFRAME_RSI = '1h'
TIMEFRAME_MACD = '15m'
CANDLE_LIMIT = 150

exchange = ccxt.okx({'options': {'defaultType': 'swap'}})

def fetch_candles(symbol, timeframe, limit):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if not ohlcv:
            return None
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] {symbol} ({timeframe}): {e}")
        return None

def add_indicators(df):
    if df.empty:
        return df
    df['rsi'] = RSIIndicator(close=df['close'], window=RSI_PERIOD).rsi()
    macd = MACD(close=df['close'], window_fast=MACD_FAST, window_slow=MACD_SLOW, window_sign=MACD_SIGNAL)
    df['macd_line'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def is_rsi_overbought(value):
    return RSI_OVERBOUGHT_LOW <= value <= RSI_OVERBOUGHT_HIGH

def detect_bearish_macd_divergence(df, num_crosses):
    crosses = []
    macd_line = df['macd_line']
    macd_signal = df['macd_signal']
    highs = df['high']

    for i in range(1, len(df)):
        prev_line = macd_line.iloc[i - 1]
        prev_signal = macd_signal.iloc[i - 1]
        curr_line = macd_line.iloc[i]
        curr_signal = macd_signal.iloc[i]
        if (prev_line > prev_signal and curr_line < curr_signal) or (prev_line < prev_signal and curr_line > curr_signal):
            crosses.append((df.index[i], curr_line, highs.iloc[i]))

    if len(crosses) < num_crosses:
        return False

    recent = crosses[-num_crosses:]
    prices = [price for _, _, price in recent]
    macds = [macd for _, macd, _ in recent]

    return prices[-1] > prices[0] and macds[-1] < macds[0]

def send_discord_alert(symbol):
    now = datetime.now(ZoneInfo("Asia/Manila")).strftime('%Y-%m-%d %H:%M %Z')
    message = f"""🔔 **4HR BP - 15 minutes Left Hand**🔴

**Symbol**: {symbol}
**Time**: {now}
===============================
"""
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print(f"[ALERT SENT] {symbol} at {now}")
    else:
        print(f"[ERROR] Discord alert failed for {symbol}: {response.status_code}")

def check_symbol(symbol):
    print(f"Checking {symbol}...")

    df_rsi = fetch_candles(symbol, TIMEFRAME_RSI, CANDLE_LIMIT)
    if df_rsi is None or df_rsi.empty:
        return
    df_rsi = add_indicators(df_rsi)

    if df_rsi['rsi'].isna().all():
        return

    latest_rsi = df_rsi['rsi'].dropna().iloc[-1]
    if not is_rsi_overbought(latest_rsi):
        return

    df_macd = fetch_candles(symbol, TIMEFRAME_MACD, CANDLE_LIMIT)
    if df_macd is None or df_macd.empty:
        return
    df_macd = add_indicators(df_macd)

    if df_macd['macd_line'].isna().all() or df_macd['macd_signal'].isna().all():
        return

    for crosses in range(3, 10):  # from 3 to 9
        if detect_bearish_macd_divergence(df_macd, crosses):
            send_discord_alert(symbol)
            time.sleep(1) 
            break

if __name__ == "__main__":
    for symbol in SYMBOLS:
        check_symbol(symbol)

        
        
        
#=============**=//=======


#=====================================================================================


