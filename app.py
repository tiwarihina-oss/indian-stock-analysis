import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="StockPulse | AI Stock Intelligence", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALIZE SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_dashboard():
    st.session_state.page = 'dashboard'

def go_to_home():
    st.session_state.page = 'home'

# --- SHARED STYLING (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050708;
        color: white;
    }

    /* Remove Streamlit Padding */
    .main .block-container { padding: 0; max-width: 100%; }
    header { visibility: hidden; }

    /* Landing Page Styles */
    .hero-section {
        background: radial-gradient(circle at 80% 20%, #102a1e 0%, #050708 50%);
        padding: 60px 10% 100px 10%;
        min-height: 90vh;
    }

    .nav-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 20px 0; margin-bottom: 60px;
    }
    
    .logo { font-size: 24px; font-weight: 800; display: flex; align-items: center; gap: 8px; }
    .logo-icon { color: #00c805; background: #00c80522; padding: 5px; border-radius: 6px; }

    .badge {
        background: #102a1e; color: #00c805; padding: 6px 16px; border-radius: 20px;
        font-size: 13px; font-weight: 600; border: 1px solid #1a3d2c; display: inline-block;
        margin-bottom: 30px;
    }

    .hero-title { font-size: 72px; font-weight: 800; line-height: 1.1; margin-bottom: 30px; }
    .green-text { color: #00c805; }
    
    .hero-desc { color: #848e9c; font-size: 18px; max-width: 500px; line-height: 1.6; margin-bottom: 40px; }

    /* Buttons */
    .primary-btn {
        background-color: #00c805; color: #050708; border: none; padding: 14px 28px;
        border-radius: 8px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 10px;
    }

    /* Mockup/Card on Right */
    .mockup-container { position: relative; }
    .floating-card {
        background: rgba(16, 22, 26, 0.8); backdrop-filter: blur(10px);
        border: 1px solid #1e262c; border-radius: 12px; padding: 20px;
        position: absolute; bottom: -30px; left: -50px; width: 220px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* Stats Section */
    .stats-grid { display: flex; gap: 80px; margin-top: 80px; }
    .stat-item h3 { font-size: 32px; font-weight: 800; margin: 0; }
    .stat-item p { color: #848e9c; font-size: 14px; margin-top: 5px; }

    /* Dashboard Logic Styling */
    .dash-container { padding: 40px 5%; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1: HOME SCREEN (LANDING)
# ==========================================
if st.session_state.page == 'home':
    st.markdown(f"""
    <div class="hero-section">
        <!-- Navigation -->
        <div class="nav-bar">
            <div class="logo">
                <span class="logo-icon">📈</span> StockPulse
            </div>
        </div>

        <div style="display: flex; align-items: center; gap: 50px;">
            <!-- Left Content -->
            <div style="flex: 1;">
                <div class="badge">⚡ AI-Powered Stock Analysis</div>
                <h1 class="hero-title">Master the <span class="green-text">Indian Stock</span> Market with AI</h1>
                <p class="hero-desc">
                    Real-time data from Yahoo Finance, AI-generated trading signals with entry, target, and stop loss prices. 
                    Your edge in NSE & BSE markets.
                </p>
            </div>

            <!-- Right Mockup -->
            <div style="flex: 1; position: relative;">
                <img src="https://images.unsplash.com/photo-1611974717537-488439a44484?auto=format&fit=crop&q=80&w=1000" 
                     style="width: 100%; border-radius: 20px; border: 1px solid #1e262c; opacity: 0.6;">
                <div class="floating-card">
                    <p style="font-size: 12px; color: #848e9c; margin: 0;">AI Signal</p>
                    <p style="font-size: 16px; font-weight: 700; color: #00c805; margin: 5px 0;">🟢 BUY RELIANCE</p>
                    <p style="font-size: 12px; color: white; margin: 0;">Target: 3,050 | SL: 2,780</p>
                </div>
            </div>
        </div>

        <!-- Stats -->
        <div class="stats-grid">
            <div class="stat-item"><h3>5000+</h3><p>Indian Stocks</p></div>
            <div class="stat-item"><h3>Real-time</h3><p>Market Data</p></div>
            <div class="stat-item"><h3>AI</h3><p>Trading Signals</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Real Streamlit Button for Navigation
    st.columns([1, 4, 1])[1].button("Go to Dashboard ➔", on_click=go_to_dashboard, use_container_width=True)

# ==========================================
# PAGE 2: DASHBOARD
# ==========================================
elif st.session_state.page == 'dashboard':
    # Top Bar for Dashboard
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 5%; background: #0b0e11; border-bottom: 1px solid #1e262c;">
            <div style="font-size: 20px; font-weight: 800; cursor: pointer;" onclick="window.location.reload()">📈 StockPulse Dashboard</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Simple Back Button
    if st.button("⬅ Back to Home"):
        go_to_home()
        st.rerun()

    # --- Your Professional Dashboard Logic ---
    st.markdown('<div class="dash-container">', unsafe_allow_html=True)
    
    # (Placeholder for the high-end Dashboard we built in the previous step)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="background:#161a1e; padding:30px; border-radius:15px; border:1px solid #2b3139;"><h3>NIFTY 50</h3><h1>22,713.10</h1><p style="color:#00c805">+0.15%</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div style="background:#161a1e; padding:30px; border-radius:15px; border:1px solid #2b3139;"><h3>SENSEX</h3><h1>73,319.55</h1><p style="color:#00c805">+0.25%</p></div>', unsafe_allow_html=True)

    st.info("💡 Pro Tip: Search for symbols like RELIANCE, SBIN, or INFY in the sidebar to generate AI signals.")
    
    # Add your Stock Analyzer Sidebar here...
    with st.sidebar:
        st.header("🔍 Stock Analyzer")
        search = st.text_input("Enter Ticker")
        if search:
            st.success(f"Analyzing {search}...")
            # Insert previous technical analysis logic here
    st.markdown('</div>', unsafe_allow_html=True)
