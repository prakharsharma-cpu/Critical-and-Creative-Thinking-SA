import streamlit as st
from datetime import date, timedelta
import time
import pandas as pd
import plotly.express as px
import random # Used to simulate history data for the demo

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="MindPatch • Digital Wellness",
    page_icon="🧠",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    body { background-color: #F6F7FB; }
    .main { background-color: #F6F7FB; }
    h1, h2, h3 { color: #3B3B98; font-family: 'Helvetica Neue', sans-serif; }
    
    .card {
        background: white;
        padding: 2rem;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #EEF2FF;
    }
    
    /* Smooth transition for charts */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
# Initialize variables if they don't exist
if "mood" not in st.session_state:
    st.session_state.mood = 3
if "gratitude" not in st.session_state:
    st.session_state.gratitude = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "habit_log" not in st.session_state:
    st.session_state.habit_log = set()

# Initialize breakdown for Pie Chart
if "time_social" not in st.session_state: st.session_state.time_social = 2.0
if "time_study" not in st.session_state: st.session_state.time_study = 4.0
if "time_ent" not in st.session_state: st.session_state.time_ent = 1.5

# ---------------- HEADER ----------------
st.title("🧠 MindPatch")
st.caption("Visualizing your digital habits for better mental health.")

# ---------------- NAVIGATION ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "😊 Mood Trends", 
    "📊 Screen Analysis", 
    "🤖 AI Planner", 
    "📔 Gratitude", 
    "🏆 Habits"
])

# ================= TAB 1: MOOD LOGGING & TRENDS =================
with tab1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Today's Mood")
        # Direct assignment to session_state variable
        st.session_state.mood = st.select_slider(
            "How do you feel?",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.mood,
            format_func=lambda x: {1:"😞", 2:"😕", 3:"😐", 4:"🙂", 5:"😄"}[x]
        )
        
        mood_labels = {1:"Rough", 2:"Low", 3:"Okay", 4:"Good", 5:"Awesome"}
        st.caption(f"Status: **{mood_labels[st.session_state.mood]}**")

    with col2:
        st.subheader("Weekly Trend")
        # GENERATE DUMMY DATA FOR VISUALIZATION PURPOSES
        dates = [date.today() - timedelta(days=i) for i in range(6, -1, -1)]
        # Make the last data point match the user's current input
        mood_data = [random.randint(2, 5) for _ in range(6)] + [st.session_state.mood]
        
        df_mood = pd.DataFrame({"Date": dates, "Mood": mood_data})
        
        fig_mood = px.line(
            df_mood, x="Date", y="Mood", 
            markers=True, 
            line_shape="spline", # Makes line curved/smooth
            range_y=[0.5, 5.5]
        )
        fig_mood.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            height=200,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_mood, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 2: SCREEN TIME (PIE CHART) =================
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Screen Time Breakdown")
    
    col_input, col_viz = st.columns([1, 1])
    
    with col_input:
        st.write("**Where did your time go?**")
        st.session_state.time_study = st.slider("📚 Productivity / Study", 0.0, 12.0, st.session_state.time_study, 0.5)
        st.session_state.time_social = st.slider("📱 Social Media", 0.0, 12.0, st.session_state.time_social, 0.5)
        st.session_state.time_ent = st.slider("🎮 Games / Movies", 0.0, 12.0, st.session_state.time_ent, 0.5)
        
        total_screen_time = st.session_state.time_study + st.session_state.time_social + st.session_state.time_ent

    with col_viz:
        # Create Data for Pie Chart
        df_screen = pd.DataFrame({
            "Category": ["Productivity", "Social Media", "Entertainment"],
            "Hours": [st.session_state.time_study, st.session_state.time_social, st.session_state.time_ent]
        })
        
        # Donut Chart
        fig_pie = px.pie(
            df_screen, 
            values='Hours', 
            names='Category',
            hole=0.5, 
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(
            margin=dict(l=20, r=20, t=0, b=20),
            height=250,
            showlegend=False
        )
        
        if total_screen_time > 0:
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Log your hours to see the breakdown.")

    st.divider()
    st.metric("Total Screen Time", f"{total_screen_time} Hours")
    
    if total_screen_time > 8:
        st.error("🚨 High Usage Detected")
    elif total_screen_time > 5:
        st.warning("⚠️ Moderate Usage")
    else:
        st.success("🌿 Healthy Balance")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 3: AI PLANNER =================
with tab3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("AI Detox Planner")
    
    social_ratio = 0
    if total_screen_time > 0:
        social_ratio = st.session_state.time_social / total_screen_time

    # AI Logic Rules
    if total_screen_time > 6 and social_ratio > 0.5:
        st.info("💡 **Insight:** Over 50% of your time was on Social Media.")
        st.markdown("### 🧘 Recommendation: The 'Grey Scale' Challenge")
        st.write("Turn your phone to Grayscale mode for the next 2 hours. This reduces dopamine triggers.")
    
    elif st.session_state.mood <= 2:
        st.info("💡 **Insight:** Mood is low today.")
        st.markdown("### 🌲 Recommendation: Nature Reset")
        st.write("Leave your phone in your room. Step outside for 10 minutes.")
        
    elif st.session_state.time_study > 5:
        st.success("💡 **Insight:** High productivity detected!")
        st.markdown("### 🧠 Recommendation: Deep Rest")
        st.write("You've worked hard. Listen to instrumental music with eyes closed.")
        
    else:
        st.markdown("### ✨ Recommendation: Maintain Balance")
        st.write("You are doing well. Maybe read a physical book for 15 minutes?")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 4: GRATITUDE =================
with tab4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Gratitude Jar")
    
    # FIX: Renamed the form key to avoid conflict with st.session_state.gratitude list
    with st.form("gratitude_form_key", clear_on_submit=True):
        txt = st.text_input("I am grateful for...", placeholder="e.g., The warm coffee this morning")
        submitted = st.form_submit_button("Add Note")
        
        if submitted and txt:
            st.session_state.gratitude.append(f"{date.today()}: {txt}")
            st.success("Added to jar!")
            
    st.divider()
    
    with st.expander("📖 Read previous entries", expanded=True):
        if st.session_state.gratitude:
            for g in reversed(st.session_state.gratitude):
                st.text(g)
        else:
            st.caption("Your jar is empty. Add your first note!")
            
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 5: HABITS =================
with tab5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Streak Tracker")
    
    col_a, col_b = st.columns([2,1])
    
    with col_a:
        st.write("### 🔥 Current Streak: " + str(st.session_state.streak))
        
        next_goal = 3
        if st.session_state.streak >= 3: next_goal = 7
        if st.session_state.streak >= 7: next_goal = 14
        
        progress = min(st.session_state.streak / next_goal, 1.0)
        st.progress(progress)
        st.caption(f"Goal: {next_goal} days")

    with col_b:
        today = date.today()
        # Logic to toggle check
        def toggle():
            if today in st.session_state.habit_log:
                st.session_state.habit_log.remove(today)
                st.session_state.streak -= 1
            else:
                st.session_state.habit_log.add(today)
                st.session_state.streak += 1
                st.balloons()
        
        st.checkbox("Log Daily Detox", value=(today in st.session_state.habit_log), on_change=toggle)

    st.markdown("</div>", unsafe_allow_html=True)
