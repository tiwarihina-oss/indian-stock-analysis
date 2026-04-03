import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Indian Stock Signal", layout="wide")

st.title("📈 AI Indian Stock Signal Pro")
st.caption("Stable Version - Powered by Real-time NSE/BSE Data")

# --- INDICATOR CALCULATIONS (Manual to avoid errors) ---
def calculate_indicators(df):
    # Calculate EMA
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    
    # Calculate RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# --- SESSION STATE FOR WATCHLIST ---
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔍 Search Stock")
    ticker_input = st.text_input("Symbol (e.g., SBIN, TATAMOTORS)").upper()
    exch = st.radio("Exchange", ["NSE", "BSE"])
    
    if st.button("Add to Watchlist"):
        if ticker_input:
            suffix = ".NS" if exch == "NSE" else ".BO"
            full_ticker = ticker_input + suffix
            if full_ticker not in st.session_state.watchlist:
                st.session_state.watchlist.append(full_ticker)
                st.rerun()

    selected_stock = st.selectbox("Select from Watchlist", st.session_state.watchlist)
    
    if st.button("Remove Selected"):
        st.session_state.watchlist.remove(selected_stock)
        st.rerun()

# --- MAIN APP LOGIC ---
if selected_stock:
    try:
        # Fetch Data
        data = yf.download(selected_stock, period="1y", interval="1d", progress=False)
        
        if data.empty:
            st.error("No data found. Please check the ticker symbol.")
        else:
            # Clean data (fix for yfinance multi-index)
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            # Calculate Technicals
            df = calculate_indicators(data)
            
            # Get latest values for AI Signal
            last_row = df.iloc[-1]
            prev_row = df.iloc[-2]
            curr_price = float(last_row['Close'])
            rsi_val = float(last_row['RSI'])
            ema20 = float(last_row['EMA20'])
            ema50 = float(last_row['EMA50'])

            # AI Signal Logic
            signal = "HOLD"
            color = "#f0f0f0" # gray
            suggestion = "Market is neutral. Avoid fresh entry."

            if rsi_val < 35 or (prev_row['EMA20'] < prev_row['EMA50'] and ema20 > ema50):
                signal = "BUY"
                color = "#00FF00" # green
                suggestion = "Bullish momentum detected. Price is showing strength."
            elif rsi_val > 70 or (prev_row['EMA20'] > prev_row['EMA50'] and ema20 < ema50):
                signal = "SELL"
                color = "#FF4B4B" # red
                suggestion = "Overbought conditions. High risk of profit booking."

            # Entry/Target/SL
            entry_price = round(curr_price, 2)
            target = round(entry_price * 1.05, 2) if signal != "SELL" else round(entry_price * 0.95, 2)
            stop_loss = round(entry_price * 0.97, 2) if signal != "SELL" else round(entry_price * 1.03, 2)

            # Display UI
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Current Price", f"₹{entry_price}")
            m2.markdown(f"### <span style='color:{color}'>{signal}</span>", unsafe_allow_html=True)
            m3.metric("Target", f"₹{target}")
            m4.metric("Stop Loss", f"₹{stop_loss}")

            st.info(f"**AI Suggestion:** {suggestion}")

            # Candlestick Chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Price"))
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name="EMA 20", line=dict(color='orange', width=1.5)))
            fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], name="EMA 50", line=dict(color='blue', width=1.5)))
            
            fig.update_layout(template="plotly_dark", height=600, margin=dict(l=10, r=10, t=30, b=10), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
