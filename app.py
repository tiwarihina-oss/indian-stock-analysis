import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- PAGE SETUP ---
st.set_page_config(page_title="Market Overview", layout="wide", initial_sidebar_state="collapsed")

# --- CSS: THE "DITTO" STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Background & Global */
    .stApp { background-color: #0b0e11; font-family: 'Inter', sans-serif; color: #ffffff; }
    header {visibility: hidden;}
    .main .block-container { padding: 2rem; }

    /* Card Layout */
    .glass-card {
        background: #161a1e;
        border: 1px solid #2b3139;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 15px;
    }

    /* Index Headers */
    .icon-box { background: #00c8051a; border-radius: 8px; padding: 10px; display: inline-flex; align-items: center; justify-content: center; margin-right: 12px; }
    .index-label { color: #ffffff; font-weight: 600; font-size: 14px; }
    .index-price { font-size: 32px; font-weight: 700; margin-top: 10px; margin-bottom: 0px; }
    .index-delta { font-size: 16px; font-weight: 500; }
    .pct-badge { background: #00c8051a; color: #00c805; padding: 4px 10px; border-radius: 6px; font-size: 14px; font-weight: 600; float: right; }
    
    /* Small Stat Boxes */
    .stat-label { color: #848e9c; font-size: 13px; margin-bottom: 8px; font-weight: 500; }
    .stat-value { font-size: 22px; font-weight: 700; color: #ffffff; }

    /* Time Range Buttons */
    .time-btn-container { display: flex; gap: 10px; margin: 20px 0; }
    .time-btn { background: transparent; border: none; color: #848e9c; font-size: 13px; font-weight: 600; cursor: pointer; padding: 5px 10px; }
    .time-btn.active { background: #00c805; color: #0b0e11; border-radius: 6px; }

    /* Sector Sidebar */
    .sector-title { font-size: 18px; font-weight: 600; margin-bottom: 5px; display: flex; align-items: center; gap: 8px;}
    .sector-summary { color: #848e9c; font-size: 13px; margin-bottom: 25px; }
    .sector-row { display: flex; align-items: center; margin-bottom: 20px; }
    .sector-icon { background: #21262c; border-radius: 8px; padding: 8px; margin-right: 12px; min-width: 40px; text-align: center; }
    .sector-info { flex-grow: 1; }
    .sector-name { font-size: 14px; font-weight: 600; }
    .sector-bar-bg { background: #2b3139; height: 6px; border-radius: 3px; margin-top: 8px; width: 100%; }
    .sector-bar-fill { height: 100%; border-radius: 3px; background: #00c805; }
    .sector-val-group { text-align: right; margin-left: 15px; }
    .sector-val { font-size: 13px; color: #848e9c; display: block; }
    .sector-pct { font-size: 13px; color: #00c805; font-weight: 600; }

    /* Colors */
    .pos { color: #00c805; }
    .neg { color: #ff3b3b; }
</style>
""", unsafe_allow_html=True)

# --- HELPER DATA ---
@st.cache_data(ttl=60)
def get_nifty_chart():
    df = yf.download("^NSEI", period="1mo", interval="1d", progress=False)
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    return df

# --- UI LAYOUT ---

st.markdown("<p style='color:#848e9c; font-size:14px; margin-bottom:20px;'>Indian Stock Market Overview powered by Yahoo Finance</p>", unsafe_allow_html=True)

# ROW 1: TOP INDICES
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="glass-card">
        <span class="pct-badge">↗ +0.15%</span>
        <div class="icon-box">📊</div> <span class="index-label">NIFTY 50</span>
        <div class="index-price">22,713.10</div>
        <div class="index-delta pos">+33.70</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card">
        <span class="pct-badge">↗ +0.25%</span>
        <div class="icon-box">📈</div> <span class="index-label">SENSEX</span>
        <div class="index-price">73,319.55</div>
        <div class="index-delta pos">+185.23</div>
    </div>
    """, unsafe_allow_html=True)

# ROW 2: SMALL STATS
s1, s2, s3, s4 = st.columns(4)
stats = [("Total Volume", "9.22 Cr"), ("Market Cap", "5093470.86 Cr"), ("Advancing", "5"), ("Declining", "3")]
for i, col in enumerate([s1, s2, s3, s4]):
    col.markdown(f"""
    <div class="glass-card" style="padding: 20px;">
        <div class="stat-label">{stats[i][0]}</div>
        <div class="stat-value">{stats[i][1]}</div>
    </div>
    """, unsafe_allow_html=True)

# ROW 3: CHART & SECTOR PERFORMANCE
st.write("")
l_col, r_col = st.columns([2.2, 1])

with l_col:
    st.markdown("""
    <div class="glass-card" style="height: 600px;">
        <span class="pct-badge" style="margin-top:5px;">↗ +0.15%</span>
        <div class="icon-box" style="padding:6px;">📊</div> <span class="index-label">NIFTY 50</span>
        <div class="index-price" style="font-size:24px; margin-top:5px;">22,713.10</div>
        
        <div class="time-btn-container">
            <button class="time-btn">1D</button>
            <button class="time-btn">5D</button>
            <button class="time-btn active">1M</button>
            <button class="time-btn">3M</button>
            <button class="time-btn">6M</button>
            <button class="time-btn">1Y</button>
        </div>
    """, unsafe_allow_html=True)
    
    # Large Chart
    df = get_nifty_chart()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'], 
        fill='tozeroy', fillcolor='rgba(0, 200, 5, 0.05)',
        line=dict(color='#00c805', width=3),
        hovertemplate="Price: ₹%{y:,.2f}<extra></extra>"
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=20, b=0), height=380,
        xaxis=dict(showgrid=False, showline=False, color="#848e9c"),
        yaxis=dict(showgrid=True, gridcolor='#21262c', position=1, side="left", color="#848e9c")
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with r_col:
    st.markdown("""
    <div class="glass-card" style="height: 600px;">
        <div class="sector-title">⌛ Sector Performance</div>
        <div class="sector-summary">🟢 5 gaining &nbsp;🔴 6 declining</div>
    """, unsafe_allow_html=True)
    
    sectors = [
        ("IT", "30,441.45", "+2.60%", 90, "💻"),
        ("Realty", "672.10", "+1.07%", 40, "🏢"),
        ("Metal", "11,456.60", "+0.39%", 30, "🔨"),
        ("FMCG", "46,232.15", "+0.21%", 15, "🛒"),
        ("Banking", "51,548.75", "+0.19%", 12, "🏦")
    ]
    
    for name, val, pct, width, icon in sectors:
        st.markdown(f"""
        <div class="sector-row">
            <div class="sector-icon">{icon}</div>
            <div class="sector-info">
                <span class="sector-name">{name}</span>
                <div class="sector-bar-bg"><div class="sector-bar-fill" style="width: {width}%;"></div></div>
            </div>
            <div class="sector-val-group">
                <span class="sector-val">{val}</span>
                <span class="sector-pct">{pct}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
