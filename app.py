import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from streamlit_lottie import st_lottie
from datetime import date, timedelta
import random

# ---------------- CONFIGURATION ----------------
st.set_page_config(
    page_title="MindPatch Pro",
    page_icon="🧠",
    layout="wide", # Switch to Wide for dashboard feel
    initial_sidebar_state="expanded"
)

# ---------------- ASSETS & STYLING ----------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Animations
lottie_zen = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_calmz.json")
lottie_welcome = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_puciaact.json")

# Custom CSS for "Breathing Bubble" and Cards
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif; 
        background-color: #f8f9fa;
    }
    
    /* Advanced Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
        border: 1px solid #e5e7eb;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Breathing Animation */
    .breathing-circle {
        width: 150px;
        height: 150px;
        background: #a5b4fc;
        border-radius: 50%;
        margin: 0 auto;
        animation: breathe 4s infinite ease-in-out;
        box-shadow: 0 0 20px rgba(165, 180, 252, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }

    @keyframes breathe {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE & GAMIFICATION ----------------
if "user_xp" not in st.session_state: st.session_state.user_xp = 0
if "user_level" not in st.session_state: st.session_state.user_level = 1
if "mood_history" not in st.session_state: 
    # Pre-filling dummy data for the "Advanced" demo feeling
    dates = [date.today() - timedelta(days=i) for i in range(14, -1, -1)]
    st.session_state.mood_history = [
        {"Date": d, "Mood": random.randint(2, 5), "ScreenTime": random.uniform(2, 8)} 
        for d in dates
    ]
if "journal" not in st.session_state: st.session_state.journal = []

# Logic to calculate Level
def calculate_level():
    # Level up every 100 XP
    new_level = 1 + (st.session_state.user_xp // 100)
    if new_level > st.session_state.user_level:
        st.balloons()
        st.toast(f"🎉 Level Up! You are now Lvl {new_level}!")
    st.session_state.user_level = new_level

# ---------------- SIDEBAR PROFILE ----------------
with st.sidebar:
    st_lottie(lottie_welcome, height=150, key="sidebar_anim")
    
    st.write(f"### 👤 Profile: Lvl {st.session_state.user_level}")
    
    # Custom XP Bar
    xp_progress = (st.session_state.user_xp % 100) / 100
    st.progress(xp_progress)
    st.caption(f"{st.session_state.user_xp} XP Total • {100 - (st.session_state.user_xp % 100)} to next level")
    
    st.markdown("---")
    menu = st.radio("Navigation", ["🏠 Dashboard", "📝 Daily Log", "🧘 Zen Mode", "📊 Analytics"])

# ---------------- PAGE 1: DASHBOARD ----------------
if menu == "🏠 Dashboard":
    st.title("Good Morning, Achiever ☀️")
    st.markdown("Here
