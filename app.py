{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import yfinance as yf\
import pandas as pd\
import pandas_ta as ta\
import plotly.graph_objects as go\
\
st.set_page_config(page_title="AI Indian Stock Analyzer", layout="wide")\
\
# Custom CSS for UI\
st.markdown("""\
    <style>\
    .main \{ background-color: #0e1117; \}\
    .stMetric \{ background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #333; \}\
    </style>\
    """, unsafe_allow_html=True)\
\
st.title("\uc0\u55356 \u57337  AI Indian Stock Signal Pro")\
st.caption("Real-time NSE/BSE Analysis with AI-driven Entry & Exit Signals")\
\
# --- Sidebar Management ---\
if 'watchlist' not in st.session_state:\
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'SBIN.NS', 'INFY.NS']\
\
with st.sidebar:\
    st.header("\uc0\u55357 \u56522  Watchlist Setup")\
    symbol = st.text_input("Enter Symbol (e.g. TATAMOTORS, HDFCBANK)").upper()\
    exchange = st.selectbox("Exchange", ["NS (NSE)", "BO (BSE)"])\
    \
    if st.button("\uc0\u10133  Add to Watchlist"):\
        suffix = ".NS" if "NS" in exchange else ".BO"\
        full_symbol = f"\{symbol\}\{suffix\}"\
        if full_symbol not in st.session_state.watchlist:\
            st.session_state.watchlist.append(full_symbol)\
            st.rerun()\
\
    selected_stock = st.sidebar.radio("Select Stock to Analyze", st.session_state.watchlist)\
    \
    if st.sidebar.button("\uc0\u55357 \u56785 \u65039  Remove Selected"):\
        st.session_state.watchlist.remove(selected_stock)\
        st.rerun()\
\
# --- Analysis Engine ---\
def fetch_and_analyze(ticker):\
    df = yf.download(ticker, period="1y", interval="1d", progress=False)\
    if df.empty: return None\
    \
    # Technical Indicators\
    df['RSI'] = ta.rsi(df['Close'], length=14)\
    df['EMA20'] = ta.ema(df['Close'], length=20)\
    df['EMA50'] = ta.ema(df['Close'], length=50)\
    df['MACD'], df['MACDs'], df['MACDh'] = ta.macd(df['Close']).iloc[:,0], ta.macd(df['Close']).iloc[:,1], ta.macd(df['Close']).iloc[:,2]\
    \
    latest = df.iloc[-1]\
    prev = df.iloc[-2]\
    price = round(latest['Close'], 2)\
    \
    # AI Logic\
    signal = "HOLD"\
    suggestion = "Maintain current position. Waiting for a clear trend."\
    \
    # Bullish Logic\
    if (latest['RSI'] < 40 and latest['Close'] > latest['EMA50']) or (prev['EMA20'] < prev['EMA50'] and latest['EMA20'] > latest['EMA50']):\
        signal = "BUY"\
        suggestion = "Strong Bullish momentum detected. Price is above EMA50 with a trend reversal signal."\
    # Bearish Logic\
    elif latest['RSI'] > 75 or (prev['EMA20'] > prev['EMA50'] and latest['EMA20'] < latest['EMA50']):\
        signal = "SELL"\
        suggestion = "Overbought conditions or EMA Crossover detected. Risk of price drop is high."\
\
    # Calculation of TP and SL\
    if signal == "BUY":\
        tp = round(price * 1.06, 2)\
        sl = round(price * 0.96, 2)\
    elif signal == "SELL":\
        tp = round(price * 0.94, 2)\
        sl = round(price * 1.04, 2)\
    else:\
        tp, sl = "-", "-"\
        \
    return df, signal, price, tp, sl, suggestion\
\
# --- Display UI ---\
if selected_stock:\
    with st.spinner(f'Analyzing \{selected_stock\}...'):\
        data, signal, price, tp, sl, suggestion = fetch_and_analyze(selected_stock)\
        \
        # Metrics Row\
        m1, m2, m3, m4 = st.columns(4)\
        m1.metric("Current Price", f"\uc0\u8377 \{price\}")\
        \
        sig_color = "#00ff00" if signal == "BUY" else "#ff4b4b" if signal == "SELL" else "#f0f0f0"\
        m2.markdown(f"<div style='text-align:center; padding:10px; border-radius:5px; background-color:\{sig_color\}; color:black; font-weight:bold;'>SIGNAL: \{signal\}</div>", unsafe_allow_html=True)\
        \
        m3.metric("Target (AI)", f"\uc0\u8377 \{tp\}")\
        m4.metric("Stop Loss", f"\uc0\u8377 \{sl\}")\
\
        st.success(f"**AI Recommendation:** \{suggestion\}")\
\
        # Charts\
        fig = go.Figure()\
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Price"))\
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], name="EMA 20", line=dict(color='cyan', width=1)))\
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], name="EMA 50", line=dict(color='magenta', width=1)))\
        \
        fig.update_layout(template="plotly_dark", height=600, xaxis_rangeslider_visible=False, title=f"\{selected_stock\} Technical Chart")\
        st.plotly_chart(fig, use_container_width=True)\
\
        # Technical Stats\
        with st.expander("Show Technical Summary"):\
            col_a, col_b = st.columns(2)\
            col_a.write(f"**RSI (14):** \{round(data['RSI'].iloc[-1], 2)\}")\
            col_b.write(f"**24h Volume:** \{data['Volume'].iloc[-1]\}")}