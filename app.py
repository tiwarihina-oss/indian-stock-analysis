import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- 1. SETTINGS & NAVIGATION ---
st.set_page_config(page_title="StockPulse AI", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'SBIN.NS']

def nav_to(page):
    st.session_state.page = page
    st.rerun()

# --- 2. THE STYLING (Professional UI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050708 !important; color: white; }
    .main .block-container { padding: 0; max-width: 100%; }
    header { visibility: hidden; }
    
    /* Hero Section */
    .hero-section { background: radial-gradient(circle at 90% 10%, #0d2b1f 0%, #050708 60%); padding: 60px 10%; min-height: 100vh; }
    .hero-title { font-size: 72px; font-weight: 800; line-height: 1.1; margin-bottom: 20px; letter-spacing: -2px; }
    .green-text { color: #00df81; }
    .badge { background: rgba(0, 223, 129, 0.1); color: #00df81; padding: 8px 18px; border-radius: 20px; font-size: 13px; font-weight: 600; display: inline-block; margin-bottom: 20px; }

    /* Dashboard Cards */
    .glass-card { background: #111418; border: 1px solid #1e262c; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
    .stat-label { color: #848e9c; font-size: 13px; font-weight: 500; }
    .stat-value { font-size: 28px; font-weight: 700; margin-top: 5px; }
    
    /* Signal Badges */
    .buy-bg { background: rgba(0, 223, 129, 0.15); color: #00df81; padding: 10px 20px; border-radius: 10px; font-weight: 700; font-size: 20px; }
    .sell-bg { background: rgba(255, 59, 59, 0.15); color: #ff3b3b; padding: 10px 20px; border-radius: 10px; font-weight: 700; font-size: 20px; }

    /* Sidebar Fix */
    section[data-testid="stSidebar"] { background-color: #0b0e11 !important; border-right: 1px solid #1e262c; }

    /* Button Styling */
    div.stButton > button { 
        background-color: #00df81 !important; color: #050708 !important; border: none !important;
        font-weight: 700 !important; padding: 12px 24px !important; border-radius: 8px !important; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
def fetch_safe_data(ticker, period="1y"):
    try:
        df = yf.download(ticker, period=period, interval="1d", progress=False)
        if df.empty: return None
        # Flatten Multi-Index Columns if they exist
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return None

def calculate_ai(df):
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rsi = 100 - (100 / (1 + (gain / loss)))
    
    curr_price = float(df['Close'].iloc[-1])
    curr_rsi = float(rsi.iloc[-1])
    
    signal, color = "HOLD", "#848e9c"
    if curr_rsi < 35: signal, color = "BUY", "#00df81"
    elif curr_rsi > 70: signal, color = "SELL", "#ff3b3b"
    
    return {
        "price": round(curr_price, 2),
        "signal": signal,
        "color": color,
        "target": round(curr_price * 1.05, 2) if signal != "SELL" else round(curr_price * 0.95, 2),
        "sl": round(curr_price * 0.97, 2) if signal != "SELL" else round(curr_price * 1.03, 2),
        "rsi": round(curr_rsi, 2)
    }

# --- 4. PAGE: HOME ---
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown('<div class="badge">⚡ AI-Powered Stock Analysis</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Master the <span class="green-text">Indian Stock</span> Market with AI</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#848e9c; font-size:18px; margin-bottom:40px;">Real-time signals, professional charts, and AI-driven entry/exit points for NSE & BSE stocks.</p>', unsafe_allow_html=True)
        st.button("Go to Dashboard →", key="home_btn", on_click=lambda: nav_to('dashboard'))
    with col2:
        # Minimalistic CSS Mockup
        st.markdown("""
        <div style="background:#111418; border:1px solid #1e262c; border-radius:20px; padding:40px; text-align:center;">
            <p style="color:#848e9c;">Live AI Signal Preview</p>
            <h1 style="color:#00df81; font-size:48px; margin:10px 0;">BUY</h1>
            <p style="font-size:20px; font-weight:700;">RELIANCE INDUSTRIES</p>
            <p style="color:#848e9c; margin-top:20px;">Target: 3,120 | Stop Loss: 2,890</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. PAGE: DASHBOARD ---
else:
    # Navigation Bar
    st.markdown("""
    <div style="padding: 15px 5%; border-bottom: 1px solid #1e262c; display: flex; justify-content: space-between; align-items: center; background:#050708;">
        <h3 style="margin:0; font-weight:800;">🏹 StockPulse <span style="color:#00df81;">Intelligence</span></h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🔍 Search & Watchlist")
        ticker = st.text_input("Enter Ticker (e.g. SBIN, TCS)").upper()
        if st.button("➕ Add Stock"):
            if ticker and f"{ticker}.NS" not in st.session_state.watchlist:
                st.session_state.watchlist.append(f"{ticker}.NS")
                st.rerun()
        
        selected = st.selectbox("Switch Asset", st.session_state.watchlist)
        st.divider()
        st.button("⬅ Back to Home", on_click=lambda: nav_to('home'))

    # DASHBOARD CONTENT
    if selected:
        data = fetch_safe_data(selected)
        if data is not None:
            analysis = calculate_ai(data)
            
            # Row 1: Key Metrics
            st.write("")
            m1, m2, m3, m4 = st.columns(4)
            with m1: st.markdown(f'<div class="glass-card"><p class="stat-label">Price</p><div class="stat-value">₹{analysis["price"]}</div></div>', unsafe_allow_html=True)
            with m2: st.markdown(f'<div class="glass-card"><p class="stat-label">AI Signal</p><div class="{"buy-bg" if analysis["signal"]=="BUY" else "sell-bg" if analysis["signal"]=="SELL" else "hold-bg"}">{analysis["signal"]}</div></div>', unsafe_allow_html=True)
            with m3: st.markdown(f'<div class="glass-card"><p class="stat-label">Target</p><div class="stat-value" style="color:#00df81">₹{analysis["target"]}</div></div>', unsafe_allow_html=True)
            with m4: st.markdown(f'<div class="glass-card"><p class="stat-label">Stop Loss</p><div class="stat-value" style="color:#ff3b3b">₹{analysis["sl"]}</div></div>', unsafe_allow_html=True)

            # Row 2: Chart & Sugges
