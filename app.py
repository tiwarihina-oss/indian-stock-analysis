import streamlit as st
import yfinance as yf

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
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050708 !important;
        color: white;
    }

    .main .block-container { padding: 0; max-width: 100%; }
    header { visibility: hidden; }
    
    /* Hero Section with Emerald Glow */
    .hero-section {
        background: radial-gradient(circle at 90% 10%, #0d2b1f 0%, #050708 60%);
        padding: 20px 10% 80px 10%;
        min-height: 100vh;
    }

    .nav-bar { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; margin-bottom: 40px; }
    .logo { font-size: 24px; font-weight: 800; display: flex; align-items: center; gap: 10px; }
    .logo span { color: #00df81; background: rgba(0, 223, 129, 0.1); padding: 6px; border-radius: 8px; }

    .badge {
        background: rgba(0, 223, 129, 0.1); color: #00df81; padding: 8px 18px; border-radius: 20px;
        font-size: 13px; font-weight: 600; border: 1px solid rgba(0, 223, 129, 0.2); 
        display: inline-block; margin-bottom: 30px;
    }

    .hero-title { font-size: clamp(40px, 5vw, 72px); font-weight: 800; line-height: 1.1; margin-bottom: 25px; letter-spacing: -2px; }
    .green-text { color: #00df81; }
    .hero-desc { color: #848e9c; font-size: 18px; max-width: 500px; line-height: 1.6; margin-bottom: 45px; }

    /* Mockup Visual Wrapper */
    .mockup-wrapper { position: relative; width: 100%; height: auto; }
    
    /* Floating AI Signal Card */
    .floating-card {
        background: rgba(11, 16, 19, 0.95); 
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1); 
        border-radius: 16px; padding: 22px;
        position: absolute; 
        bottom: 40px; 
        left: -30px; 
        width: 260px; 
        box-shadow: 0 30px 60px rgba(0,0,0,0.8);
        z-index: 99;
    }

    .stats-row { display: flex; gap: 60px; margin-top: 60px; }
    .stat-box h3 { font-size: 32px; font-weight: 800; margin: 0; }
    .stat-box p { color: #848e9c; font-size: 14px; margin-top: 5px; }

    .footer-text { text-align: center; font-size: 36px; font-weight: 800; margin-top: 80px; padding-bottom: 50px; }

    /* Fix Streamlit's Native Image Border/Padding */
    [data-testid="stImage"] img { border-radius: 24px; border: 1px solid #1e262c; }

    /* Primary Button Style */
    div.stButton > button {
        background-color: #00df81 !important; color: #050708 !important;
        font-weight: 700 !important; padding: 14px 32px !important;
        border-radius: 10px !important; border: none !important;
        font-size: 16px !important; width: fit-content !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1: HOME SCREEN
# ==========================================
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    # 1. NAVBAR
    nav_l, nav_r = st.columns([1, 1])
    with nav_l:
        st.markdown('<div class="logo"><span>📈</span> StockPulse</div>', unsafe_allow_html=True)
    with nav_r:
        _, btn_c = st.columns([2, 1])
        btn_c.button("Go to Dashboard →", key="nav_btn", on_click=lambda: navigate_to('dashboard'))
    
    # 2. HERO AREA
    col_text, col_img = st.columns([1.1, 1], gap="large")
    
    with col_text:
        st.markdown('<div class="badge">⚡ AI-Powered Stock Analysis</div>', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title">Master the <span class="green-text">Indian Stock</span> Market with AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-desc">Real-time data from Yahoo Finance, AI-generated trading signals with entry, target, and stop loss prices.</p>', unsafe_allow_html=True)
        
        st.button("Go to Dashboard →", key="hero_main_btn", on_click=lambda: navigate_to('dashboard'))
        
        st.markdown("""
        <div class="stats-row">
            <div class="stat-box"><h3>5000+</h3><p>Indian Stocks</p></div>
            <div class="stat-box"><h3>Real-time</h3><p>Market Data</p></div>
            <div class="stat-box"><h3>AI</h3><p>Trading Signals</p></div>
        </div>
        """, unsafe_allow_html=True)

    with col_img:
        # We use a wrapper div to contain the image and the floating card
        st.markdown('<div class="mockup-wrapper">', unsafe_allow_html=True)
        
        # Native Streamlit Image (Most stable way to show images)
        st.image("https://images.unsplash.com/photo-1611974717537-488439a44484?auto=format&fit=crop&q=80&w=1000", use_container_width=True)
        
        # Overlay the Floating Card using HTML
        st.markdown("""
            <div class="floating-card">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                    <span style="background:rgba(0, 223, 129, 0.2); padding:5px; border-radius:50%;">🎯</span>
                    <span style="color:#848e9c; font-size:12px;">AI Signal</span>
                </div>
                <p style="color:#00df81; font-size:18px; font-weight:800; margin:0;">BUY RELIANCE</p>
                <p style="color:white; font-size:13px; margin-top:5px;">Target: 3,050 | SL: 2,780</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. BOTTOM TEXT
    st.markdown('<div class="footer-text">Everything You Need to <span class="green-text">Trade Smarter</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: DASHBOARD (ANALYZER)
# ==========================================
elif st.session_state.page == 'dashboard':
    st.markdown("""
    <div style="padding: 20px 8%; border-bottom: 1px solid #1e262c; display: flex; justify-content: space-between; align-items: center;">
        <h2 style="margin:0; font-weight:800; color:#00df81;">🏹 Analytics Terminal</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.button("⬅ Back to Home", on_click=lambda: navigate_to('home'))
    
    # Dashboard Grid
    c1, c2, c3 = st.columns(3)
    c1.metric("NIFTY 50", "22,713.10", "↗ 0.15%")
    c2.metric("SENSEX", "73,319.55", "↗ 0.25%")
    c3.metric("ADVANCES", "1,420", "Bullish")
    
    st.info("Analysis engine is active. Search for stocks in the sidebar.")
