# app.py 
import streamlit as st
from streamlit_lottie import st_lottie
import json
import base64
from pathlib import Path
import streamlit.components.v1 as components

# Import page modules (now inside pages/)
from tabs.know_yourself import run_mental_wellness_tab
from tabs.untold_side_page import render_untold_side
from tabs.who_we_are import run_who_we_are_tab

# =====================================================================
# PAGE CONFIG  (set ONCE at the top level)
# =====================================================================
st.set_page_config(
    page_title="Student Mental Wellness Dashboard",
    page_icon="🧠",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
ANIM_DIR = BASE_DIR / "assets" / "animations"
IMG_DIR = BASE_DIR / "assets" / "img"

def img_to_base64(filename: str) -> str:
    img_path = IMG_DIR / filename
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# turn your 3 member photos into base64 strings
member1_b64 = img_to_base64("member1.png")
member2_b64 = img_to_base64("member2.png")
member3_b64 = img_to_base64("member3.png")
sidebar_html = f"""

<style>
.team-wrapper {{
    padding: 4px;
    border-radius: 20px;
    background: linear-gradient(135deg, #a5b4fc 0%, #7dd3fc 40%, #fecaca 100%);
}}
/* soft animated glow behind avatar */
@keyframes pulseGlow {{
    0%   {{ box-shadow: 0 0 0 0 rgba(129, 140, 248, 0.55); }}
    70%  {{ box-shadow: 0 0 0 12px rgba(129, 140, 248, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(129, 140, 248, 0); }}
}}

.team-avatar-ring {{
    position: absolute;
    top: 24px;
    left: 50%;
    transform: translateX(-50%);
    width: 72px;
    height: 72px;
    border-radius: 999px;
    animation: pulseGlow 2.4s infinite;
}}

.team-card {{
    background: rgba(248, 250, 252, 0.92);
    border-radius: 18px;
    padding: 18px 16px 20px 16px;
    box-shadow:
        0 18px 35px rgba(15, 23, 42, 0.25),
        0 0 0 1px rgba(148, 163, 184, 0.3);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(226, 232, 240, 0.9);
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    position: relative;
    overflow: hidden;
    transform: translateY(0px);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    max-width: 360px;      
    margin: 0 auto;        
}}

.team-card:hover {{
    transform: translateY(-4px);
    box-shadow:
        0 22px 40px rgba(15, 23, 42, 0.35),
        0 0 0 1px rgba(129, 140, 248, 0.7);
}}

.team-glow-bar {{
    position: absolute;
    top: 0;
    left: 18%;
    right: 18%;
    height: 4px;
    border-radius: 0 0 999px 999px;
    background: linear-gradient(90deg, #22c55e, #3b82f6, #ec4899);
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.6);
}}

.team-avatar {{
    width: 62px;
    height: 62px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 8px auto 10px auto;
    font-size: 32px;
    background: radial-gradient(circle at 30% 30%, #fef9c3, #fbbf24);
    box-shadow: 0 6px 14px rgba(0,0,0,0.25);
    border: 3px solid rgba(248, 250, 252, 0.9);
}}

.team-title {{
    text-align: center;
    font-weight: 800;
    font-size: 18px;
    color: #0f172a;
    margin-bottom: 2px;
}}
.team-subtitle {{
    text-align: center;
    font-size: 13px;
    color: #475569;
    margin-bottom: 12px;
}}

.team-section-title {{
    font-weight: 700;
    font-size: 13px;
    color: #111827;
    margin-top: 10px;
    margin-bottom: 4px;
}}

/* member rows */
.member-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
}}

.member-photo {{
    width: 65px;
    height: 65px;
    border-radius: 999px;
    overflow: hidden;
    border: 2px solid rgba(129, 140, 248, 0.9);
    box-shadow: 0 3px 6px rgba(15, 23, 42, 0.35);
    flex-shrink: 0;
}}

.member-photo img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.member-text {{
    display: flex;
    flex-direction: column;
    gap: 0;
}}

.member-name {{
    font-size: 12.5px;
    font-weight: 600;
    color: #111827;
    line-height: 1.1;
    white-space: nowrap;
}}


.member-role {{
    font-size: 11px;
    font-weight: 500;
    color: #4f46e5;
    background: rgba(224, 231, 255, 0.9);
    padding: 1px 6px;
    border-radius: 999px;
    display: inline-block;
    margin-top: 4px;
}}

.team-course {{
    font-size: 13px;
    color: #1f2937;
    margin-bottom: 8px;
}}
.team-note {{
    font-size: 11.5px;
    font-style: italic;
    color: #6b7280;
    margin-top: 4px;
}}
</style>

<div class="team-wrapper">
  <div class="team-card">
    <div class="team-glow-bar"></div>

    <div class="team-avatar-ring"></div>
    <div class="team-avatar">👩‍💻</div>

    <div class="team-title">Project Team</div>
    <div class="team-subtitle">Student Mental Wellness Dashboard</div>

    <div class="team-section-title">Developed by:</div>

    <div class="member-row">
        <div class="member-photo">
            <img src="data:image/png;base64,{member1_b64}" alt="Member 1">
        </div>
        <div class="member-text">
            <div class="member-name">ANDLY DANNY ‎ ‎ ‎ ‎
              ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎</div>
            <div class="member-role">Member 1</div>
        </div>
    </div>

    <div class="member-row">
        <div class="member-photo">
            <img src="data:image/png;base64,{member2_b64}" alt="Member 2">
        </div>
        <div class="member-text">
            <div class="member-name">BAYU FATWA NEGARA</div>
            <div class="member-role">Member 2</div>
        </div>
    </div>

    <div class="member-row">
        <div class="member-photo">
            <img src="data:image/png;base64,{member3_b64}" alt="Member 3">
        </div>
        <div class="member-text">
            <div class="member-name">MUHAMMAD ROSLAN</div>
            <div class="member-role">Member 3</div>
        </div>
    </div>

    <div class="team-section-title">Course:</div>
    <div class="team-course">
        XBDS2014N – Data Analytics
    </div>

    <div class="team-note">
        This dashboard was created for academic purposes.
    </div>
  </div>
</div>
"""



with st.sidebar:
    components.html(sidebar_html, height=650, scrolling=False)



# =====================================================================
# GLOBAL LAYOUT: MAIN CONTENT WIDTH + GLOBAL STYLES
# =====================================================================
st.markdown(
    """
    <style>
        /* Control the main content width so it looks similar on most laptops */
        .block-container {
            max-width: 1200px;
            padding-top: 1rem;
            padding-bottom: 1rem;
            margin: 0 auto;
        }

        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Montserrat', sans-serif !important;
        }

        .header-title {
            text-align: center;
            font-size: 32px;
            font-weight: 700;
            padding-top: 10px;
        }

        .header-sub {
            text-align: center;
            font-size: 16px;
            margin-top: -8px;
            color: #444;
        }

        .start-btn {
            display: inline-block;
            padding: 14px 24px;
            background: #4a90e2;
            color: white;
            font-weight: 600;
            border-radius: 10px;
            margin-top: 25px;
            text-decoration: none;
        }

        .section-title {
            font-size: 20px;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .section-text {
            font-size: 14px;
            color: #333;
        }

        .equal-card {
            background: #ffffff;
            border-radius: 18px;
            padding: 24px;
            box-shadow: 0px 6px 18px rgba(0,0,0,0.10);
            border: 1px solid #f1f1f1;
            min-height: 320px;
            display: flex;
            flex-direction: column;
        }

        .video-frame {
            position: relative;
            width: 100%;
            padding-top: 56.25%;
            border-radius: 18px;
            overflow: hidden;
            flex: 1;
        }

        .video-frame iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }

        /* FADE-IN ANIMATION FOR TITLE/SUBTITLE */
        @keyframes fadeInUpTitle {
            from { opacity: 0; transform: translateY(15px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .fade-title {
            opacity: 0;
            animation: fadeInUpTitle 0.8s ease-out forwards;
        }

        .fade-sub {
            opacity: 0;
            animation: fadeInUpTitle 0.8s ease-out forwards;
            animation-delay: 0.15s;
        }

        /* ====== NAV BAR RADIO AS TOP TABS ====== */
        /* Center the radio group */
        div[role="radiogroup"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            width: 115% !important;
            gap: 50px !important;
            margin-top: 10px !important;
        }

        /* Hide the default radio circle */
        div[role="radio"] input {
            display: none !important;
        }

        /* Each tab item */
        div[role="radio"] {
            white-space: nowrap !important;
            display: inline-flex !important;
            align-items: center;
            justify-content: center;
            min-width: fit-content;
            padding: 8px 22px;
            border-radius: 999px;
            border: 1px solid #d0d0d0;
            background-color: #ffffff;
            font-weight: 600;
            font-size: 14px;
            color: #333;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
        }

        div[role="radio"]:hover {
            background-color: #f0f6ff;
            border-color: #4a90e2;
        }

        div[role="radio"][aria-checked="true"] {
            background: #4a90e2 !important;
            color: #ffffff !important;
            border-color: #4a90e2 !important;
            box-shadow: 0 4px 10px rgba(74,144,226,0.35);
        }
        :root {
            color-scheme: light !important;   /* tell browser: use light colours */
        }
        
        /* main containers */
            html,
            body,
            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stAppViewBlockContainer"],
            main,
            .block-container,
            [data-testid="stHeader"],
            section[data-testid="stSidebar"] {
                background-color: #ffffff !important;
            }
        /* SMALLER SCREENS */
        @media (max-width: 900px) {
            .header-title {
                font-size: 26px;
            }
            .section-title {
                font-size: 18px;
            }
            .section-text {
                font-size: 13px;
            }
            .equal-card {
                min-height: auto;
            }
        }

        button[kind="secondary"] {
            background-color: #4a90e2 !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 12px 30px !important;
            font-weight: 600 !important;
            border: none !important;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# LOAD LOTTIE (used in HOME)
# =====================================================================

def load_lottiefile(filename: str):
    file_path = ANIM_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


lottie_students = load_lottiefile("Group of people communicating.json")
lottie_thinking = load_lottiefile("Thinking.json")

# =====================================================================
# APP HEADER (TITLE + SUBTITLE)
# =====================================================================
st.markdown(
    """
    <h1 class="fade-title" style="text-align:center; font-weight:700;">
        STUDENT MENTAL WELLNESS DASHBOARD
    </h1>

    <p class="fade-sub" style="text-align:center; font-size:17px; color:#555;">
        "Understanding Your Journey to Wellbeing"
    </p>
    """,
    unsafe_allow_html=True,
)

# =======================
# NAV TABS (WITH STATE)
# =======================
TAB_OPTIONS = [
    "HOME",
    "WHO WE ARE",
    "THE UNTOLD SIDE",
    "KNOW YOURSELF",
]

# 1) Initialise nav_tabs once
if "nav_tabs" not in st.session_state:
    st.session_state["nav_tabs"] = "HOME"

# 2) Handle jump from START EXPLORING button BEFORE radio renders
if st.session_state.get("go_to_who_we_are"):
    st.session_state["nav_tabs"] = "WHO WE ARE"
    st.session_state["go_to_who_we_are"] = False

# 3) Jump form who we are to the untold side
if st.session_state.get("go_to_untold_side"):
    st.session_state["nav_tabs"] = "THE UNTOLD SIDE"
    st.session_state["go_to_untold_side"] = False

# 4) From untold side to know yourself
if st.session_state.get("go_to_know_yourself"):
    st.session_state["nav_tabs"] = "KNOW YOURSELF"
    st.session_state["go_to_know_yourself"] = False  # reset flag

left_gap, tab_col, right_gap = st.columns([1, 6, 1])

with tab_col:
    st.radio(
        label="Navigation",
        options=TAB_OPTIONS,
        horizontal=True,
        key="nav_tabs",
        label_visibility="collapsed",
    )

tab = st.session_state["nav_tabs"]

# =====================================================================
# TAB: HOME
# =====================================================================
if tab == "HOME":
    # ------------------ HERO SECTION ------------------
    centerA, centerB, centerC = st.columns([1, 2, 1])

    with centerB:
        st_lottie(lottie_students, height=320, key="main_lottie")

        st.markdown(
            """
            <div style='text-align:center; font-size:20px; font-weight:700; margin-top:10px;'>
                WELCOME TO YOUR MENTAL WELLNESS HUB
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style='text-align:center; font-size:15px;'>
                "Mental health matters. Let's explore together what affects<br>
                student wellbeing in Malaysia."
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown(
        """
        <div class='section-text' style='text-align:center; max-width:750px; margin: 0 auto;'>
            This dashboard is built to help students pause, reflect, and understand how different parts of life 
            – academics, money, relationships, sleep, and stress – are linked to mental wellness.  
            You are not alone, and your feelings are valid.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------ VIDEO + INFO ------------------
    st.write("")
    st.markdown("### Learn About Mental Health")

    col_video, col_info = st.columns(2)

    with col_video:
        st.markdown(
            """
            <div class="equal-card">
              <div class="video-frame">
                <iframe
                  src="https://www.youtube.com/embed/gWs-AswW398"
                  title="Let's Talk About Mental Health and Wellness"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowfullscreen>
                </iframe>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_info:
        st.markdown(
            """
            <div class="equal-card">
              <h4>Why this video matters</h4>

              <p>
                This video introduces what mental health really means in everyday life. It reminds us that:
              </p>

              <ul>
                <li>Mental health is not just about “being happy” — it includes how we think, feel, and cope.</li>
                <li>Anyone can experience stress, anxiety, or low mood, especially during exam season.</li>
                <li>Talking to someone and seeking professional help is a strong and healthy step.</li>
              </ul>

              <p style="margin-top: 12px;">
                As students, we often carry many invisible pressures — assignments, finances, family expectations,
                and our own goals. Watching this video is a small first step to understand that mental health is real,
                normal, and something we <b>can</b> take care of.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------ WHY IT MATTERS ------------------
    st.write("")
    st.write("")

    left_lottie, right_text = st.columns([1, 2])

    with left_lottie:
        st_lottie(lottie_thinking, height=260, key="thinking_lottie")

    with right_text:
        st.markdown(
            "<div class='section-title'>Why Student Mental Health Matters</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class='section-text'>
                University life is exciting, but it can also be overwhelming. Many students quietly struggle with:
                <ul>
                    <li>Heavy coursework, deadlines, and exams</li>
                    <li>Financial worries and part-time work</li>
                    <li>Family expectations and responsibilities</li>
                    <li>Loneliness, homesickness, or relationship issues</li>
                </ul>
                Mental health challenges are common – and they are <b>not</b> a sign of weakness.<br>
                This dashboard aims to bring these issues into the open, so we can talk about them
                and support one another.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ------------------ 3 STAT CARDS ------------------
    st.markdown("")

    col1, col2, col3 = st.columns(3)

    box_style = """
        padding: 26px;
        border-radius: 22px;
        min-height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    """

    inner_card = """
        background: white;
        padding: 20px 25px;
        border-radius: 14px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.10);
        text-align: center;
        font-size: 15px;
        flex-grow: 1;
        display: flex;
        align-items: center;
        justify-content: center;
    """

    with col1:
        st.markdown(
            f"""
            <div style="{box_style} background: linear-gradient(135deg, #ff4d4d, #cc0000);">
                <div style="text-align:center; font-size:20px; font-weight:700; color:white;">
                    📊 QUICK STATS
                </div>
                <div style="height:18px;"></div>
                <div style="{inner_card}">
                    312 students shared their experiences<br>
                    from different universities and backgrounds.<br><br>
                    Their responses help us see patterns<br>
                    in stress, coping, and wellbeing.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="{box_style} background: linear-gradient(135deg, #28c76f, #009f4d);">
                <div style="text-align:center; font-size:20px; font-weight:700; color:white;">
                    👥 OUR COMMUNITY
                </div>
                <div style="height:18px;"></div>
                <div style="{inner_card}">
                    Behind every data point is a real person.
                    Some are thriving, some are coping,
                    and some are struggling in silence.
                    This space reminds you:
                    you are not alone.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div style="{box_style} background: linear-gradient(135deg, #3a7bd5, #0052cc);">
                <div style="text-align:center; font-size:20px; font-weight:700; color:white;">
                    🎯 OUR GOAL
                </div>
                <div style="height:18px;"></div>
                <div style="{inner_card} text-align:left;">
                    • Build awareness about mental wellness<br>
                    • Encourage honest conversations<br>
                    • Help students notice their own patterns<br>
                    • Point towards support and next steps
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ------------------ CHECK-IN CORNER ------------------
    st.markdown("### 💬 Check-in Corner")

    col_check1, col_check2 = st.columns(2)

    with col_check1:
        mood = st.slider(
            "How are you feeling today on a scale of 1–10?",
            min_value=1,
            max_value=10,
            value=5,
        )

        if mood <= 3:
            st.warning(
                "It sounds like you're having a tough day. It's okay to feel this way. "
                "Reaching out to someone you trust can really help. 💛"
            )
        elif 4 <= mood <= 7:
            st.info(
                "You seem to be somewhere in the middle – not great, not terrible. "
                "Small breaks, movement, or talking to a friend might make today a bit lighter. 💙"
            )
        else:
            st.success(
                "That's wonderful to hear! Keep doing what supports your mental wellbeing – "
                "and check in on friends who may need a boost. 🌱"
            )

    with col_check2:
        stress_source = st.selectbox(
            "What is stressing you the most right now?",
            [
                "Assignments & exams",
                "Time management",
                "Family expectations",
                "Money & finances",
                "Relationships / friendships",
                "Health & sleep",
                "I’m not sure",
            ],
        )

        if stress_source == "Assignments & exams":
            st.write(
                "📚 Try breaking big tasks into smaller parts and study in focused blocks "
                "(like 25 minutes). It feels less overwhelming."
            )
        elif stress_source == "Time management":
            st.write(
                "⏰ A simple to-do list or weekly planner can help you see your time clearly "
                "and reduce mental clutter."
            )
        elif stress_source == "Family expectations":
            st.write(
                "🏠 You're not alone. Many students feel this. Setting small personal goals "
                "that matter to you can balance internal and external expectations."
            )
        elif stress_source == "Money & finances":
            st.write(
                "💸 Consider tracking your spending for a week. Small awareness steps can "
                "reduce anxiety and help you plan better."
            )
        elif stress_source == "Relationships / friendships":
            st.write(
                "💌 Healthy connections take time and communication. It’s okay to set "
                "boundaries and also to ask for support when you need it."
            )
        elif stress_source == "Health & sleep":
            st.write(
                "😴 Regular sleep, simple movement, and proper meals are basics that strongly "
                "support mental health. Start with one small habit."
            )
        else:
            st.write(
                "🌫️ It's okay not to have a clear answer. Sometimes we just feel 'off'. "
                "Checking in with yourself is already a brave first step."
            )

    st.markdown("---")

    # ------------------ START EXPLORING BUTTON ------------------
    center_btn = st.columns([4, 2, 4])[1]

    with center_btn:
        if st.button("START EXPLORING ➜", key="go_explore"):
            st.session_state["go_to_who_we_are"] = True
            st.rerun()


# =====================================================================
# TAB: WHO WE ARE
# =====================================================================
elif tab == "WHO WE ARE":
    # 1. Render the WHO WE ARE page
    run_who_we_are_tab()

# =====================================================================
# TAB: THE UNTOLD SIDE  (call external module)
# =====================================================================
elif tab == "THE UNTOLD SIDE":
    render_untold_side()

# =====================================================================a
# TAB: KNOW YOURSELF  (call external module)
# =====================================================================
elif tab == "KNOW YOURSELF":
    run_mental_wellness_tab()
