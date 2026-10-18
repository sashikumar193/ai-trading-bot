import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import yfinance as yf

st.set_page_config(page_title="GoldMind Signals™ | AI Trading Terminal", layout="wide", initial_sidebar_state="expanded")

# GoldMind Cyber-Terminal CSS Styling
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #f0b90b; font-family: 'Courier New', monospace; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 6px; border: 1px solid #f0b90b44; box-shadow: 0 0 12px #f0b90b15; }
    .gold-panel { background-color: #161b22; padding: 15px; border-radius: 8px; border-left: 4px solid #f0b90b; margin-bottom: 15px; }
    .log-buy { color: #00ff66; font-family: monospace; font-weight: bold; }
    .log-sell { color: #ff4d4d; font-family: monospace; font-weight: bold; }
    .log-info { color: #33ccff; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

st.title("🥇 GoldMind Signals™ // INSTITUTIONAL XAUUSD AI PLATFORM")
st.markdown("<p style='color: #8b949e;'>Autonomous Multi-Agent XAUUSD Signal Generator, XGBoost ML Scoring & Telegram Dispatcher</p>", unsafe_allow_html=True)
st.markdown("---")

# Session State Initialization
if 'balance' not in st.session_state:
    st.session_state.balance = 25000.0
    st.session_state.initial_balance = 25000.0
    st.session_state.trades_history = []
    st.session_state.gold_logs = ["[GOLDMIND SYSTEM] Multi-Agent Swarm Initialized for XAUUSD Execution."]

# Sidebar Controls
st.sidebar.header("⚙️ GoldMind Parameters")
asset_symbol = st.sidebar.selectbox("Signal Asset", ["GC=F", "XAUUSD=X", "BTC-USD", "EURUSD=X"])
model_engine = st.sidebar.selectbox("AI Model Architecture", ["XGBoost + Smart Money Concepts (SMC)", "Random Forest Order Block Classifier", "LSTM Neural Net Trend Filter"])
risk_per_trade = st.sidebar.slider("Micro-Lot Risk Allocation (%)", 0.25, 5.0, 1.0)
auto_dispatch = st.sidebar.checkbox("🚀 Enable Autonomous Telegram/Signal Loop", value=False)

# Top Metrics Row
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Account Equity", f"${st.session_state.balance:,.2f}")
total_pnl = st.session_state.balance - st.session_state.initial_balance
c2.metric("Strategy PnL", f"${total_pnl:,.2f}", delta=f"{(total_pnl/st.session_state.initial_balance)*100:.2f}%")
c3.metric("XGBoost Confidence", "96.4%", delta="+2.8%")
c4.metric("Active Agents", "4 / 4 Online", delta="Optimized")
c5.metric("Telegram Bot", "CONNECTED", delta="Secure")

st.markdown("---")

# Main Dashboard Layout
col_chart, col_swarm = st.columns([1.3, 0.7])

with col_chart:
    st.markdown("### 📈 Live XAUUSD Market Structure & Price Action")
    try:
        data = yf.download(asset_symbol, period="5d", interval="1h", progress=False)
        if not data.empty:
            spot_price = float(data['Close'].iloc[-1].item())
            high_price = float(data['High'].max().item())
            low_price = float(data['Low'].min().item())
            
            sub_c1, sub_c2, sub_c3 = st.columns(3)
            sub_c1.metric("Spot Price", f"${spot_price:,.2f}")
            sub_c2.metric("Session High", f"${high_price:,.2f}")
            sub_c3.metric("Session Low", f"${low_price:,.2f}")
            
            # Interactive Line Chart
            st.line_chart(data['Close'], height=300)
        else:
            st.warning("Connecting to institutional price feed...")
    except Exception as e:
        st.error(f"Feed error: {e}")

with col_swarm:
    st.markdown("### 🤖 GoldMind Multi-Agent Real-Time Stream")
    
    if st.button("⚡ Run GoldMind Signal Scan") or auto_dispatch:
        with st.spinner("Running XGBoost model and SMC structure scan..."):
            time.sleep(0.7)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            # Simulate Multi-Agent Logs
            st.session_state.gold_logs.insert(0, f"[{timestamp}] [MARKET AGENT]: Liquidity sweep near support on {asset_symbol}.")
            st.session_state.gold_logs.insert(0, f"[{timestamp}] [SIGNAL AGENT]: XGBoost probability score 94.8% -> BUY (LONG) setup confirmed.")
            st.session_state.gold_logs.insert(0, f"[{timestamp}] [RISK AGENT]: ATR volatility filtered. Position size locked.")
            
            trade_profit = np.random.uniform(100.0, 350.0)
            st.session_state.balance += trade_profit
            st.session_state.trades_history.insert(0, {
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Asset": asset_symbol,
                "Model": model_engine.split()[0],
                "Direction": "BUY (LONG)",
                "Alpha PnL": f"+${trade_profit:.2f}",
                "Status": "EXECUTED & SECURED"
            })
            st.success("GoldMind signal successfully generated and logged!")
    
    # Render Log Box
    gold_log_box = st.container(height=300)
    with gold_log_box:
        for log in st.session_state.gold_logs[:20]:
            if "SIGNAL" in log:
                st.markdown(f"<span class='log-buy'>{log}</span>", unsafe_allow_html=True)
            elif "MARKET" in log:
                st.markdown(f"<span class='log-info'>{log}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span class='log-sell'>{log}</span>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📋 GoldMind Signal Ledger & Audit Trail")
if len(st.session_state.trades_history) > 0:
    st.dataframe(pd.DataFrame(st.session_state.trades_history), use_container_width=True)
else:
    st.info("Signal ledger is clear. Run a signal scan or enable autonomous loop.")

if st.sidebar.button("Reset GoldMind Account"):
    st.session_state.balance = 25000.0
    st.session_state.trades_history = []
    st.session_state.gold_logs = ["[GOLDMIND SYSTEM] Ledger reset."]
    st.rerun()
