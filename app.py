import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="StockPulse AI", layout="wide", initial_sidebar_state="collapsed")

# Navigation Logic
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. THE STYLING (CSS) ---
# We use a separate block for CSS to avoid "code showing on screen" errors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050708 !important;
        color: white;
    }

    .main .block-container { padding: 0; max-width: 100%; }
    header { visibility: hidden; }
    
    /* Hero Section Background */
    .hero-section {
        background: radial-gradient(circle at 90% 10%, #102a1e 0%, #050708 60%);
        padding: 80px 8% 120px 8%;
        min-height: 85vh;
    }

    .logo { font-size: 26px; font-weight: 800; margin-bottom: 60px; display: flex; align-items: center; gap: 10px; }
    .logo span { color: #00c805; }

    .badge {
        background: #102a1e; color: #00c805; padding: 8px 18px; border-radius: 20px;
        font-size: 14px; font-weight: 600; border: 1px solid #1a3d2c; display: inline-block; margin-bottom: 25px;
    }

    .hero-title { font-size: 75px; font-weight: 800; line-height: 1.1; margin-bottom: 25px; letter-spacing: -2px; }
    .green-text { color: #00c805; }
    
    .hero-desc { color: #848e9c; font-size: 19px; max-width: 550px; line-height: 1.6; margin-bottom: 45px; }

    /* Mockup Visual on the right */
    .mockup-img {
        width: 100%; border-radius: 24px; border: 1px solid #1e262c;
        box-shadow: 0 40px 100px rgba(0,0,0,0.6);
    }

    .floating-card {
        background: rgba(16, 22, 26, 0.9); backdrop-filter: blur(12px);
        border: 1px solid #2b3139; border-radius: 16px; padding: 20px;
        position: absolute; bottom: 40px; left: -40px; width: 260px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }

    /* Stats Row */
    .stats-row { display: flex; gap: 100px; margin-top: 60px; }
    .stat-box h3 { font-size: 36px; font-weight: 800; margin: 0; color: white; }
    .stat-box p { color: #848e9c; font-size: 15px; margin-top: 4px; }

    /* Fix Streamlit Buttons to look like the design */
    div.stButton > button {
        background-color: #00c805 !important;
        color: #050708 !important;
        font-weight: 700 !important;
        padding: 15px 40px !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 18px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1: HOME SCREEN
# ==========================================
if st.session_state.page == 'home':
    # Container for Hero Content
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="logo"><span>📈</span> StockPulse</div>', unsafe_allow_html=True)
    
    # Left & Right Layout
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown('<div class="badge">⚡ AI-Powered Stock Analysis</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Master the <span class="green-text">Indian Stock</span> Market with AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-desc">Real-time data from Yahoo Finance, AI-generated trading signals with entry, target, and stop loss prices. Your edge in NSE & BSE markets.</p>', unsafe_allow_html=True)
        
        # NAVIGATION BUTTON
        st.button("Go to Dashboard →", on_click=lambda: navigate_to('dashboard'))
        
        # Stats
        st.markdown("""
        <div class="stats-row">
            <div class="stat-box"><h3>5000+</h3><p>Indian Stocks</p></div>
            <div class="stat-box"><h3>Real-time</h3><p>Market Data</p></div>
            <div class="stat-box"><h3>AI</h3><p>Trading Signals</p></div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="position: relative;">
            <img class="mockup-img" src="https://images.unsplash.com/photo-1611974717537-488439a44484?q=80&w=1000&auto=format&fit=crop">
            <div class="floating-card">
                <p style="color:#848e9c; font-size:12px; margin-bottom:5px;">AI Signal Generated</p>
                <p style="color:#00c805; font-size:20px; font-weight:800; margin:0;">🟢 BUY RELIANCE</p>
                <p style="color:white; font-size:14px; margin-top:5px;">Target: 3,050 | SL: 2,780</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: DASHBOARD
# ==========================================
elif st.session_state.page == 'dashboard':
    # Simple Dashboard Header
    st.markdown("""
    <div style="padding: 20px 5%; border-bottom: 1px solid #1e262c; display: flex; justify-content: space-between; align-items: center;">
        <h2 style="margin:0;">📈 StockPulse Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.button("⬅ Back to Home", on_click=lambda: navigate_to('home'))
    
    # --- Professional Dashboard Content ---
    st.write("")
    c1, c2, c3 = st.columns(3)
    c1.metric("Nifty 50", "22,713.10", "33.70")
    c2.metric("Sensex", "73,319.55", "185.23")
    c3.metric("Bank Nifty", "48,950.20", "-12.40")
    
    st.divider()
    st.info("You are now in the AI Analysis Zone. Search for any Indian stock in the sidebar to begin.")
    
    # (The rest of your stock analyzer code goes here...)
