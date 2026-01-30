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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- ASSETS & STYLING ----------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load Animations
lottie_zen = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_calmz.json")
lottie_welcome = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_puciaact.json")

# Custom CSS
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
    # Pre-filling dummy data
    dates = [date.today() - timedelta(days=i) for i in range(14, -1, -1)]
    st.session_state.mood_history = [
        {"Date": d, "Mood": random.randint(2, 5), "ScreenTime": random.uniform(2, 8)} 
        for d in dates
    ]
if "journal" not in st.session_state: st.session_state.journal = []

# Logic to calculate Level
def calculate_level():
    new_level = 1 + (st.session_state.user_xp // 100)
    if new_level > st.session_state.user_level:
        st.balloons()
        st.toast(f"🎉 Level Up! You are now Lvl {new_level}!")
    st.session_state.user_level = new_level

# ---------------- SIDEBAR PROFILE ----------------
with st.sidebar:
    if lottie_welcome:
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
    st.markdown("Here is your wellness snapshot.")
    
    # Top Stats Row
    c1, c2, c3, c4 = st.columns(4)
    
    last_mood = st.session_state.mood_history[-1]['Mood']
    mood_map = {1:"😞", 2:"😕", 3:"😐", 4:"🙂", 5:"😄"}
    
    with c1:
        st.markdown(f"<div class='metric-card'><h3>{mood_map.get(last_mood, '😐')}</h3><p>Last Mood</p></div>", unsafe_allow_html=True)
    with c2:
        avg_screen = sum(d['ScreenTime'] for d in st.session_state.mood_history[-7:]) / 7
        st.markdown(f"<div class='metric-card'><h3>{avg_screen:.1f}h</h3><p>7-Day Avg Screen</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><h3>{len(st.session_state.journal)}</h3><p>Journal Entries</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-card'><h3>{st.session_state.user_level}</h3><p>Current Level</p></div>", unsafe_allow_html=True)

    st.markdown("### 💡 AI Daily Insight")
    
    # Correlation Check
    recent_data = pd.DataFrame(st.session_state.mood_history[-7:])
    if len(recent_data) > 1:
        corr = recent_data['Mood'].corr(recent_data['ScreenTime'])
    else:
        corr = 0
    
    if corr < -0.3:
        insight = "📉 **Strong Negative Correlation:** Your data shows that when your screen time goes UP, your mood goes DOWN. Try reducing usage by 30 mins tomorrow."
        status = "warning"
    elif last_mood >= 4:
        insight = "🌟 **Winning Streak:** You're maintaining high spirits! Whatever routine you are doing, keep it up."
        status = "success"
    else:
        insight = "⚖️ **Neutral Phase:** Your stats are stable. Try a quick walk to boost your dopamine naturally."
        status = "info"

    if status == "warning": st.warning(insight)
    elif status == "success": st.success(insight)
    else: st.info(insight)

# ---------------- PAGE 2: DAILY LOG ----------------
elif menu == "📝 Daily Log":
    st.title("Track Your Day")
    
    col1, col2 = st.columns([1, 1])
    
    mood_map = {1:"😞", 2:"😕", 3:"😐", 4:"🙂", 5:"😄"}

    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("1. How do you feel?")
        new_mood = st.select_slider("Mood", options=[1,2,3,4,5], format_func=lambda x: mood_map[x], label_visibility="collapsed")
        
        st.subheader("2. Screen Hours")
        new_screen = st.slider("Hours", 0.0, 16.0, 4.0, 0.5, label_visibility="collapsed")
        
        if st.button("💾 Save & Earn XP"):
            # Update Data
            new_entry = {"Date": date.today(), "Mood": new_mood, "ScreenTime": new_screen}
            st.session_state.mood_history.append(new_entry)
            
            # Update XP
            st.session_state.user_xp += 20
            calculate_level()
            st.toast("Saved! +20 XP")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("3. Gratitude Journal")
        with st.form("journal_form", clear_on_submit=True):
            note = st.text_area("Write one positive thing...", height=150)
            if st.form_submit_button("Log Journal"):
                if note:
                    st.session_state.journal.append(f"{date.today()}: {note}")
                    st.session_state.user_xp += 10
                    calculate_level()
                    st.success("Entry saved! +10 XP")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- PAGE 3: ZEN MODE ----------------
elif menu == "🧘 Zen Mode":
    st.title("Digital Decompression")
    
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.info("Follow the circle: Inhale as it expands, Exhale as it shrinks.")
        # Pure CSS Animation for smooth breathing
        st.markdown("""
            <br><br>
            <div class="breathing-circle">
                Breathe
            </div>
            <br><br>
        """, unsafe_allow_html=True)
    
    with c2:
        if lottie_zen:
            st_lottie(lottie_zen, height=300, key="zen_anim")
        else:
            st.write("✨ Visualize a calm stream...")

# ---------------- PAGE 4: ANALYTICS ----------------
elif menu == "📊 Analytics":
    st.title("Deep Dive Analytics")
    
    df = pd.DataFrame(st.session_state.mood_history)
    
    tab_a, tab_b = st.tabs(["📈 Trends", "🔍 Correlations"])
    
    with tab_a:
        st.caption("Mood vs Screen Time over the last 14 days")
        fig = px.line(df, x="Date", y=["Mood", "ScreenTime"], markers=True, 
                      color_discrete_map={"Mood": "#6366f1", "ScreenTime": "#f43f5e"})
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab_b:
        st.caption("Does Screen Time actually affect your Mood?")
        
        # Advanced: Scatter Plot with Trendline
        try:
            fig_corr = px.scatter(
                df, x="ScreenTime", y="Mood", 
                trendline="ols", 
                title="Correlation Analysis",
                labels={"ScreenTime": "Hours on Phone", "Mood": "Happiness Level"},
                color_discrete_sequence=["#10b981"]
            )
            fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_corr, use_container_width=True)
        except:
            st.info("Gathering more data to build your trend line...")
        
        st.markdown("""
        **How to read this:**
        * If the line goes **DOWN** ↘️: More screen time = Less happiness.
        * If the line is **FLAT** ➡️: Screen time doesn't affect your mood much.
        """)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("<center style='color: #9ca3af'>MindPatch Pro • v2.1 • Gamified Wellness</center>", unsafe_allow_html=True)
