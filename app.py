import streamlit as st
from datetime import date

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MindPatch • Digital Wellness",
    page_icon="🧠",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #F6F7FB;
}
.main {
    background-color: #F6F7FB;
}
h1, h2, h3 {
    color: #3B3B98;
}
.card {
    background-color: white;
    padding: 1.2rem;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}
.badge {
    display: inline-block;
    padding: 6px 12px;
    background-color: #E0E7FF;
    color: #3730A3;
    border-radius: 20px;
    font-size: 14px;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "streak" not in st.session_state:
    st.session_state.streak = 0

if "gratitude" not in st.session_state:
    st.session_state.gratitude = []

# ---------------- HEADER ----------------
st.title("🧠 MindPatch")
st.subheader("A Digital Detox & Wellness Planner")
st.caption("Helping students build healthier digital habits")

# ---------------- NAVIGATION ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "😊 Mood",
    "📱 Screen Time",
    "🤖 AI Detox Planner",
    "📔 Gratitude",
    "🏆 Habits"
])

# ================= TAB 1: MOOD LOGGING =================
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("How are you feeling today?")

    mood = st.slider(
        "Select your mood",
        1, 5, 3,
        format="%d"
    )

    mood_map = {
        1: "😞 Very Low",
        2: "😕 Low",
        3: "😐 Neutral",
        4: "🙂 Good",
        5: "😄 Great"
    }

    st.markdown(f"### Your Mood: {mood_map[mood]}")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 2: SCREEN TIME =================
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Daily Screen Time Input")

    screen_time = st.number_input(
        "Hours spent on screens today",
        min_value=0.0,
        max_value=18.0,
        step=0.5
    )

    if screen_time <= 2:
        st.success("Healthy screen usage 🌿")
    elif screen_time <= 5:
        st.warning("Moderate usage ⚠️")
    else:
        st.error("High screen exposure 🚨")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 3: AI DETOX PLANNER =================
with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("AI-Generated Detox Planner")

    st.caption("Suggestions are generated using mood & screen-time rules")

    if mood <= 2 and screen_time > 4:
        st.info("🧘 Suggestion: Take a 20-minute phone-free break and do slow breathing.")
    elif mood <= 3 and screen_time > 3:
        st.info("🚶 Suggestion: Go for a short walk without your phone.")
    elif mood >= 4 and screen_time <= 3:
        st.success("✨ You’re doing great! Maintain your routine.")
    else:
        st.warning("📖 Suggestion: Read or journal for 10 minutes offline.")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 4: GRATITUDE JOURNAL =================
with tab4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Gratitude Journal")

    entry = st.text_area(
        "Write one thing you're grateful for today:",
        height=100
    )

    if st.button("Save Entry"):
        if entry.strip():
            st.session_state.gratitude.append(
                f"{date.today()} • {entry}"
            )
            st.success("Gratitude saved 💙")

    st.subheader("Past Entries")
    for g in reversed(st.session_state.gratitude[-5:]):
        st.markdown(f"- {g}")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 5: HABIT TRACKER =================
with tab5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Habit Tracker & Rewards")

    completed = st.checkbox("📵 Took a screen-free break today")

    if completed:
        st.session_state.streak += 1
        st.success(f"🔥 Streak: {st.session_state.streak} days")

    st.subheader("Your Rewards")
    if st.session_state.streak >= 3:
        st.markdown("<span class='badge'>🥉 Bronze Mindful Badge</span>", unsafe_allow_html=True)
    if st.session_state.streak >= 5:
        st.markdown("<span class='badge'>🥈 Silver Balance Badge</span>", unsafe_allow_html=True)
    if st.session_state.streak >= 7:
        st.markdown("<span class='badge'>🥇 Gold Wellness Badge</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.caption("MindPatch Prototype • Critical & Creative Thinking • AI-Assisted Wellness")
