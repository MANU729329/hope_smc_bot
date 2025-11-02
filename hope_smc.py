# -*- coding: utf-8 -*-
"""
HOPE_SMC_AUTO_BOT v2 (Live Market Data Version)
Author: Manu
Description: Real-time Smart Money Concepts (HOPE) Signal Bot with live data + Telegram alerts.
"""

import time
import threading
import pandas as pd
import yfinance as yf
import requests
from flask import Flask
from datetime import datetime

# ==============================
# 🔹 Telegram Configuration
# ==============================
BOT_TOKEN = 8376149890
CHAT_ID = 1609197089

# ==============================
# 🔹 Flask Web Setup (Render Ping)
# ==============================
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 HOPE SMC Bot is live and pulling real market data!"

# ==============================
# 🔹 Forex Pair Mapping (Yahoo Tickers)
# ==============================
PAIRS = {
    "EURUSD": "EURUSD=X",
    "GBPJPY": "GBPJPY=X",
    "USDJPY": "USDJPY=X",
    "XAUUSD": "XAUUSD=X",
    "GBPUSD": "GBPUSD=X"
}

# ==============================
# 🔹 Fetch Live Market Data
# ==============================
def get_live_data():
    data = []
    for pair, symbol in PAIRS.items():
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1d", interval="15m")
            if not df.empty:
                latest = df.iloc[-1]
                open_p, close_p, high, low = latest["Open"], latest["Close"], latest["High"], latest["Low"]
                price = round(close_p, 5)

                # Simulate SMC signals (replace with real logic later)
                sweep = (high - close_p) / close_p > 0.002  # small wick logic
                bos = abs(close_p - open_p) / open_p > 0.001
                entry_conf = (close_p > open_p)
                bias = "Bullish" if close_p > open_p else "Bearish"

                data.append({
                    "pair": pair,
                    "price": price,
                    "open": open_p,
                    "close": close_p,
                    "sweep": sweep,
                    "bos": bos,
                    "entry_conf": entry_conf,
                    "bias": bias
                })
        except Exception as e:
            print(f"⚠️ Error fetching {pair}: {e}")
    return pd.DataFrame(data)

# ==============================
# 🔹 HOPE Setup Checker
# ==============================
def check_hope_setup(df):
    setups = []
    for _, row in df.iterrows():
        if row["sweep"] and row["bos"] and row["entry_conf"]:
            signal = "BUY 🟩" if row["bias"] == "Bullish" else "SELL 🔻"
            setups.append((row["pair"], signal, row["bias"], row["price"]))
    return setups

# ==============================
# 🔹 Telegram Sender
# ==============================
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot8376149890:AAFiw5rok3-NbT5SdxHGWcmn3Q7aEOzKKYs/sendMessage"
        payload = {"chat_id": 1609197089, "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

# ==============================
# 🔹 Main Runner
# ==============================
def run_hope_smc():
    print("🔍 Checking live market data for A+ setups...\n")
    df = get_live_data()
    if df.empty:
        print("⚠️ No data fetched. Skipping this cycle.\n")
        return

    setups = check_hope_setup(df)

    if setups:
        for setup in setups:
            pair, signal, bias, price = setup
            msg = f"""
🔥 HOPE A+ SETUP DETECTED (LIVE) 🔥
Pair: {pair}
Bias: {bias}
Signal: {signal}
Price: {price}
RR: 1:3
Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
Session: London/New York (Live Data)
"""
            print(msg)
            send_telegram_message(msg)
    else:
        print("No A+ setups at this moment.\n")

# ==============================
# 🔹 Auto Loop (Every 15 min)
# ==============================
def start_auto_loop():
    print("🤖 HOPE SMC Bot started with LIVE market data.\n")
    while True:
        run_hope_smc()
        print("⏱ Waiting 15 minutes for next scan...\n")
        time.sleep(900)  # 15 minutes

# ==============================
# 🔹 Run Flask + Bot
# ==============================
if __name__ == '__main__':
    threading.Thread(target=start_auto_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
