import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(page_title="Indian Market Intelligence", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS FOR HIGH-END UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0b0e11; color: white; }
    
    /* Card Styling */
    .metric-card {
        background-color: #161a1e;
        border: 1px solid #2b3139;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 10px;
    }
    .index-title { color: #848e9c; font-size: 14px; font-weight: 600; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
    .index-value { font-size: 28px; font-weight: 700; margin: 0; }
    .index-delta { font-size: 16px; margin-top: 4px; }
    .positive { color: #00c805; }
    .negative { color: #ff3b3b; }
    
    /* Small Stat Cards */
    .stat-card { background-color: #161a1e; border: 1px solid #21262c; border-radius: 12px; padding: 15px; height: 100%; }
    .stat-label { color: #848e9c; font-size: 12px; margin-bottom: 5px; }
    .stat-value { font-size: 18px; font-weight: 600; }

    /* Sector Progress Bars */
    .sector-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
    .progress-bg { background-color: #2b3139; border-radius: 4px; height: 6px; width: 100%; margin-top: 8px; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 4px; }

    /* Buttons */
    .stButton>button { 
        background-color: #1e222d; border: none; color: #848e9c; border-radius: 6px; 
        padding: 4px 12px; font-size: 12px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #2962ff; color: white; }
</style>
""", unsafe_allow_html=True)

# --- DATA FETCHING ---
@st.cache_data(ttl=60)
def get_market_data(ticker, period="1mo", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    return df

# --- MAIN DASHBOARD LAYOUT ---
st.write("Indian Stock Market Overview powered by Yahoo Finance")

# TOP ROW: MAIN INDICES
t1, t2 = st.columns(2)

indices = [("^NSEI", "NIFTY 50"), ("^BSESN", "SENSEX")]
for i, col in enumerate([t1, t2]):
    data = get_market_data(indices[i][0], period="2d", interval="1m")
    if not data.empty:
        curr = data['Close'].iloc[-1]
        prev = data['Close'].iloc[0]
        diff = curr - prev
        pct = (diff / prev) * 100
        cls = "positive" if diff >= 0 else "negative"
        sign = "+" if diff >= 0 else ""
        
        col.markdown(f"""
        <div class="metric-card">
            <div class="index-title"><span style="background:#00c80522; padding:4px; border-radius:4px;">📊</span> {indices[i][1]} <span style="margin-left:auto; background:#00c80522; color:#00c805; padding:2px 8px; border-radius:6px; font-size:12px;">↗ {sign}{round(pct,2)}%</span></div>
            <div class="index-value">{round(curr,2):,}</div>
            <div class="index-delta {cls}">{sign}{round(diff,2)}</div>
        </div>
        """, unsafe_allow_html=True)

# SECOND ROW: SMALL STATS
s1, s2, s3, s4 = st.columns(4)
stats = [
    ("Total Volume", "9.22 Cr"),
    ("Market Cap", "509.34 L Cr"),
    ("Advancing", "32"),
    ("Declining", "18")
]
for i, col in enumerate([s1, s2, s3, s4]):
    col.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">{stats[i][0]}</div>
        <div class="stat-value">{stats[i][1]}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer

# THIRD ROW: MAIN CHART & SECTORS
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown('<div class="metric-card" style="height:550px">', unsafe_allow_html=True)
    
    # Chart Header
    ch1, ch2 = st.columns([1, 2])
    ch1.markdown(f"**NIFTY 50**<br><span style='font-size:20px; font-weight:700;'>22,713.10</span> <span class='positive' style='font-size:12px;'>↗ +0.15%</span>", unsafe_allow_html=True)
    
    # Time Selectors
    time_period = ch2.segmented_control("Period", options=["1D", "5D", "1M", "3M", "6M", "1Y"], default="1M", label_visibility="collapsed")
    
    # Fetch Nifty Chart Data
    period_map = {"1D":"1d", "5D":"5d", "1M":"1mo", "3M":"3mo", "6M":"6mo", "1Y":"1y"}
    chart_data = get_market_data("^NSEI", period=period_map[time_period], interval="1h" if time_period != "1D" else "5m")
    
    # Plotly Smooth Area Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chart_data.index, y=chart_data['Close'],
        fill='tozeroy', fillcolor='rgba(0, 200, 5, 0.1)',
        line=dict(color='#00c805', width=3),
        mode='lines',
        hovertemplate="Price: ₹%{y:,.2f}<extra></extra>"
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0), height=400,
        xaxis=dict(showgrid=False, showline=False, showticklabels=True),
        yaxis=dict(showgrid=True, gridcolor='#21262c', side="right"),
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="metric-card" style="height:550px">', unsafe_allow_html=True)
    st.markdown("🕒 **Sector Performance**", unsafe_allow_html=True)
    st.markdown("<span style='font-size:12px; color:#848e9c;'>● 5 gaining  ● 6 declining</span>", unsafe_allow_html=True)
    st.write("")
    
    sectors = [
        ("IT", 2.60, "💻"),
        ("Realty", 1.07, "🏢"),
        ("Metal", 0.39, "🔨"),
        ("FMCG", 0.21, "🛒"),
        ("Banking", 0.19, "🏦"),
        ("Auto", -0.45, "🚗"),
        ("Pharma", -0.82, "💊")
    ]
    
    for name, chg, icon in sectors:
        color = "#00c805" if chg > 0 else "#ff3b3b"
        width = min(abs(chg) * 20, 100) # Scaling for visual
        st.markdown(f"""
        <div class="sector-row">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="background:#2b3139; padding:8px; border-radius:8px;">{icon}</span>
                <span style="font-weight:600; font-size:14px;">{name}</span>
            </div>
            <div style="text-align:right;">
                <span style="font-size:12px; font-weight:700; color:{color};">{"+" if chg>0 else ""}{chg}%</span>
                <div class="progress-bg"><div class="progress-fill" style="width:{width}%; background-color:{color};"></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- AI ANALYZER TAB (Optional Sidebar integration) ---
with st.sidebar:
    st.title("🎯 AI Analyzer")
    st.info("Enter a stock symbol below to get AI Buy/Sell signals with Target & Stop Loss.")
    symbol = st.text_input("Symbol (e.g. RELIANCE)").upper()
    if symbol:
        st.write(f"Analyzing {symbol}...")
        # (Insert the AI Logic from previous code here if needed)
