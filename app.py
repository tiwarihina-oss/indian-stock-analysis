import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go

# Set page to wide mode
st.set_page_config(page_title="AI Indian Stock Analyzer", layout="wide")

st.title("🏹 AI Indian Stock Signal Pro")

# Initialize Watchlist in session state
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'SBIN.NS']

# --- SIDEBAR ---
with st.sidebar:
    st.header("📊 Watchlist")
    new_symbol = st.text_input("Enter Symbol (e.g. INFY, TATAMOTORS)").upper()
    exchange = st.selectbox("Exchange", ["NSE", "BSE"])
    
    if st.button("➕ Add Stock"):
        if new_symbol:
            suffix = ".NS" if exchange == "NSE" else ".BO"
            full_symbol = f"{new_symbol}{suffix}"
            if full_symbol not in st.session_state.watchlist:
                st.session_state.watchlist.append(full_symbol)
                st.rerun()

    selected_stock = st.selectbox("Analyze Stock:", st.session_state.watchlist)
    
    if st.button("🗑️ Remove Selected"):
        if selected_stock in st.session_state.watchlist:
            st.session_state.watchlist.remove(selected_stock)
            st.rerun()

# --- DATA PROCESSING ---
def get_analysis(ticker):
    try:
        # Fetch data
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        
        if df.empty:
            return None

        # Fix for yfinance MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Technical Indicators
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['EMA20'] = ta.ema(df['Close'], length=20)
        df['EMA50'] = ta.ema(df['Close'], length=50)
        
        # Get latest values
        latest_price = float(df['Close'].iloc[-1])
        latest_rsi = float(df['RSI'].iloc[-1])
        ema20_val = float(df['EMA20'].iloc[-1])
        ema50_val = float(df['EMA50'].iloc[-1])
        
        # AI Logic
        signal = "HOLD"
        suggestion = "No clear trend. Wait for RSI to enter extreme zones or EMA crossover."
        
        if latest_rsi < 35 or ema20_val > ema50_val:
            signal = "BUY"
            suggestion = "Indicators suggest bullish momentum. RSI is low or Golden Crossover detected."
        elif latest_rsi > 70 or ema20_val < ema50_val:
            signal = "SELL"
            suggestion = "Indicators suggest bearish pressure. Overbought RSI or Death Crossover detected."

        # Targets
        entry = round(latest_price, 2)
        target = round(entry * 1.05, 2) if signal == "BUY" else round(entry * 0.95, 2)
        sl = round(entry * 0.97, 2) if signal == "BUY" else round(entry * 1.03, 2)
        
        return df, signal, entry, target, sl, suggestion
    except Exception as e:
        st.error(f"Error processing {ticker}: {e}")
        return None

# --- MAIN UI ---
if selected_stock:
    res = get_analysis(selected_stock)
    if res:
        df, signal, price, target, sl, suggestion = res
        
        # Display Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Current Price", f"₹{price}")
        
        # Signal Styling
        color = "green" if signal == "BUY" else "red" if signal == "SELL" else "gray"
        c2.markdown(f"### Signal: <span style='color:{color}'>{signal}</span>", unsafe_allow_html=True)
        
        c3.metric("Target", f"₹{target}")
        c4.metric("Stop Loss", f"₹{sl}")
        
        st.info(f"**AI Logic:** {suggestion}")

        # Chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"))
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name="EMA 20", line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], name="EMA 50", line=dict(color='blue')))
        fig.update_layout(template="plotly_dark", height=500, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("No data found for this symbol. Check if the symbol is correct.")
