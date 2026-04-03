import streamlit as st
import yfinance as yf
import pandas as pd

# --- 1. PRO PAGE CONFIG ---
st.set_page_config(page_title="StockPulse AI", layout="wide", initial_sidebar_state="collapsed")

# Navigation Logic
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. THE STYLING (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    /* Deep Black Theme */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050708 !important;
        color: white;
    }

    .main .block-container { padding: 0; max-width: 100%; }
    header { visibility: hidden; }
    
    /* Hero Section with Green Glow */
    .hero-section {
        background: radial-gradient(circle at 85% 15%, #0d2b1f 0%, #050708 55%);
        padding: 40px 8% 100px 8%;
        min-height: 100vh;
    }

    /* Top Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 80px;
    }
    
    .logo { 
        font-size: 24px; 
        font-weight: 800; 
        display: flex; 
        align-items: center; 
        gap: 10px; 
        letter-spacing: -0.5px;
    }
    .logo span { 
        color: #00df81; 
        background: rgba(0, 223, 129, 0.15); 
        padding: 6px; 
        border-radius: 8px;
    }

    /* Badge */
    .badge {
        background: rgba(0, 223, 129, 0.1); 
        color: #00df81; 
        padding: 8px 18px; 
        border-radius: 20px;
        font-size: 13px; 
        font-weight: 600; 
        border: 1px solid rgba(0, 223, 129, 0.2); 
        display: inline-block; 
        margin-bottom: 30px;
    }

    /* Typography */
    .hero-title { font-size: 72px; font-weight: 800; line-height: 1.1; margin-bottom: 25px; letter-spacing: -2px; }
    .green-text { color: #00df81; }
    .hero-desc { color: #848e9c; font-size: 18px; max-width: 500px; line-height: 1.6; margin-bottom: 45px; }

    /* Mockup Visual */
    .mockup-container { position: relative; }
    .mockup-img {
        width: 100%; 
        border-radius: 20px; 
        border: 1px solid #1e262c;
        box-shadow: 0 50px 100px rgba(0,0,0,0.8);
        mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 80%, rgba(0,0,0,0));
    }

    .floating-card {
        background: rgba(11, 16, 19, 0.85); 
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.1); 
        border-radius: 16px; 
        padding: 20px;
        position: absolute; 
        bottom: 50px; 
        left: -30px; 
        width: 250px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.6);
    }

    /* Stats Row */
    .stats-row { display: flex; gap: 60px; margin-top: 60px; }
    .stat-box h3 { font-size: 32px; font-weight: 800; margin: 0; color: #ffffff; }
    .stat-box p { color: #848e9c; font-size: 14px; margin-top: 4px; }

    /* Buttons Styling */
    div.stButton > button {
        background-color: #00df81 !important;
        color: #050708 !important;
        font-weight: 700 !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        border: none !important;
        font-size: 16px !important;
        transition: 0.3s all ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 223, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1: HOME SCREEN
# ==========================================
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    # 1. NAVBAR
    nav_col1, nav_col2 = st.columns([1, 1])
    with nav_col1:
        st.markdown('<div class="logo"><span>📈</span> StockPulse</div>', unsafe_allow_html=True)
    with nav_col2:
        # TOP RIGHT BUTTON
        st.button("Go to Dashboard →", key="top_nav_btn", on_click=lambda: navigate_to('dashboard'))
    
    # 2. HERO SECTION
    col_left, col_right = st.columns([1.1, 1])
    
    with col_left:
        st.markdown('<div class="badge">⚡ AI-Powered Stock Analysis</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Master the <span class="green-text">Indian Stock</span> Market with AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-desc">Real-time data from Yahoo Finance, AI-generated trading signals with entry, target, and stop loss prices. Your edge in NSE & BSE markets.</p>', unsafe_allow_html=True)
        
        # MAIN HERO BUTTON
        st.button("Go to Dashboard →", key="hero_btn", on_click=lambda: navigate_to('dashboard'))
        
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
        <div class="mockup-container">
            <img class="mockup-img" src="https://images.unsplash.com/photo-1642790106117-e829e14a795f?q=80&w=1200&auto=format&fit=crop">
            <div class="floating-card">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <span style="background:rgba(0, 223, 129, 0.2); padding:6px; border-radius:50%; font-size:14px;">🎯</span>
                    <span style="color:#848e9c; font-size:12px;">AI Signal</span>
                </div>
                <p style="color:#00df81; font-size:18px; font-weight:800; margin:0;">BUY RELIANCE</p>
                <p style="color:white; font-size:13px; margin-top:5px; opacity:0.8;">Target: 3,050 | SL: 2,780</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: DASHBOARD
# ==========================================
elif st.session_state.page == 'dashboard':
    st.markdown("""
    <div style="padding: 25px 8%; border-bottom: 1px solid #1e262c; display: flex; justify-content: space-between; align-items: center; background:#050708;">
        <h2 style="margin:0; font-weight:800; color:#00df81;">📈 StockPulse Analytics</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.button("⬅ Back to Home", on_click=lambda: navigate_to('home'))
    
    # Dashboard Content
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="background:#111518; padding:30px; border-radius:15px; border:1px solid #1e262c;"><h3>NIFTY 50</h3><h1>22,713.10</h1><p style="color:#00df81">↗ +0.15%</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="background:#111518; padding:30px; border-radius:15px; border:1px solid #1e262c;"><h3>SENSEX</h3><h1>73,319.55</h1><p style="color:#00df81">↗ +0.25%</p></div>', unsafe_allow_html=True)

    st.success("Analysis Engine is online. Use the sidebar to search for Indian stocks.")
