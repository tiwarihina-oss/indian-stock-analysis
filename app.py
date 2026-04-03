import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PRO PAGE CONFIG ---
st.set_page_config(page_title="QUANT | AI Stock Intelligence", layout="wide", initial_sidebar_state="collapsed")

# --- PROFESSIONAL STYLING (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0b0e11; }
    .stMetric { background-color: #161a1e; border: 1px solid #2b3139; padding: 20px; border-radius: 12px; }
    
    /* Custom Card Style */
    .signal-card {
        background: linear-gradient(135deg, #1e222d 0%, #131722 100%);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #363c4e;
        margin-bottom: 20px;
    }
    
    .buy-signal { color: #00ff88; font-weight: 600; font-size: 24px; }
    .sell-signal { color: #ff3b3b; font-weight: 600; font-size: 24px; }
    .hold-signal { color: #848e9c; font-weight: 600; font-size: 24px; }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e222d;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 25px;
        color: #848e9c;
    }
    .stTabs [aria-selected="true"] { background-color: #2962ff !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
@st.cache_data(ttl=60)
def fetch_data(ticker, period="1y", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

def get_ai_analysis(df):
    # Technicals
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    
    latest = df.iloc[-1]
    price = float(latest['Close'])
    rsi = float(latest['RSI'])
    
    # Logic
    if rsi < 35:
        signal, color, desc = "STRONG BUY", "#00ff88", "Oversold conditions detected. High probability of reversal."
    elif rsi > 70:
        signal, color, desc = "STRONG SELL", "#ff3b3b", "Overbought territory. Profit booking expected."
    elif latest['EMA20'] > latest['EMA50']:
        signal, color, desc = "BULLISH HOLD", "#00ff88", "Golden crossover active. Trend is upward."
    else:
        signal, color, desc = "NEUTRAL", "#848e9c", "Market consolidation. Wait for breakout."
        
    return {
        "signal": signal, "color": color, "desc": desc,
        "entry": round(price, 2),
        "target": round(price * 1.05, 2),
        "sl": round(price * 0.97, 2)
    }

# --- UI COMPONENTS ---
def draw_chart(df, name):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.7, 0.3])
    
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        name="Price", increasing_line_color='#26a69a', decreasing_line_color='#ef5350',
        increasing_fillcolor='#26a69a', decreasing_fillcolor='#ef5350'
    ), row=1, col=1)
    
    # EMAs
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], line=dict(color='#2962ff', width=1.5), name="EMA 20"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], line=dict(color='#ff9800', width=1.5), name="EMA 50"), row=1, col=1)
    
    # Volume
    colors = ['#26a69a' if row['Open'] < row['Close'] else '#ef5350' for index, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name="Volume", opacity=0.5), row=2, col=1)
    
    fig.update_layout(
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=600,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#2b3139')
    return fig

# --- APP LAYOUT ---
st.title("🏹 QUANT AI Intelligence")

tab_dash, tab_ai = st.tabs(["🏛️ Market Dashboard", "🎯 AI Stock Signals"])

# WATCHLIST (SIDEBAR)
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']

with st.sidebar:
    st.header("Watchlist")
    ticker = st.text_input("Add Symbol (e.g. SBIN)").upper()
    if st.button("➕ Add to List"):
        if ticker: st.session_state.watchlist.append(f"{ticker}.NS"); st.rerun()
    
    selected_stock = st.selectbox("Switch View", st.session_state.watchlist)
    if st.button("🗑️ Remove"):
        st.session_state.watchlist.remove(selected_stock); st.rerun()

# TAB 1: MARKET DASHBOARD
with tab_dash:
    c1, c2, c3 = st.columns(3)
    indices = [("^NSEI", "NIFTY 50"), ("^NSEBANK", "BANK NIFTY"), ("^BSESN", "SENSEX")]
    
    for i, (sym, name) in enumerate(indices):
        d = fetch_data(sym, period="2d", interval="1m")
        if not d.empty:
            price = d['Close'].iloc[-1]
            diff = price - d['Close'].iloc[0]
            pct = (diff / d['Close'].iloc[0]) * 100
            with [c1, c2, c3][i]:
                st.markdown(f"""
                <div class="stMetric">
                    <p style='color:#848e9c; margin:0;'>{name}</p>
                    <h2 style='margin:0;'>{round(price,2)}</h2>
                    <p style='color:{"#00ff88" if diff>0 else "#ff3b3b"}; margin:0;'>
                        {"▲" if diff>0 else "▼"} {round(pct,2)}%
                    </p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("### Sector Rotation (Heatmap)")
    sectors = {"IT": "^CNXIT", "Bank": "^NSEBANK", "Auto": "^CNXAUTO", "Pharma": "^CNXPHARMA", "Metal": "^CNXMETAL", "FMCG": "^CNXFMCG"}
    sec_cols = st.columns(len(sectors))
    for i, (name, sym) in enumerate(sectors.items()):
        sd = fetch_data(sym, period="5d")
        chg = ((sd['Close'].iloc[-1] - sd['Close'].iloc[-2])/sd['Close'].iloc[-2])*100
        sec_cols[i].markdown(f"""
        <div style='text-align:center; padding:10px; background:#161a1e; border-radius:8px; border-bottom:3px solid {"#00ff88" if chg>0 else "#ff3b3b"}'>
            <small style='color:#848e9c'>{name}</small><br>
            <b>{round(chg,2)}%</b>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: AI ANALYZER
with tab_ai:
    if selected_stock:
        data = fetch_data(selected_stock)
        analysis = get_ai_analysis(data)
        
        # Signal Header Card
        st.markdown(f"""
        <div class="signal-card">
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <h4 style='margin:0; color:#848e9c;'>AI ANALYTICS: {selected_stock}</h4>
                    <h1 style='margin:0; color:{analysis['color']}'>{analysis['signal']}</h1>
                </div>
                <div style='text-align:right'>
                    <p style='margin:0; color:#848e9c;'>Entry Price</p>
                    <h2 style='margin:0;'>₹{analysis['entry']}</h2>
                </div>
            </div>
            <p style='margin-top:15px; color:#d1d4dc; font-size:1.1em;'>{analysis['desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Target Cards
        col_t1, col_t2 = st.columns(2)
        col_t1.markdown(f"""
            <div style='background:#1e222d; padding:20px; border-radius:12px; border-left:5px solid #00ff88'>
                <p style='color:#848e9c; margin:0;'>AI Target Price</p>
                <h2 style='color:#00ff88; margin:0;'>₹{analysis['target']}</h2>
            </div>
        """, unsafe_allow_html=True)
        col_t2.markdown(f"""
            <div style='background:#1e222d; padding:20px; border-radius:12px; border-left:5px solid #ff3b3b'>
                <p style='color:#848e9c; margin:0;'>Safety Stop Loss</p>
                <h2 style='color:#ff3b3b; margin:0;'>₹{analysis['sl']}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Technical Chart
        st.plotly_chart(draw_chart(data, selected_stock), use_container_width=True)
