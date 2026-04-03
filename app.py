import streamlit as st
import yfinance as yf

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="StockPulse AI", layout="wide", initial_sidebar_state="collapsed")

# Navigation Logic
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 2. BULLETPROOF CSS (No external images) ---
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
    
    /* Emerald Glow Background */
    .hero-section {
        background: radial-gradient(circle at 90% 10%, #0d2b1f 0%, #050708 55%);
        padding: 20px 10% 80px 10%;
        min-height: 100vh;
    }

    /* Navbar */
    .nav-bar { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; margin-bottom: 40px; }
    .logo { font-size: 24px; font-weight: 800; display: flex; align-items: center; gap: 10px; color: white; }
    .logo-icon { 
        background: #00df81; color: #050708; width: 32px; height: 32px; 
        display: flex; align-items: center; justify-content: center; border-radius: 8px; font-size: 18px;
    }

    /* Badge */
    .badge {
        background: rgba(0, 223, 129, 0.1); color: #00df81; padding: 8px 18px; border-radius: 20px;
        font-size: 13px; font-weight: 600; border: 1px solid rgba(0, 223, 129, 0.2); 
        display: inline-block; margin-bottom: 30px;
    }

    /* Hero Text */
    .hero-title { font-size: clamp(40px, 5vw, 72px); font-weight: 800; line-height: 1.1; margin-bottom: 25px; letter-spacing: -2px; }
    .green-text { color: #00df81; }
    .hero-desc { color: #848e9c; font-size: 18px; max-width: 500px; line-height: 1.6; margin-bottom: 45px; }

    /* BULLETPROOF CSS CHART MOCKUP (Replaces the broken image) */
    .chart-mockup {
        width: 100%;
        height: 400px;
        background: #0b1012;
        border: 1px solid #1e262c;
        border-radius: 24px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: flex-end;
        padding: 20px;
        background-image: 
            linear-gradient(rgba(0, 223, 129, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 223, 129, 0.05) 1px, transparent 1px);
        background-size: 40px 40px;
    }
    
    /* CSS Line representing the stock trend */
    .trend-line {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0; left: 0;
        background: linear-gradient(transparent 60%, rgba(0, 223, 129, 0.1));
        clip-path: polygon(0% 80%, 15% 70%, 30% 75%, 45% 40%, 60% 55%, 75% 20%, 90% 35%, 100% 10%, 100% 100%, 0% 100%);
    }

    /* Floating AI Card */
    .floating-card {
        background: rgba(11, 16, 19, 0.9); 
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1); 
        border-radius: 16px; padding: 22px;
        position: absolute; 
        bottom: 40px; 
        left: -30px; 
        width: 250px; 
        box-shadow: 0 30px 60px rgba(0,0,0,0.8);
        z-index: 100;
    }

    .stats-row { display: flex; gap: 60px; margin-top: 60px; }
    .stat-box h3 { font-size: 32px; font-weight: 800; margin: 0; }
    .stat-box p { color: #848e9c; font-size: 14px; margin-top: 5px; }

    .footer-text { text-align: center; font-size: 36px; font-weight: 800; margin-top: 100px; padding-bottom: 80px; }

    /* Green Button Styling */
    div.stButton > button {
        background-color: #00df81 !important; color: #050708 !important;
        font-weight: 700 !important; padding: 12px 28px !important;
        border-radius: 8px !important; border: none !important;
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1: HOME SCREEN
# ==========================================
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    
    # NAVBAR
    nl, nr = st.columns([1, 1])
    with nl:
        st.markdown('<div class="logo"><div class="logo-icon">📈</div> StockPulse</div>', unsafe_allow_html=True)
    with nr:
        _, nbc = st.columns([2, 1.2])
        nbc.button("Go to Dashboard →", key="nav_btn", on_click=lambda: navigate_to('dashboard'))
    
    # HERO CONTENT
    st.write("") # Spacer
    col_text, col_mockup = st.columns([1.1, 1], gap="large")
    
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

    with col_mockup:
        # This is the bulletproof code-based visual
        st.markdown("""
        <div style="position: relative;">
            <div class="chart-mockup">
                <div class="trend-line"></div>
                <div style="color: #00df81; font-size: 10px; opacity: 0.5;">0.2455</div>
            </div>
            <div class="floating-card">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:10px;">
                    <span style="background:rgba(0, 223, 129, 0.2); padding:5px; border-radius:50%; font-size:12px;">🎯</span>
                    <span style="color:#848e9c; font-size:12px;">AI Signal</span>
                </div>
                <p style="color:#00df81; font-size:20px; font-weight:800; margin:0;">BUY RELIANCE</p>
                <p style="color:white; font-size:13px; margin-top:5px; opacity:0.8;">Target: 3,050 | SL: 2,780</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # BOTTOM FOOTER
    st.markdown('<div class="footer-text">Everything You Need to <span class="green-text">Trade Smarter</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: DASHBOARD
# ==========================================
elif st.session_state.page == 'dashboard':
    st.markdown("""
    <div style="padding: 20px 8%; background: #050708; border-bottom: 1px solid #1e262c; display: flex; justify-content: space-between; align-items: center;">
        <h2 style="margin:0; font-weight:800; color:#00df81;">🏹 Intelligence Terminal</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("⬅ Back to Home"):
        navigate_to('home')
    
    st.write("")
    st.title("Market Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("NIFTY 50", "22,713.10", "↗ 0.15%")
    c2.metric("SENSEX", "73,319.55", "↗ 0.25%")
    c3.metric("RELIANCE", "2,985.00", "↗ 1.20%")
