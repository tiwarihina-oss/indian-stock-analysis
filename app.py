import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. PRO PAGE CONFIG ---
st.set_page_config(page_title="QUANT AI | Indian Market", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CUSTOM CSS (High-End Fintech UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0b0e11; color: white; }
    .stApp { background-color: #0b0e11; }
    
    /* Global Card Style */
    .glass-card { background: #161a1e; border: 1px solid #2b3139; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1c2024; border-radius: 8px; padding: 10px 20px; color: #848e9c; border: none;
    }
    .stTabs [aria-selected="true"] { background-color: #00c805 !important; color: #0b0e11 !important; font-weight: 700; }

    /* Signal Badges */
    .buy-badge { background: #00c80522; color: #00c805; padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 24px; display: inline-block; }
    .sell-badge { background: #ff3b3b22; color: #ff3b3b; padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 24px; display: inline-block; }
    
    /* Metrics */
    .metric-label { color: #848e9c; font-size: 13px; font-weight: 500; margin-bottom: 4px; }
    .metric-value { font-size: 22px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE ANALYTICS ENGINE ---
def get_clean_data(ticker, period="1y"):
    df = yf.download(ticker, period=period, interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    return df

def calculate_ai_signals(df):
    # Technical Logic (Manual for stability)
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    
    last = df.iloc[-1]
    price = float(last['Close'])
    rsi = float(last['RSI'])
    
    # AI Logic
    signal, color, msg = "HOLD", "#848e9c", "Market trend is neutral. Wait for a clear breakout."
    if rsi < 35 or (df['EMA20'].iloc[-2] < df['EMA50'].iloc[-2] and last['EMA20'] > last['EMA50']):
        signal, color, msg = "BUY", "#00c805", "Strong bullish momentum. Indicators suggest an entry point."
    elif rsi > 70 or (df['EMA20'].iloc[-2] > df['EMA50'].iloc[-2] and last['EMA20'] < last['EMA50']):
        signal, color, msg = "SELL", "#ff3b3b", "Overbought zone reached. High probability of profit booking."
    
    return {
        "signal": signal, "color": color, "suggestion": msg,
        "entry": round(price, 2),
        "target": round(price * 1.05, 2) if signal != "SELL" else round(price * 0.95, 2),
        "sl": round(price * 0.97, 2) if signal != "SELL" else round(price * 1.03, 2),
        "rsi": round(rsi, 2)
    }

# --- 4. WATCHLIST & SEARCH ---
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'SBIN.NS', 'HDFCBANK.NS']

with st.sidebar:
    st.markdown("### 🔍 Search Assets")
    new_ticker = st.text_input("Enter Symbol (e.g., INFY)").upper()
    if st.button("➕ Add to Watchlist"):
        if new_ticker:
            st.session_state.watchlist.append(f"{new_ticker}.NS")
            st.rerun()
    
    selected_stock = st.selectbox("Your Watchlist", st.session_state.watchlist)
    if st.button("🗑️ Remove Selected"):
        st.session_state.watchlist.remove(selected_stock)
        st.rerun()

# --- 5. MAIN UI ---
st.markdown("<p style='color:#848e9c; margin-bottom:0;'>QUANT AI Intelligence Suite</p>", unsafe_allow_html=True)
st.title("Indian Stock Market Dashboard")

tabs = st.tabs(["📊 Market Overview", "🎯 AI Stock Analysis"])

# --- TAB 1: MARKET DASHBOARD (Minimalistic) ---
with tabs[0]:
    c1, c2 = st.columns(2)
    
    # Top Index Cards
    for i, (sym, name) in enumerate([("^NSEI", "NIFTY 50"), ("^BSESN", "SENSEX")]):
        d = get_clean_data(sym, period="2d")
        curr = d['Close'].iloc[-1]
        pct = ((curr - d['Close'].iloc[0])/d['Close'].iloc[0])*100
        with [c1, c2][i]:
            st.markdown(f"""
            <div class="glass-card">
                <span style="float:right; color:{'#00c805' if pct>0 else '#ff3b3b'}; font-weight:700;">{'+' if pct>0 else ''}{round(pct,2)}%</span>
                <p style="color:#848e9c; margin:0; font-size:14px;">{name}</p>
                <h2 style="margin:0; font-size:32px;">{round(curr,2):,}</h2>
            </div>
            """, unsafe_allow_html=True)

    # Large Minimalistic Nifty Chart
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**NIFTY 50 Trend**")
    nifty_data = get_clean_data("^NSEI", period="1mo")
    fig_nifty = go.Figure()
    fig_nifty.add_trace(go.Scatter(x=nifty_data.index, y=nifty_data['Close'], fill='tozeroy', fillcolor='rgba(0, 200, 5, 0.05)', line=dict(color='#00c805', width=3)))
    fig_nifty.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0), height=300, xaxis_visible=False, yaxis_gridcolor='#21262c')
    st.plotly_chart(fig_nifty, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Sector Heatmap (Minimalist Progress Bars)
    st.markdown("### Sector Performance")
    sectors = [("IT", 2.1), ("Banking", 1.4), ("Auto", -0.5), ("Pharma", 0.8), ("Metal", -1.2)]
    scols = st.columns(len(sectors))
    for i, (name, chg) in enumerate(sectors):
        color = "#00c805" if chg > 0 else "#ff3b3b"
        scols[i].markdown(f"""
        <div style="background:#161a1e; padding:15px; border-radius:12px; border-bottom: 4px solid {color}">
            <p style="color:#848e9c; margin:0; font-size:12px;">{name}</p>
            <p style="margin:0; font-weight:700;">{'+' if chg>0 else ''}{chg}%</p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: AI STOCK ANALYSIS (Detailed & Clean) ---
with tabs[1]:
    if selected_stock:
        with st.spinner("AI is calculating signals..."):
            df_stock = get_clean_data(selected_stock)
            analysis = calculate_ai_signals(df_stock)
            
            # 1. Top Signal Card
            st.markdown(f"""
            <div class="glass-card" style="border-left: 8px solid {analysis['color']};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <p class="metric-label">AI RECOMMENDATION FOR {selected_stock}</p>
                        <div class="{'buy-badge' if analysis['signal']=='BUY' else 'sell-badge' if analysis['signal']=='SELL' else 'hold-signal'}">{analysis['signal']}</div>
                    </div>
                    <div style="text-align:right">
                        <p class="metric-label">ENTRY PRICE</p>
                        <div class="metric-value">₹{analysis['entry']}</div>
                    </div>
                </div>
                <p style="margin-top:20px; color:#d1d4dc;"><b>AI Suggestion:</b> {analysis['suggestion']}</p>
            </div>
            """, unsafe_allow_html=True)

            # 2. Target & SL Row
            tcol1, tcol2, tcol3 = st.columns(3)
            with tcol1: st.markdown(f'<div class="glass-card"><p class="metric-label">🎯 AI Target</p><div class="metric-value" style="color:#00c805">₹{analysis["target"]}</div></div>', unsafe_allow_html=True)
            with tcol2: st.markdown(f'<div class="glass-card"><p class="metric-label">🛡️ Stop Loss</p><div class="metric-value" style="color:#ff3b3b">₹{analysis["sl"]}</div></div>', unsafe_allow_html=True)
            with tcol3: st.markdown(f'<div class="glass-card"><p class="metric-label">📉 RSI (14)</p><div class="metric-value">{analysis["rsi"]}</div></div>', unsafe_allow_html=True)

            # 3. Minimalist Candlestick Chart
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"**{selected_stock} Technical Chart**")
            
            fig = make_subplots(rows=1, cols=1)
            fig.add_trace(go.Candlestick(
                x=df_stock.index, open=df_stock['Open'], high=df_stock['High'], low=df_stock['Low'], close=df_stock['Close'],
                increasing_line_color='#00c805', decreasing_line_color='#ff3b3b', name="Price"
            ))
            fig.add_trace(go.Scatter(x=df_stock.index, y=df_stock['EMA20'], name="EMA 20", line=dict(color='#2962ff', width=1.5)))
            
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0,r=0,t=0,b=0), height=500, xaxis_rangeslider_visible=False,
                xaxis_showgrid=False, yaxis_gridcolor='#21262c', yaxis_side="right"
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)
