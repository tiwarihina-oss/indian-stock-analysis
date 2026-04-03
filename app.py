import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="Pro Indian Market Suite", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a clean look
st.markdown("""
    <style>
    .metric-card { background-color: #1e2130; border-radius: 10px; padding: 15px; border: 1px solid #333; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #0e1117; border-radius: 5px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- UTILITY FUNCTIONS ---
def get_clean_data(ticker, period="1y", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    if not data.empty and isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data

def calculate_technicals(df):
    # EMA
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# --- APP LAYOUT ---
st.title("🏹 Indian Market Intelligence")

tabs = st.tabs(["📊 Market Dashboard", "🔍 AI Stock Analyzer"])

# ==========================================
# TAB 1: MARKET DASHBOARD
# ==========================================
with tabs[0]:
    st.subheader("Market Overview (NIFTY 50)")
    
    # Nifty 50 Chart
    nifty_data = get_clean_data("^NSEI", period="1mo", interval="15m")
    if not nifty_data.empty:
        fig_nifty = go.Figure()
        fig_nifty.add_trace(go.Scatter(x=nifty_data.index, y=nifty_data['Close'], fill='tozeroy', line=dict(color='#00ffcc', width=2), name="Nifty 50"))
        fig_nifty.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig_nifty, use_container_width=True)

    st.divider()
    st.subheader("Sector Performance (%)")
    
    # Sector List
    sectors = {
        "Nifty Bank": "^NSEBANK",
        "Nifty IT": "^CNXIT",
        "Nifty Pharma": "^CNXPHARMA",
        "Nifty Auto": "^CNXAUTO",
        "Nifty FMCG": "^CNXFMCG",
        "Nifty Metal": "^CNXMETAL"
    }
    
    # Display Sectors in Columns
    cols = st.columns(len(sectors))
    for i, (name, sym) in enumerate(sectors.items()):
        s_data = yf.download(sym, period="2d", interval="1d", progress=False)
        if len(s_data) >= 2:
            if isinstance(s_data.columns, pd.MultiIndex): s_data.columns = s_data.columns.get_level_values(0)
            change = ((s_data['Close'].iloc[-1] - s_data['Close'].iloc[-2]) / s_data['Close'].iloc[-2]) * 100
            color = "inverse" if change < 0 else "normal"
            cols[i].metric(name, f"{round(float(s_data['Close'].iloc[-1]), 1)}", f"{round(float(change), 2)}%", delta_color=color)

# ==========================================
# TAB 2: AI ANALYZER
# ==========================================
with tabs[1]:
    # Sidebar within Tab 2 logic
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'SBIN.NS', 'HDFCBANK.NS']

    st.sidebar.header("Navigation")
    new_stock = st.sidebar.text_input("Quick Add (e.g. INFY)").upper()
    if st.sidebar.button("➕ Add"):
        if new_stock:
            st.session_state.watchlist.append(f"{new_stock}.NS")
            st.rerun()

    current_stock = st.sidebar.selectbox("Select Target Stock", st.session_state.watchlist)
    if st.sidebar.button("🗑️ Remove Selected"):
        st.session_state.watchlist.remove(current_stock)
        st.rerun()

    # Analysis Section
    if current_stock:
        with st.spinner(f"AI is analyzing {current_stock}..."):
            data = get_clean_data(current_stock)
            if not data.empty:
                df = calculate_technicals(data)
                last = df.iloc[-1]
                price = round(float(last['Close']), 2)
                rsi = float(last['RSI'])
                
                # Signal Logic
                signal, s_color = "HOLD", "#f0f0f0"
                if rsi < 38: signal, s_color = "BUY", "#00ff00"
                elif rsi > 68: signal, s_color = "SELL", "#ff4b4b"
                
                target = round(price * 1.05, 2) if signal != "SELL" else round(price * 0.95, 2)
                sl = round(price * 0.97, 2) if signal != "SELL" else round(price * 1.03, 2)

                # UI Display
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Live Price", f"₹{price}")
                c2.markdown(f"### <span style='color:{s_color}'>{signal}</span>", unsafe_allow_html=True)
                c3.metric("AI Target", f"₹{target}")
                c4.metric("Stop Loss", f"₹{sl}")

                st.success(f"**AI Logic:** RSI at {round(rsi, 2)}. " + 
                          ("Momentum looks bullish." if signal=="BUY" else "High overbought risk." if signal=="SELL" else "Wait for trend."))

                # Main Technical Chart
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Candles"))
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name="EMA 20", line=dict(color='orange')))
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], name="EMA 50", line=dict(color='blue')))
                fig.update_layout(template="plotly_dark", height=500, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Invalid symbol. Please use NSE/BSE tickers.")
