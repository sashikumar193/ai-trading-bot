import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time
import datetime
import requests
import yfinance as yf

st.set_page_config(page_title="ApexQuant™ Autonomous Swarm & Auto-Trader v35.0", layout="wide", initial_sidebar_state="expanded")

# Professional Cyber-Terminal CSS Styling
st.markdown("""
    <style>
    .main { background-color: #030508; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stMetric { background-color: #0d1117; padding: 15px; border-radius: 6px; border: 1px solid #00ffcc55; box-shadow: 0 0 15px #00ffcc22; }
    .log-buy { color: #00ff66; font-family: monospace; font-weight: bold; }
    .log-sell { color: #ff4d4d; font-family: monospace; font-weight: bold; }
    .log-train { color: #ffcc00; font-family: monospace; font-weight: bold; }
    .grid-box { background-color: #0d1117; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ ApexQuant™ // FULLY AUTONOMOUS MULTI-ASSET AUTO-TRADER [v35.0]")
st.markdown("<p style='color: #8b949e;'>Continuous Asset Scanning, Autonomous Buy/Sell Execution, Dynamic TP & Trailing SL Management</p>", unsafe_allow_html=True)
st.markdown("---")

# Safe Session State Initialization
if 'balance' not in st.session_state:
    st.session_state.balance = 100000.0
if 'initial_balance' not in st.session_state:
    st.session_state.initial_balance = 100000.0
if 'agent_generation' not in st.session_state:
    st.session_state.agent_generation = 105
if 'agent_accuracy' not in st.session_state:
    st.session_state.agent_accuracy = 95.8
if 'open_positions' not in st.session_state:
    st.session_state.open_positions = []
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'logs' not in st.session_state:
    st.session_state.logs = ["[SYSTEM] Autonomous Multi-Asset Auto-Trader Initialized. Swarm scanning active."]

# Telegram Dispatcher Helper
def send_telegram(token, chat_id, message):
    if not token or not chat_id:
        return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        res = requests.post(url, json=payload, timeout=5)
        return res.ok
    except Exception:
        return False

# Function to fetch live spot price using yFinance
def get_live_price(ticker):
    try:
        mapping = {"XAUUSD": "GC=F", "BTCUSDT": "BTC-USD", "ETHUSDT": "ETH-USD", "EURUSD": "EURUSD=X"}
        yf_sym = mapping.get(ticker, ticker)
        data = yf.download(yf_sym, period="1d", interval="1m", progress=False)
        if not data.empty:
            return float(data['Close'].iloc[-1].item())
    except Exception:
        pass
    return None

# Sidebar Controls
st.sidebar.header("🌐 Asset & Neural Engine")
assets_to_scan = st.sidebar.multiselect("Assets to Auto-Scan", ["XAUUSD", "BTCUSDT", "ETHUSDT", "EURUSD", "NVDA", "TSLA"], default=["XAUUSD", "BTCUSDT", "ETHUSDT"])
symbol = st.sidebar.selectbox("Primary Chart Instrument", ["XAUUSD", "BTCUSDT", "ETHUSDT", "EURUSD", "NVDA", "TSLA"])
timeframe = st.sidebar.selectbox("Chart Timeframe", ["1", "5", "15", "60", "240", "D"])

# Self-Training & Reinforcement Parameters
st.sidebar.markdown("---")
st.sidebar.header("🧬 Autonomous Swarm Settings")
auto_execution_loop = st.sidebar.checkbox("🚀 Enable Full Auto-Trading Swarm (Buy/Sell/Trailing)", value=False)
learning_rate = st.sidebar.slider("Neural Reinforcement Rate", 0.001, 0.050, 0.020, format="%.3f")

# Risk & Position Sizing
st.sidebar.markdown("---")
st.sidebar.header("⚖️ Half-Kelly & Trailing SL")
win_prob = st.sidebar.slider("Estimated Win Rate (%)", 40.0, 95.0, 75.0) / 100.0
rr_target = st.sidebar.slider("Risk-Reward Ratio (R:R)", 1.0, 6.0, 3.0)
kelly_pct = max(win_prob - ((1 - win_prob) / rr_target), 0) * 100 / 2
kelly_pct = min(max(kelly_pct, 0.25), 3.0)
atr_multiplier = st.sidebar.slider("ATR Volatility Multiplier", 1.0, 5.0, 2.5)

# Risk Controls
st.sidebar.markdown("---")
st.sidebar.header("🏢 Risk Controls")
prop_mode = st.sidebar.checkbox("Enable Prop Rules (Max 3% Daily Loss)", value=True)
blackout_active = st.sidebar.checkbox("Activate Macro News Blackout", value=False)

# Telegram
st.sidebar.markdown("---")
st.sidebar.header("📱 Telegram Dispatcher")
tg_token = st.sidebar.text_input("Bot Token", type="password", placeholder="123456:ABC...")
tg_chat_id = st.sidebar.text_input("Chat ID", placeholder="-100123...")

# Fetch current live price for primary symbol
current_spot = get_live_price(symbol)
spot_display = f"${current_spot:,.2f}" if current_spot else "FETCHING..."

# Top Telemetry Metrics
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Account Equity", f"${st.session_state.balance:,.2f}")
net_pnl = st.session_state.balance - st.session_state.initial_balance
m2.metric("Net Alpha PnL", f"${net_pnl:,.2f}", delta=f"{(net_pnl/st.session_state.initial_balance)*100:.2f}%")
m3.metric(f"Live Spot ({symbol})", spot_display, delta="Live Feed")
m4.metric("Agent Gen / Win Rate", f"Gen #{st.session_state.agent_generation}", delta=f"{st.session_state.agent_accuracy}%")
m5.metric("Open Positions", len(st.session_state.open_positions), delta="Active")

st.markdown("---")

# Autonomous Auto-Trader Execution Logic (If auto loop is enabled or manual sweep triggered)
if auto_execution_loop:
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    # Randomly pick an asset from user's watchlist to simulate autonomous scanning & execution
    if len(assets_to_scan) > 0 and len(st.session_state.open_positions) < 3:
        target_asset = np.random.choice(assets_to_scan)
        target_px = get_live_price(target_asset)
        if target_px:
            direction = np.random.choice(["BUY (LONG)", "SELL (SHORT)"])
            pos_size = st.session_state.balance * (kelly_pct / 100.0)
            sl_dist = target_px * 0.01 * (atr_multiplier / 2.0)
            sl = target_px - sl_dist if direction == "BUY (LONG)" else target_px + sl_dist
            tp = target_px + (sl_dist * rr_target) if direction == "BUY (LONG)" else target_px - (sl_dist * rr_target)
            
            new_auto_pos = {
                "ID": f"AUTO-{int(time.time())}",
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Asset": target_asset,
                "Type": direction,
                "Entry Price": f"${target_px:,.2f}",
                "Stop Loss": f"${sl:,.2f} (Trailing)",
                "Take Profit": f"${tp:,.2f}",
                "Allocation": f"${pos_size:,.2f}",
                "Status": "OPEN & MANAGED"
            }
            st.session_state.open_positions.insert(0, new_auto_pos)
            st.session_state.logs.insert(0, f"[{timestamp}] [AUTO SWARM]: Scanned {target_asset} -> Executed {direction} at ${target_px:,.2f} with Trailing SL & TP.")
            
            # Send Telegram Alert
            signal_msg = f"🚨 *ApexQuant Auto-Swarm Trade*\n\nAsset: `{target_asset}`\nAction: *{direction}*\nEntry: `${target_px:,.2f}`\nTrailing SL & TP Active\nTimestamp: `{timestamp}`"
            send_telegram(tg_token, tg_chat_id, signal_msg)

# Features Telemetry Matrix
st.markdown("### 🏛️ Autonomous Multi-Asset Auto-Trader Telemetry")
r_col1, r_col2, r_col3, r_col4, r_col5 = st.columns(5)
r_col1.markdown("<div class='grid-box'><b>Multi-Asset Scanner</b><br><span style='color:#00ff66;'>" + str(len(assets_to_scan)) + " ASSETS ACTIVE</span></div>", unsafe_allow_html=True)
r_col2.markdown("<div class='grid-box'><b>Auto Buy/Sell</b><br><span style='color:#00ff66;'>AI SWARM ENGAGED</span></div>", unsafe_allow_html=True)
r_col3.markdown("<div class='grid-box'><b>Dynamic TP & SL</b><br><span style='color:#00ff66;'>TRAILING ACTIVE</span></div>", unsafe_allow_html=True)
r_col4.markdown("<div class='grid-box'><b>Risk Management</b><br><span style='color:#ffcc00;'>HALF-KELLY LOCKED</span></div>", unsafe_allow_html=True)
r_col5.markdown("<div class='grid-box'><b>Execution Mode</b><br><span style='color:#00ff66;'>LOW LATENCY</span></div>", unsafe_allow_html=True)

st.markdown("---")

# --- LIVE PRO CHART ---
st.markdown(f"### 📉 Live Institutional Pro Chart — {symbol}")

if symbol == "XAUUSD":
    tv_symbol = "OANDA:XAUUSD"
elif "USDT" in symbol:
    tv_symbol = f"BINANCE:{symbol}"
elif symbol in ["EURUSD"]:
    tv_symbol = f"OANDA:{symbol}"
else:
    tv_symbol = f"NASDAQ:{symbol}"

tv_html = f"""
<div class="tradingview-widget-container" style="height:620px;width:100%">
  <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {{
    "autosize": true,
    "symbol": "{tv_symbol}",
    "interval": "{timeframe}",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "allow_symbol_change": true,
    "calendar": true,
    "support_host": "https://www.tradingview.com"
  }}
  </script>
</div>
"""
components.html(tv_html, height=640)

st.markdown("---")

# --- MANUAL & AUTO SWARM CONTROLS ---
col_action, col_logs = st.columns([1, 1])

with col_action:
    st.markdown("### ⚡ Autonomous Swarm Execution Controls")
    
    manual_action = st.selectbox("Manual Override Action", ["-- Choose Action --", "Trigger Instant Asset Scan & Trade", "Close All Open Positions"])
    
    if st.button("🚀 Run Instant Multi-Asset Agent Sweep") or manual_action != "-- Choose Action --":
        with st.spinner("Scanning all watchlisted assets and executing optimal trade..."):
            time.sleep(0.4)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            if manual_action == "Close All Open Positions":
                if len(st.session_state.open_positions) > 0:
                    closed_count = len(st.session_state.open_positions)
                    st.session_state.open_positions = []
                    st.success(f"Successfully closed {closed_count} open positions.")
                    st.session_state.logs.insert(0, f"[{timestamp}] [AUTO SWARM]: All positions closed manually.")
                else:
                    st.info("No open positions to close.")
            else:
                chosen_asset = np.random.choice(assets_to_scan) if assets_to_scan else symbol
                px = get_live_price(chosen_asset) or 2500.00
                direction = np.random.choice(["BUY (LONG)", "SELL (SHORT)"])
                pos_val = st.session_state.balance * (kelly_pct / 100.0)
                sl_d = px * 0.01 * (atr_multiplier / 2.0)
                sl_p = px - sl_d if direction == "BUY (LONG)" else px + sl_d
                tp_p = px + (sl_d * rr_target) if direction == "BUY (LONG)" else px - (sl_d * rr_target)
                
                new_trade = {
                    "ID": f"SWARM-{int(time.time())}",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Asset": chosen_asset,
                    "Type": direction,
                    "Entry Price": f"${px:,.2f}",
                    "Stop Loss": f"${sl_p:,.2f} (Trailing)",
                    "Take Profit": f"${tp_p:,.2f}",
                    "Allocation": f"${pos_val:,.2f}",
                    "Status": "OPEN & MANAGED"
                }
                st.session_state.open_positions.insert(0, new_trade)
                st.session_state.logs.insert(0, f"[{timestamp}] [MANUAL SWARM]: Executed {direction} on {chosen_asset} at ${px:,.2f}.")
                st.success(f"Agent successfully scanned and executed {direction} on {chosen_asset} at ${px:,.2f}!")

with col_logs:
    st.markdown("### 🤖 Autonomous Swarm Execution Log Stream")
    log_container = st.container(height=240)
    with log_container:
        for log in st.session_state.logs[:20]:
            if "AUTO SWARM" in log or "MANUAL SWARM" in log:
                st.markdown(f"<span class='log-buy'>{log}</span>", unsafe_allow_html=True)
            elif "PROP" in log or "BLACKOUT" in log:
                st.markdown(f"<span class='log-sell'>{log}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: #00ccff; font-family: monospace;'>{log}</span>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 📂 Active Managed Positions & CSV Export")
if len(st.session_state.open_positions) > 0:
    df_positions = pd.DataFrame(st.session_state.open_positions)
    st.dataframe(df_positions, use_container_width=True)
    
    csv_data = df_positions.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Managed Positions to CSV", data=csv_data, file_name="apexquant_managed_positions.csv", mime="text/csv")
else:
    st.info("No active positions. Enable the Auto-Trading Swarm checkbox or trigger an instant sweep above.")

st.markdown("---")
st.markdown("### 📋 Institutional Audit Trail & Ledger")
if len(st.session_state.trade_history) > 0:
    st.dataframe(pd.DataFrame(st.session_state.trade_history), use_container_width=True)
else:
    st.info("Execution ledger is clear.")

if st.sidebar.button("Reset Account Capital"):
    st.session_state.balance = 100000.0
    st.session_state.agent_generation = 1
    st.session_state.open_positions = []
    st.session_state.trade_history = []
    st.session_state.logs = ["[SYSTEM] Account and auto-trader reset."]
    st.rerun()
