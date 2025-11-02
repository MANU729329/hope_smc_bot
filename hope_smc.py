# -*- coding: utf-8 -*-
"""
HOPE_SMC_AUTO_BOT v1 (Test Data Version)
Author: Manu
Description: Simulated Smart Money Concepts (HOPE) Signal Bot that sends A+ setups to Telegram
"""

import time
import threading
import random
import pandas as pd
import requests
from flask import Flask
from datetime import datetime

# ==============================
# 🔹 Telegram Bot Configuration
# ==============================
BOT_TOKEN = 8376149890 
CHAT_ID = 1609197089

# ==============================
# 🔹 Flask Web Setup (Render Ping)
# ==============================
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 HOPE SMC Bot is running successfully on Render (Test Mode)."

# ==============================
# 🔹 Simulated Market Data
# ==============================
PAIRS = ["EURUSD", "GBPJPY", "USDJPY", "XAUUSD", "GBPUSD"]

def simulate_market_data():
    data = []
    for pair in PAIRS:
        price = random.uniform(1.0, 2000.0)
        rsi = random.randint(10, 90)
        sweep = random.choice([True, False])
        bos = random.choice([True, False])
        entry_conf = random.choice([True, False])
        bias = random.choice(["Bullish", "Bearish"])
        data.append({
            "pair": pair,
            "price": round(price, 2),
            "rsi": rsi,
            "sweep": sweep,
            "bos": bos,
            "entry_conf": entry_conf,
            "bias": bias
        })
    return pd.DataFrame(data)

# ==============================
# 🔹 HOPE Strategy Logic (Simulated)
# ==============================
def check_hope_setup(df):
    setups = []
    for _, row in df.iterrows():
        if row["sweep"] and row["bos"] and row["entry_conf"]:
            if row["bias"] == "Bullish" and row["rsi"] < 40:
                setups.append((row["pair"], "BUY 🟩", row["bias"], row["price"]))
            elif row["bias"] == "Bearish" and row["rsi"] > 60:
                setups.append((row["pair"], "SELL 🔻", row["bias"], row["price"]))
    return setups

# ==============================
# 🔹 Telegram Message Sender
# ==============================
def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/8376149890:AAFiw5rok3-NbT5SdxHGWcmn3Q7aEOzKKYs/sendMessage"
        payload = {"chat_id":1609197089 , "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram send error: {e}")

# ==============================
# 🔹 Bot Runner (Main Logic)
# ==============================
def run_hope_smc():
    print("🔍 Checking for A+ HOPE setups...\n")
    df = simulate_market_data()
    setups = check_hope_setup(df)

    if setups:
        for setup in setups:
            pair, signal, bias, price = setup
            msg = f"""
🔥 HOPE A+ SETUP DETECTED 🔥
Pair: {pair}
Bias: {bias}
Signal: {signal}
Price: {price}
RR: 1:3
Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
Session: Simulated
"""
            print(msg)
            send_telegram_message(msg)
    else:
        print("No A+ setups right now.\n")

# ==============================
# 🔹 Background Auto Loop
# ==============================
def start_auto_loop():
    print("🤖 HOPE SMC Bot started. Scanning every 15 minutes...\n")
    while True:
        run_hope_smc()
        print("⏱ Waiting 15 minutes before next scan...\n")
        time.sleep(900)  # 15 minutes

# ==============================
# 🔹 Run Flask + Bot Thread Together
# ==============================
if __name__ == '__main__':
    threading.Thread(target=start_auto_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)

