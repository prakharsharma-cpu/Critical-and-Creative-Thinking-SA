import streamlit as st
from datetime import date
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MindPatch • Digital Wellness",
    page_icon="🧠",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    /* Global Styles */
    body { background-color: #F6F7FB; }
    .main { background-color: #F6F7FB; }
    
    /* Headings */
    h1, h2, h3 { color: #3B3B98; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Card Container */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #EEF2FF;
    }
    
    /* Badge Styles */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        background: #E0E7FF;
        color: #312E81;
        border-radius: 999px;
        font-size: 14px;
        font-weight: 600;
        margin: 4px 6px 4px 0;
    }
    
    /* Metric Styling */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE INITIALIZATION ----------------
if "mood" not in st.session_state:
    st.session_state.mood = 3

if "screen_time" not in st.session_state:
    st.session_state.screen_time = 0.0

if "gratitude" not in st.session_state:
    st.session_state.gratitude = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "habit_log" not in st.session_state:
    st.session_state.habit_log = set() # Using a set to store dates

# ---------------- HEADER ----------------
st.title("🧠 MindPatch")
st.markdown("**Digital Detox & Wellness Planner**")
st.caption("A functional prototype for student mental wellness.")

# ---------------- NAVIGATION ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "😊 Mood", 
    "📱 Screen Time", 
    "🤖 AI Planner", 
    "📔 Gratitude", 
    "🏆 Habits"
])

# ================= TAB 1: MOOD LOGGING =================
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("How are you feeling?")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Fixed syntax error here: added commas
        st.session_state.mood = st.slider(
            "Select your mood level:",
            min_value=1,
            max_value=5,
            value=st.session_state.mood
        )

    mood_map = {
        1: ("😞 Very Low", "It's okay to have bad days."),
        2: ("😕 Low", "Be gentle with yourself."),
        3: ("😐 Neutral", "Taking it one step at a time."),
        4: ("🙂 Good", "Glad to hear you're doing well!"),
        5: ("😄 Great", "Keep up that positive energy!")
    }
    
    current_mood, message = mood_map[st.session_state.mood]
    
    with col2:
        st.metric(label="Current Mood", value=current_mood.split(" ")[0])

    st.info(f"**{current_mood}** — {message}")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 2: SCREEN TIME =================
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Screen-Time Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.screen_time = st.number_input(
            "Hours spent on screens today:",
            min_value=0.0,
            max_value=24.0,
            step=0.5,
            value=st.session_state.screen_time
        )
    
    # Logic for progress bar color
    usage_ratio = min(st.session_state.screen_time / 12, 1.0) # Assume 12h is max for bar
    
    if st.session_state.screen_time <= 2:
        status_color = "green"
        msg = "Healthy usage 🌿"
    elif st.session_state.screen_time <= 5:
        status_color = "orange"
        msg = "Moderate usage ⚠️"
    else:
        status_color = "red"
        msg = "High screen exposure 🚨"

    with col2:
        st.markdown(f"**Status:** {msg}")
        st.progress(usage_ratio)
        
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 3: AI DETOX PLANNER =================
with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("AI Detox Planner")
    st.markdown("Based on your **Mood** and **Screen Time**, here is your suggested plan:")
    
    mood = st.session_state.mood
    screen = st.session_state.screen_time
    
    # Simulating AI processing
    with st.spinner("Analyzing your wellness data..."):
        time.sleep(0.5) # Cosmetic delay for "AI feel"
    
    if mood <= 2 and screen > 4:
        suggestion = "🧘 **Deep Reset:** Take a 20-minute phone-free break. Try the 4-7-8 breathing technique."
        reason = "High screen time combined with low mood can lead to digital burnout."
    elif mood <= 3 and screen > 3:
        suggestion = "🚶 **Nature Walk:** Go for a 15-minute walk without your phone."
        reason = "Movement and fresh air are proven to boost serotonin levels."
    elif mood >= 4 and screen <= 3:
        suggestion = "🎨 **Creative Flow:** You are in a good spot! Use this energy to read, draw, or cook."
        reason = "Maintaining low screen time preserves your current positive momentum."
    else:
        suggestion = "📖 **Mindful Journaling:** Spend 10 minutes writing down your thoughts."
        reason = "A neutral activity helps recalibrate your focus."

    st.success(suggestion)
    with st.expander("Why this suggestion?"):
        st.write(reason)
        
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 4: GRATITUDE JOURNAL =================
with tab4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Gratitude Journal")
    
    # Using a Form ensures the text box clears after submission
    with st.form(key='gratitude_form', clear_on_submit=True):
        entry_text = st.text_area("What are you grateful for today?", height=100)
        submit_button = st.form_submit_button(label='Save Entry')
        
        if submit_button and entry_text:
            st.session_state.gratitude.append(f"{date.today()} • {entry_text}")
            st.toast("Saved successfully! 💙")
            
    st.divider()
    
    st.subheader("Recent Entries")
    if not st.session_state.gratitude:
        st.caption("No entries yet. Start writing above!")
    else:
        for g in reversed(st.session_state.gratitude[-5:]):
            st.markdown(f"✨ {g}")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 5: HABIT TRACKER =================
with tab5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Habit Tracker")
    
    today = date.today()
    
    # Check if today is already in the log
    is_done_today = today in st.session_state.habit_log
    
    st.markdown("### 🎯 Daily Goal: Take a 1-hour screen-free break")
    
    # Callback logic for the checkbox
    def toggle_habit():
        if today in st.session_state.habit_log:
            st.session_state.habit_log.remove(today)
            st.session_state.streak = max(0, st.session_state.streak - 1)
        else:
            st.session_state.habit_log.add(today)
            st.session_state.streak += 1
            st.balloons()

    checked = st.checkbox(
        "I completed my break today", 
        value=is_done_today,
        on_change=toggle_habit
    )
    
    st.divider()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Streak", f"{st.session_state.streak} Days")
    
    st.subheader("Your Badges")
    
    badges = []
    if st.session_state.streak >= 3:
        badges.append("🥉 Bronze Mindful")
    if st.session_state.streak >= 5:
        badges.append("🥈 Silver Balance")
    if st.session_state.streak >= 7:
        badges.append("🥇 Gold Wellness")
        
    if badges:
        for b in badges:
            st.markdown(f"<span class='badge'>{b}</span>", unsafe_allow_html=True)
    else:
        st.caption("Hit a 3-day streak to earn your first badge!")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>"
    "MindPatch • Built with Streamlit • Prioritizing Digital Wellness"
    "</div>", 
    unsafe_allow_html=True
)
