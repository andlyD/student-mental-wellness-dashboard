# know_yourself.py
import streamlit as st
import pandas as pd
import time
import plotly.express as px
from pathlib import Path
import os


# ----------------------------------------------------
# Helper: classification logic (0–30 -> 3 levels)
# ----------------------------------------------------
def classify_stress(total_score):
    """
    Classify the summed score (0-30) into three levels:
    - 0-9   -> "Minimal and Mild"
    - 10-19 -> "Moderate"
    - 20-30 -> "Severe"
    """
    try:
        total_score = int(total_score)
    except Exception:
        # fallback in case of unexpected input
        return "Severe"

    if total_score <= 9:
        return "Minimal and Mild"
    if total_score <= 19:
        return "Moderate"
    return "Severe"

BASE_DIR = Path(__file__).resolve().parents[1]
VIDEO_PATH = BASE_DIR / "assets" / "video" / "VID_0955.mp4"

def run_mental_wellness_tab():
    # -----------------------------
    # Global CSS for header + cards
    # -----------------------------
    st.markdown(
        """
        <style>
        .main-header {
            text-align: center;
            background: royalblue;
            color: #FFFFFF;
            font-size: 3rem;
            font-weight: 900;
            padding: 2.5rem 2rem;
            border-radius: 20px;
            margin-bottom: 3rem;
            box-shadow: 0 10px 30px rgba(65, 105, 225, 0.3);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        .header-subtitle {
            text-align: center;
            font-size: 1.2rem;
            font-weight: 400;
            margin-top: -1.5rem;
            margin-bottom: 2.5rem;
            color: #455A64;
            font-style: italic;
            letter-spacing: 1px;
        }
        .question-card {
            border-radius: 18px;
            padding: 14px 18px;
            background: #ffffff;
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
            margin-bottom: 8px;
        }
        .question-title {
            font-weight: 700;
            font-size: 1rem;
            margin-bottom: 4px;
        }
        .question-scene {
            font-size: 0.9rem;
            color: #374151;
        }

        /* ====== ONLY STYLE RADIOS USED FOR QUESTIONS ======
           (the radio that comes right after .question-card) */
        .question-card + div.stRadio {
            max-width: 900px;
            margin: -5px auto 15px auto;
            padding: 0 18px;
        }
        .question-card + div.stRadio > div {
            display: flex !important;
            justify-content: space-between !important;
            align-items: center;
            width: 100%;        /* no 135% overflow */
        }
        .question-card + div.stRadio > div > label {
            flex: 1;
            text-align: center;
            white-space: nowrap;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------
    # Header block (HTML only)
    # -----------------------------
    st.markdown(
        """
        <div class="main-header">
            Know Your Wellness Level
        </div>
        <div class="header-subtitle">
            “Understanding patterns is great. But what about <b>YOU</b> personally?”
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------
    # Intro + instructions
    # -----------------------------
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px; margin-top:10px;">
            <span style="font-size:22px;">🧬</span>
            <span style="font-size:22px; font-weight:700;">Your Mental Wellness Check</span>
        </div>
        <p style="margin-top:4px; margin-bottom:4px;">
            Fill in the following to get your personalised assessment.
        </p>

        <div style="
            margin-top:6px;
            padding:10px 14px;
            border-radius:10px;
            background-color:#fffbeb;
            border:1px solid #facc15;
            font-size:13px;
            line-height:1.5;
        ">
            ⚠️ <b>Important:</b> Please answer <b>all 10 questions</b> honestly.  
            You’ll only see your result <b>after every question is completed</b>.
            <br/>
            <span style="color:#6b7280;">Your responses are anonymous and not stored.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==============================
    # Question block
    # ==============================
    questions = [
        {"icon": "🌅", "title": "Scene 1: Morning in Dorm",
         "prompt": "When you wake up and think about the day ahead, how often do you already feel stressed or overwhelmed by your responsibilities?"},
        {"icon": "📚", "title": "Scene 2: Short Break Between Classes",
         "prompt": "During your free time, how often do you find it hard to relax, even when you are supposed to rest?"},
        {"icon": "🏃‍♂️", "title": "Scene 3: Rushing to Lecture",
         "prompt": "On the way to class or while getting ready, how often do you feel tense, worried, or 'on edge'?"},
        {"icon": "🌙", "title": "Scene 4: Late at Night",
         "prompt": "When you try to sleep, how often do your thoughts or overthinking keep you awake?"},
        {"icon": "🛏️", "title": "Scene 5: Alone in Your Room",
         "prompt": "When you are alone, how often do you feel sad, low, or emotionally drained?"},
        {"icon": "📝", "title": "Scene 6: Looking at Assignments or Grades",
         "prompt": "How often do you worry a lot about mistakes, marks, or your future plans?"},
        {"icon": "🎮", "title": "Scene 7: Free Time or Hobbies",
         "prompt": "When you do activities you usually enjoy, how often do you still feel like you can’t fully enjoy them?"},
        {"icon": "🤝", "title": "Scene 8: Group Work or Social Situations",
         "prompt": "Around other people, how often do you get irritated or frustrated more easily than usual?"},
        {"icon": "😮‍💨", "title": "Scene 9: End of the Day",
         "prompt": "After a normal day, how often do you feel unusually tired or exhausted, even if you haven’t done that much?"},
        {"icon": "🚪", "title": "Scene 10: Choosing What to Do",
         "prompt": "When deciding how to spend your time, how often do you feel like withdrawing and avoiding others?"},
    ]

    label_to_score = {
        "0 - Never": 0,
        "1 - Sometimes": 1,
        "2 - Often": 2,
        "3 - Almost always": 3,
    }

    st.markdown("#### ✏️ Answer the questions below")

    scores = []
    answered_count = 0

    for i, q in enumerate(questions):
        st.markdown(
            f"""
            <div class="question-card">
                <div class="question-title">{q['icon']} {q['title']}</div>
                <div class="question-scene">{q['prompt']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        choice = st.radio(
            label=" ",
            options=list(label_to_score.keys()),
            index=None,                     # 👈 start with no selection
            key=f"q{i+1}",
            horizontal=True,
            label_visibility="collapsed",
        )

        if choice is not None:
            scores.append(label_to_score[choice])
            answered_count += 1
        else:
            scores.append(None)

    # Progress bar
    progress = answered_count / len(questions)
    st.write("")
    st.write(f"✅ Answered {answered_count} / {len(questions)} questions")
    st.progress(progress)
    st.write("")

    # ==============================
    # PREDICT BUTTON
    # ==============================
    analyze_button = st.button("🤖 Predict My Wellness Level")

    # Store results in session state
    if analyze_button:
        if None in scores:
            st.warning("⚠️ Please answer **all 10 questions** before checking your wellness level.")
            return

        with st.spinner("Analyzing your responses..."):
            time.sleep(2)

        total_score = sum(scores)
        level = classify_stress(total_score)
        
        # CRITICAL: Save to session state
        st.session_state.analysis_complete = True
        st.session_state.total_score = total_score
        st.session_state.level = level
        st.session_state.scores = scores

    # Check if analysis has been completed
    if st.session_state.get('analysis_complete', False):
        # Retrieve from session state
        total_score = st.session_state.total_score
        level = st.session_state.level
        scores = st.session_state.scores

        st.markdown("---")
        st.markdown("### 📊 Your Results")


        # ----- Colour scheme based on level -----
        if level == "Minimal and Mild":
            card_bg = "#ecfdf5"
            card_border = "#6ee7b7"
            level_color = "#047857"
            level_icon = "🟢"
            result_message = "Your answers show minimal to mild stress. You seem to be coping well, but keep paying attention to how you feel."
        elif level == "Moderate":
            card_bg = "#fffbeb"
            card_border = "#fbbf24"
            level_color = "#92400e"
            level_icon = "🟠"
            result_message = "Your responses show moderate stress. This is common, and talking to someone you trust or using simple coping strategies can help."
        else:  # Severe
            card_bg = "#fef2f2"
            card_border = "#f87171"
            level_color = "#b91c1c"
            level_icon = "🔴"
            result_message = "Your score is in the Severe range. Don't worry, this test does not diagnose anything. It only suggests that you may benefit from extra support, and reaching out to a mental health professional can be helpful."

        # ----- Result card -----
        st.markdown(
            f"""
            <div style="
                border-radius: 18px;
                padding: 18px 20px;
                background-color: {card_bg};
                border: 1px solid {card_border};
                margin-bottom: 18px;
            ">
                <h4 style="margin-bottom: 6px; display:flex; align-items:center; gap:8px;">
                    <span>{level_icon}</span>
                    <span style="
                        font-weight: 800;
                        letter-spacing: 0.5px;
                        color: {level_color};
                        text-shadow: 0 1px 3px rgba(0,0,0,0.25);
                    ">
                        Your Wellness Level: {level.upper()}
                    </span>
                </h4>
                <p style="margin-top: 4px; margin-bottom: 0; color:#111827;">
                    {result_message}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ----- Gauge bar -----
        st.markdown("#### 🧭 Where you are on the depression scale")

        gauge_cols = st.columns([1, 6, 1])
        with gauge_cols[1]:
            position_pct = (total_score / 30) * 100  # 0–100%

            st.markdown(
                f"""
                <div style="margin-top:8px; margin-bottom:12px;">
                    <div style="
                        position: relative;
                        height: 16px;
                        border-radius: 999px;
                        background: linear-gradient(
                            90deg,
                            #22c55e 0%,
                            #a3e635 20%,
                            #facc15 40%,
                            #fb923c 65%,
                            #ef4444 100%
                        );
                        box-shadow: inset 0 1px 3px rgba(0,0,0,0.25);
                    ">
                        <div style="
                            position: absolute;
                            top: 0px;
                            left: calc({position_pct}% - 8px);
                            width: 16px;
                            height: 16px;
                            border-radius: 999px;
                            background: #ffffff;
                            border: 2px solid #111827;
                            box-shadow: 0 0 6px rgba(0,0,0,0.35);
                        "></div>
                    </div>
                    <div style="
                        display:flex;
                        justify-content:space-between;
                        font-size:12px;
                        color:#4b5563;
                        margin-top:4px;
                    ">
                        <span>Minimal</span>
                        <span>Moderate</span>
                        <span>Severe</span>
                    </div>
                    <div style="text-align:center; font-size:11px; color:#6b7280; margin-top:2px;">
                        ● shows your current position on the depression scale
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ==============================
        # What's driving your result?
        # ==============================
        st.markdown("### 💡 What's driving your result?")

        factor_scores = {
            "Worry & Overthinking": scores[0] + scores[1] + scores[2] + scores[5],
            "Sleep & Fatigue": scores[3] + scores[8],
            "Mood & Enjoyment": scores[4] + scores[6],
            "Irritability & Withdrawal": scores[7] + scores[9],
        }

        factor_df = pd.DataFrame({
            "Factor": list(factor_scores.keys()),
            "Score": list(factor_scores.values())
        })

        # Define colors for each factor
        color_map = {
            "Irritability & Withdrawal": "deeppink",
            "Mood & Enjoyment": "orange",
            "Sleep & Fatigue": "firebrick",
            "Worry & Overthinking": "blueviolet"
        }

        factor_df["Color"] = factor_df["Factor"].map(color_map)

        fig = px.bar(factor_df, x="Factor", y="Score", 
                    color="Factor",
                    color_discrete_map=color_map)

        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="",
            yaxis_title="Impact Score",
            xaxis_tickangle=0  # This makes labels horizontal (flat/readable)
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("The higher the bar, the more that area is contributing to your current wellness level.")

        # ==============================
        # Explanation expander
        # ==============================
        st.markdown("### Understanding your result")

        with st.expander("Click to read a simple explanation"):
            if level == "Minimal and Mild":
                st.write(
                    "- Your responses suggest that your stress is currently at a **manageable level**.\n"
                    "- You might still face pressure at times, but overall you are coping relatively well.\n"
                    "- Many students in this range benefit from keeping healthy routines and staying connected with friends."
                )
            elif level == "Moderate":
                st.write(
                    "- Your result indicates **moderate stress**, which means your mood, sleep, or energy may be affected.\n"
                    "- You’re still managing day to day, but these challenges might be making things feel heavier.\n"
                    "- Many students in this range feel better after adjusting their workload, using campus support, "
                    "or talking to someone they trust."
                )
            else:  # Severe
                st.write(
                    "- Your answers show a **high level of stress**, which may strongly affect your mood, energy, and focus.\n"
                    "- It is important not to ignore these signs. Reaching out for support can really help.\n"
                    "- Consider talking to a counsellor, mental health professional, or a trusted person in your life. "
                    "You do not have to handle everything alone."
                )

        st.caption(
            "⚠️ This screening is only for reflection and does not replace professional assessment or treatment."
        )


        st.markdown("**Based on your wellness level, here are some recommended actions**")

        # ------- MINIMAL & MILD: GAMES -------
        if level == "Minimal and Mild":
            # Import components at the very beginning
            import streamlit.components.v1 as components
            
            st.markdown("#### 🎮 Take a Mental Break: Play a Game!")
            st.markdown("You're doing well! Here's a fun game to help you relax and take a quick break.")
            
            # Game selection
            game_choice = st.radio(
                "Choose a game:",
                ["Gravity Jump Game", "Memory Puzzle Game", "Tic-Tac-Toe Game"],
                horizontal=True
            )
            
            # ============== GRAVITY JUMP GAME ==============
            if game_choice == "Gravity Jump Game":
                # How to Play instructions for Gravity Game
                st.markdown("""
                **How to Play:**
                - Use the UP button to make the red square jump
                - Use LEFT/RIGHT buttons to move horizontally
                - Use DOWN button to fall faster
                - Avoid the green obstacles
                - Try to get the highest score!
                - Game ends when you hit an obstacle
                """)
                
                # Initialize game state
                if 'game_started' not in st.session_state:
                    st.session_state.game_started = False
                if 'game_restart_count' not in st.session_state:
                    st.session_state.game_restart_count = 0
                
                # Start/Restart button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if not st.session_state.game_started:
                        if st.button("▶️ Start Game", use_container_width=True, key="start_gravity"):
                            st.session_state.game_started = True
                            st.rerun()
                    else:
                        if st.button("🔄 Restart Game", use_container_width=True, key="restart_gravity"):
                            st.session_state.game_restart_count += 1
                            st.rerun()
                
                # Show game only if started
                if st.session_state.game_started:
                    game_key = st.session_state.game_restart_count
                    
                    game_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                        <style>
                            body {{
                                margin: 0;
                                padding: 20px;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                background-color: #f0f0f0;
                            }}
                            canvas {{
                                border: 2px solid #333;
                                background-color: #f1f1f1;
                                margin-bottom: 20px;
                            }}
                            .controls {{
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                gap: 10px;
                            }}
                            .control-row {{
                                display: flex;
                                gap: 10px;
                            }}
                            button {{
                                width: 80px;
                                height: 50px;
                                font-size: 16px;
                                font-weight: bold;
                                border: 2px solid #333;
                                border-radius: 8px;
                                background-color: #4CAF50;
                                color: white;
                                cursor: pointer;
                                transition: all 0.2s;
                            }}
                            button:active {{
                                background-color: #45a049;
                                transform: scale(0.95);
                            }}
                            button:hover {{
                                background-color: #45a049;
                            }}
                        </style>
                    </head>
                    <body onload="startGame()">
                    <!-- Game instance: {game_key} -->

                    <script>
                    var myGamePiece;
                    var myObstacles = [];
                    var myScore;

                    function startGame() {{
                        myGamePiece = new component(30, 30, "red", 10, 120);
                        myGamePiece.gravity = 0.05;
                        myScore = new component("30px", "Consolas", "black", 280, 40, "text");
                        myGameArea.start();
                    }}

                    var myGameArea = {{
                        canvas : document.createElement("canvas"),
                        start : function() {{
                            this.canvas.width = 480;
                            this.canvas.height = 270;
                            this.context = this.canvas.getContext("2d");
                            document.body.insertBefore(this.canvas, document.body.childNodes[0]);
                            this.frameNo = 0;
                            this.interval = setInterval(updateGameArea, 20);
                        }},
                        clear : function() {{
                            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
                        }},
                        stop : function() {{
                            clearInterval(this.interval);
                        }}
                    }}

                    function component(width, height, color, x, y, type) {{
                        this.type = type;
                        this.score = 0;
                        this.width = width;
                        this.height = height;
                        this.speedX = 0;
                        this.speedY = 0;    
                        this.x = x;
                        this.y = y;
                        this.gravity = 0;
                        this.gravitySpeed = 0;
                        this.update = function() {{
                            ctx = myGameArea.context;
                            if (this.type == "text") {{
                                ctx.font = this.width + " " + this.height;
                                ctx.fillStyle = color;
                                ctx.fillText(this.text, this.x, this.y);
                            }} else {{
                                ctx.fillStyle = color;
                                ctx.fillRect(this.x, this.y, this.width, this.height);
                            }}
                        }}
                        this.newPos = function() {{
                            this.gravitySpeed += this.gravity;
                            this.x += this.speedX;
                            this.y += this.speedY + this.gravitySpeed;
                            this.hitBottom();
                            this.hitSides();
                        }}
                        this.hitBottom = function() {{
                            var rockbottom = myGameArea.canvas.height - this.height;
                            if (this.y > rockbottom) {{
                                this.y = rockbottom;
                                this.gravitySpeed = 0;
                            }}
                        }}
                        this.hitSides = function() {{
                            if (this.x < 0) {{
                                this.x = 0;
                            }}
                            if (this.x > myGameArea.canvas.width - this.width) {{
                                this.x = myGameArea.canvas.width - this.width;
                            }}
                        }}
                        this.crashWith = function(otherobj) {{
                            var myleft = this.x;
                            var myright = this.x + (this.width);
                            var mytop = this.y;
                            var mybottom = this.y + (this.height);
                            var otherleft = otherobj.x;
                            var otherright = otherobj.x + (otherobj.width);
                            var othertop = otherobj.y;
                            var otherbottom = otherobj.y + (otherobj.height);
                            var crash = true;
                            if ((mybottom < othertop) || (mytop > otherbottom) || (myright < otherleft) || (myleft > otherright)) {{
                                crash = false;
                            }}
                            return crash;
                        }}
                    }}

                    function updateGameArea() {{
                        var x, height, gap, minHeight, maxHeight, minGap, maxGap;
                        for (i = 0; i < myObstacles.length; i += 1) {{
                            if (myGamePiece.crashWith(myObstacles[i])) {{
                                myGameArea.stop();
                                return;
                            }} 
                        }}
                        myGameArea.clear();
                        myGameArea.frameNo += 1;
                        if (myGameArea.frameNo == 1 || everyinterval(150)) {{
                            x = myGameArea.canvas.width;
                            minHeight = 20;
                            maxHeight = 200;
                            height = Math.floor(Math.random()*(maxHeight-minHeight+1)+minHeight);
                            minGap = 50;
                            maxGap = 200;
                            gap = Math.floor(Math.random()*(maxGap-minGap+1)+minGap);
                            myObstacles.push(new component(10, height, "green", x, 0));
                            myObstacles.push(new component(10, x - height - gap, "green", x, height + gap));
                        }}
                        for (i = 0; i < myObstacles.length; i += 1) {{
                            myObstacles[i].x += -1;
                            myObstacles[i].update();
                        }}
                        myScore.text="SCORE: " + myGameArea.frameNo;
                        myScore.update();
                        myGamePiece.newPos();
                        myGamePiece.update();
                    }}

                    function everyinterval(n) {{
                        if ((myGameArea.frameNo / n) % 1 == 0) {{return true;}}
                        return false;
                    }}

                    function moveUp() {{
                        myGamePiece.gravitySpeed = -1.5;
                    }}

                    function moveLeft() {{
                        myGamePiece.speedX = -3;
                    }}

                    function moveRight() {{
                        myGamePiece.speedX = 3;
                    }}

                    function moveDown() {{
                        myGamePiece.gravitySpeed = 2;
                    }}

                    function stopMove() {{
                        myGamePiece.speedX = 0;
                    }}
                    </script>

                    <div class="controls">
                        <div class="control-row">
                            <button onmousedown="moveUp()" onmouseup="stopMove()">UP</button>
                        </div>
                        <div class="control-row">
                            <button onmousedown="moveLeft()" onmouseup="stopMove()">LEFT</button>
                            <button onmousedown="moveRight()" onmouseup="stopMove()">RIGHT</button>
                        </div>
                        <div class="control-row">
                            <button onmousedown="moveDown()" onmouseup="stopMove()">DOWN</button>
                        </div>
                    </div>

                    </body>
                    </html>
                    """
                    
                    components.html(game_html, height=500, scrolling=False)
            
            # ============== MEMORY PUZZLE GAME ==============
            elif game_choice == "Memory Puzzle Game":
                st.markdown("""
                **How to Play:**
                - Click on cards to flip them
                - Find matching pairs of cards
                - Match all pairs before time runs out (60 seconds)
                - Try to complete it in fewer moves!
                """)
                
                # Initialize memory game state
                if 'memory_game_started' not in st.session_state:
                    st.session_state.memory_game_started = False
                if 'memory_restart_count' not in st.session_state:
                    st.session_state.memory_restart_count = 0
                
                # Start/Restart button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if not st.session_state.memory_game_started:
                        if st.button("▶️ Start Memory Game", use_container_width=True, key="start_memory"):
                            st.session_state.memory_game_started = True
                            st.rerun()
                    else:
                        if st.button("🔄 Restart Memory Game", use_container_width=True, key="restart_memory"):
                            st.session_state.memory_restart_count += 1
                            st.rerun()
                
                if st.session_state.memory_game_started:
                    memory_key = st.session_state.memory_restart_count
                    
                    memory_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {{
                                margin: 0;
                                padding: 20px;
                                background-color: #2c3e50;
                                font-family: Arial, sans-serif;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                            }}
                            .game-container {{
                                text-align: center;
                            }}
                            .stats {{
                                display: flex;
                                justify-content: space-around;
                                width: 400px;
                                margin-bottom: 20px;
                                color: white;
                                font-size: 18px;
                            }}
                            .grid {{
                                display: grid;
                                grid-template-columns: repeat(4, 100px);
                                grid-gap: 10px;
                                margin: 20px auto;
                            }}
                            .card {{
                                width: 100px;
                                height: 100px;
                                background-color: #3498db;
                                border-radius: 8px;
                                cursor: pointer;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-size: 40px;
                                transition: transform 0.3s;
                            }}
                            .card:hover {{
                                transform: scale(1.05);
                            }}
                            .card.flipped {{
                                background-color: #ecf0f1;
                            }}
                            .card.matched {{
                                background-color: #2ecc71;
                                cursor: default;
                            }}
                            .message {{
                                color: white;
                                font-size: 24px;
                                margin-top: 20px;
                                font-weight: bold;
                            }}
                            .restart-btn {{
                                background-color: #e74c3c;
                                color: white;
                                border: none;
                                padding: 10px 20px;
                                font-size: 16px;
                                border-radius: 5px;
                                cursor: pointer;
                                margin-top: 15px;
                            }}
                            .restart-btn:hover {{
                                background-color: #c0392b;
                            }}
                        </style>
                    </head>
                    <body>
                    <!-- Game instance: {memory_key} -->
                    
                    <div class="game-container">
                        <div class="stats">
                            <div>Moves: <span id="moves">0</span></div>
                            <div>Time: <span id="timer">60</span>s</div>
                            <div>Pairs: <span id="pairs">0</span>/8</div>
                        </div>
                        <div class="grid" id="grid"></div>
                        <div class="message" id="message"></div>
                        <button class="restart-btn" onclick="restartGame()">Restart Game</button>
                    </div>

                    <script>
                    const emojis = ['🍎', '🍌', '🍇', '🍊', '🍓', '🍉', '🍒', '🍑'];
                    let cards = [...emojis, ...emojis];
                    let flippedCards = [];
                    let matchedPairs = 0;
                    let moves = 0;
                    let timeLeft = 60;
                    let timerInterval;
                    let gameActive = true;

                    function shuffle(array) {{
                        for (let i = array.length - 1; i > 0; i--) {{
                            const j = Math.floor(Math.random() * (i + 1));
                            [array[i], array[j]] = [array[j], array[i]];
                        }}
                        return array;
                    }}

                    function createBoard() {{
                        const grid = document.getElementById('grid');
                        grid.innerHTML = '';
                        shuffle(cards);
                        
                        cards.forEach((emoji, index) => {{
                            const card = document.createElement('div');
                            card.className = 'card';
                            card.dataset.emoji = emoji;
                            card.dataset.index = index;
                            card.addEventListener('click', flipCard);
                            grid.appendChild(card);
                        }});
                    }}

                    function flipCard() {{
                        if (!gameActive) return;
                        if (flippedCards.length >= 2) return;
                        if (this.classList.contains('flipped') || this.classList.contains('matched')) return;

                        this.classList.add('flipped');
                        this.textContent = this.dataset.emoji;
                        flippedCards.push(this);

                        if (flippedCards.length === 2) {{
                            moves++;
                            document.getElementById('moves').textContent = moves;
                            checkMatch();
                        }}
                    }}

                    function checkMatch() {{
                        const [card1, card2] = flippedCards;
                        
                        if (card1.dataset.emoji === card2.dataset.emoji) {{
                            card1.classList.add('matched');
                            card2.classList.add('matched');
                            matchedPairs++;
                            document.getElementById('pairs').textContent = matchedPairs;
                            flippedCards = [];
                            
                            if (matchedPairs === 8) {{
                                endGame(true);
                            }}
                        }} else {{
                            setTimeout(() => {{
                                card1.classList.remove('flipped');
                                card2.classList.remove('flipped');
                                card1.textContent = '';
                                card2.textContent = '';
                                flippedCards = [];
                            }}, 800);
                        }}
                    }}

                    function startTimer() {{
                        timerInterval = setInterval(() => {{
                            timeLeft--;
                            document.getElementById('timer').textContent = timeLeft;
                            
                            if (timeLeft <= 0) {{
                                endGame(false);
                            }}
                        }}, 1000);
                    }}

                    function endGame(won) {{
                        gameActive = false;
                        clearInterval(timerInterval);
                        const message = document.getElementById('message');
                        
                        if (won) {{
                            message.textContent = `🎉 Congratulations! You won in ${{moves}} moves!`;
                        }} else {{
                            message.textContent = "⏰ Time's up! Try again!";
                        }}
                    }}

                    function restartGame() {{
                        gameActive = true;
                        matchedPairs = 0;
                        moves = 0;
                        timeLeft = 60;
                        flippedCards = [];
                        
                        document.getElementById('moves').textContent = 0;
                        document.getElementById('timer').textContent = 60;
                        document.getElementById('pairs').textContent = 0;
                        document.getElementById('message').textContent = '';
                        
                        clearInterval(timerInterval);
                        createBoard();
                        startTimer();
                    }}

                    // Initialize game
                    createBoard();
                    startTimer();
                    </script>

                    </body>
                    </html>
                    """
                    
                    components.html(memory_html, height=600, scrolling=False)
            
            # ============== TIC-TAC-TOE GAME ==============
            else:  # Tic-Tac-Toe Game
                st.markdown("""
                **How to Play:**
                - You are X, Computer is O
                - Click on any empty cell to place your X
                - Computer will automatically make its move
                - Get 3 in a row (horizontal, vertical, or diagonal) to win!
                - If all cells are filled with no winner, it's a tie
                """)
                
                # Initialize tic-tac-toe game state
                if 'tictactoe_started' not in st.session_state:
                    st.session_state.tictactoe_started = False
                if 'tictactoe_restart_count' not in st.session_state:
                    st.session_state.tictactoe_restart_count = 0
                
                # Start/Restart button
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if not st.session_state.tictactoe_started:
                        if st.button("▶️ Start Tic-Tac-Toe", use_container_width=True, key="start_tictactoe"):
                            st.session_state.tictactoe_started = True
                            st.rerun()
                    else:
                        if st.button("🔄 Restart Tic-Tac-Toe", use_container_width=True, key="restart_tictactoe"):
                            st.session_state.tictactoe_restart_count += 1
                            st.rerun()
                
                if st.session_state.tictactoe_started:
                    tictactoe_key = st.session_state.tictactoe_restart_count
                    
                    tictactoe_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {{
                                margin: 0;
                                padding: 20px;
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                font-family: 'Arial', sans-serif;
                                display: flex;
                                flex-direction: column;
                                align-items: center;
                                min-height: 100vh;
                            }}
                            .game-container {{
                                text-align: center;
                                background: white;
                                padding: 30px;
                                border-radius: 20px;
                                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                            }}
                            .status {{
                                font-size: 24px;
                                font-weight: bold;
                                margin-bottom: 20px;
                                color: #667eea;
                                min-height: 30px;
                            }}
                            .board {{
                                display: grid;
                                grid-template-columns: repeat(3, 120px);
                                grid-template-rows: repeat(3, 120px);
                                gap: 10px;
                                margin: 20px auto;
                            }}
                            .cell {{
                                background: #f0f0f0;
                                border: 3px solid #667eea;
                                border-radius: 10px;
                                font-size: 48px;
                                font-weight: bold;
                                cursor: pointer;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                transition: all 0.3s;
                            }}
                            .cell:hover {{
                                background: #e8e8e8;
                                transform: scale(1.05);
                            }}
                            .cell.x {{
                                color: #e74c3c;
                            }}
                            .cell.o {{
                                color: #3498db;
                            }}
                            .cell.winner {{
                                background: #2ecc71;
                                color: white;
                            }}
                            .restart-btn {{
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white;
                                border: none;
                                padding: 12px 30px;
                                font-size: 18px;
                                border-radius: 25px;
                                cursor: pointer;
                                margin-top: 20px;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                                transition: transform 0.2s;
                            }}
                            .restart-btn:hover {{
                                transform: translateY(-2px);
                                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
                            }}
                            .player-info {{
                                display: flex;
                                justify-content: space-around;
                                margin-bottom: 20px;
                            }}
                            .player {{
                                font-size: 18px;
                                padding: 10px 20px;
                                border-radius: 10px;
                                background: #f8f9fa;
                            }}
                            .player.active {{
                                background: #667eea;
                                color: white;
                                font-weight: bold;
                            }}
                        </style>
                    </head>
                    <body>
                    <!-- Game instance: {tictactoe_key} -->
                    
                    <div class="game-container">
                        <h2 style="color: #667eea; margin-bottom: 20px;">Tic-Tac-Toe vs Computer</h2>
                        
                        <div class="player-info">
                            <div class="player active" id="playerX">You (X)</div>
                            <div class="player" id="playerO">Computer (O)</div>
                        </div>
                        
                        <div class="status" id="status">Your Turn</div>
                        
                        <div class="board" id="board">
                            <div class="cell" data-index="0"></div>
                            <div class="cell" data-index="1"></div>
                            <div class="cell" data-index="2"></div>
                            <div class="cell" data-index="3"></div>
                            <div class="cell" data-index="4"></div>
                            <div class="cell" data-index="5"></div>
                            <div class="cell" data-index="6"></div>
                            <div class="cell" data-index="7"></div>
                            <div class="cell" data-index="8"></div>
                        </div>
                        
                        <button class="restart-btn" onclick="restartGame()">Restart Game</button>
                    </div>

                    <script>
                    let board = ['', '', '', '', '', '', '', '', ''];
                    let humanPlayer = 'X';
                    let aiPlayer = 'O';
                    let gameActive = true;

                    const winningConditions = [
                        [0, 1, 2],
                        [3, 4, 5],
                        [6, 7, 8],
                        [0, 3, 6],
                        [1, 4, 7],
                        [2, 5, 8],
                        [0, 4, 8],
                        [2, 4, 6]
                    ];

                    const cells = document.querySelectorAll('.cell');
                    const statusDisplay = document.getElementById('status');
                    const playerXDisplay = document.getElementById('playerX');
                    const playerODisplay = document.getElementById('playerO');

                    cells.forEach(cell => {{
                        cell.addEventListener('click', handleCellClick);
                    }});

                    function handleCellClick(event) {{
                        const clickedCell = event.target;
                        const clickedCellIndex = parseInt(clickedCell.getAttribute('data-index'));

                        if (board[clickedCellIndex] !== '' || !gameActive) {{
                            return;
                        }}

                        // Human move
                        makeMove(clickedCellIndex, humanPlayer);
                        
                        if (!checkWinner(humanPlayer) && !checkTie() && gameActive) {{
                            // Computer's turn
                            statusDisplay.textContent = "Computer's Turn...";
                            playerXDisplay.classList.remove('active');
                            playerODisplay.classList.add('active');
                            
                            setTimeout(() => {{
                                const aiMove = getBestMove();
                                makeMove(aiMove, aiPlayer);
                                
                                if (!checkWinner(aiPlayer) && !checkTie()) {{
                                    statusDisplay.textContent = "Your Turn";
                                    playerODisplay.classList.remove('active');
                                    playerXDisplay.classList.add('active');
                                }}
                            }}, 500);
                        }}
                    }}

                    function makeMove(index, player) {{
                        board[index] = player;
                        cells[index].textContent = player;
                        cells[index].classList.add(player.toLowerCase());
                    }}

                    function getBestMove() {{
                        // AI Strategy:
                        // 1. Try to win
                        let move = findWinningMove(aiPlayer);
                        if (move !== -1) return move;
                        
                        // 2. Block player from winning
                        move = findWinningMove(humanPlayer);
                        if (move !== -1) return move;
                        
                        // 3. Take center if available
                        if (board[4] === '') return 4;
                        
                        // 4. Take a corner
                        const corners = [0, 2, 6, 8];
                        const availableCorners = corners.filter(i => board[i] === '');
                        if (availableCorners.length > 0) {{
                            return availableCorners[Math.floor(Math.random() * availableCorners.length)];
                        }}
                        
                        // 5. Take any available space
                        const availableSpaces = board.map((val, idx) => val === '' ? idx : null).filter(val => val !== null);
                        return availableSpaces[Math.floor(Math.random() * availableSpaces.length)];
                    }}

                    function findWinningMove(player) {{
                        for (let i = 0; i < winningConditions.length; i++) {{
                            const [a, b, c] = winningConditions[i];
                            if (board[a] === player && board[b] === player && board[c] === '') return c;
                            if (board[a] === player && board[c] === player && board[b] === '') return b;
                            if (board[b] === player && board[c] === player && board[a] === '') return a;
                        }}
                        return -1;
                    }}

                    function checkWinner(player) {{
                        let roundWon = false;
                        let winningCombination = [];

                        for (let i = 0; i < winningConditions.length; i++) {{
                            const [a, b, c] = winningConditions[i];
                            if (board[a] === '' || board[b] === '' || board[c] === '') {{
                                continue;
                            }}
                            if (board[a] === board[b] && board[b] === board[c]) {{
                                roundWon = true;
                                winningCombination = [a, b, c];
                                break;
                            }}
                        }}

                        if (roundWon) {{
                            if (player === humanPlayer) {{
                                statusDisplay.textContent = "You Win! 🎉";
                            }} else {{
                                statusDisplay.textContent = "Computer Wins! 🤖";
                            }}
                            winningCombination.forEach(index => {{
                                cells[index].classList.add('winner');
                            }});
                            gameActive = false;
                            return true;
                        }}
                        return false;
                    }}

                    function checkTie() {{
                        const roundDraw = !board.includes('');
                        if (roundDraw) {{
                            statusDisplay.textContent = "It's a Tie! 🤝";
                            gameActive = false;
                            return true;
                        }}
                        return false;
                    }}

                    function restartGame() {{
                        board = ['', '', '', '', '', '', '', '', ''];
                        gameActive = true;
                        statusDisplay.textContent = "Your Turn";
                        
                        playerXDisplay.classList.add('active');
                        playerODisplay.classList.remove('active');
                        
                        cells.forEach(cell => {{
                            cell.textContent = '';
                            cell.classList.remove('x', 'o', 'winner');
                        }});
                    }}
                    </script>

                    </body>
                    </html>
                    """
                    
                    components.html(tictactoe_html, height=770, scrolling=False)
                    
        elif level == "Moderate":
            # Local video file path
            video_path = VIDEO_PATH

            if os.path.exists(video_path):
                # Create two equal columns for side-by-side layout
                col_left, col_right = st.columns([1.5, 0.9])

                with col_left:
                    # Messages stacked on the left
                    st.markdown("""
                    <div style="
                        background-color: #FFF9C4;
                        border-left: 4px solid #FBC02D;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 15px;
                        height: auto;
                ">
                    <h4 style="margin-top: 0; color: #F57C00; font-weight: 700;">A MESSAGE FOR YOU</h4>
                    <p style="line-height: 1.8; color: #424242; margin-bottom: 0; font-size: 0.95rem;">
                    You're going through a challenging time, and that's okay. 
                    <b>Your feelings are valid</b>, and seeking support is a sign of strength, not weakness.
                    </p>
                    <p style="line-height: 1.8; color: #424242; margin-bottom: 0; font-size: 0.95rem; margin-top: 15px;">
                    Remember, taking care of your mental health is just as important as your physical health. 
                    <b>You don't have to face this alone</b>. Reach out to friends, family, or trusted people in your life 
                    who can provide the support you need.
                    </p>
                    <p style="line-height: 1.8; color: #424242; margin-bottom: 0; font-size: 0.95rem; margin-top: 15px;">
                    Small steps matter. Whether it's talking to someone you trust, practicing self-care, or trying new 
                    coping strategies, <b>every step forward counts</b>. You have the strength within you to navigate 
                    through this.
                    </p>
                    <p style="line-height: 1.8; color: #424242; margin-bottom: 0; font-size: 0.95rem; margin-top: 15px;">
                    It's important to recognize that healing isn't linear. <b>Some days will be harder than others</b>, 
                    and that's completely normal. Be patient with yourself as you work through these challenges. 
                    Progress might feel slow, but each moment of self-awareness and self-compassion is valuable.
                    <p style="line-height: 1.8; color: #424242; margin-bottom: 0; font-size: 0.95rem; margin-top: 15px;">
                    Remember to celebrate small victories along the way. <b>You're doing better than you think</b>, and 
                    taking time to acknowledge your efforts can make a real difference in how you feel each day.
                    </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                    <div style="
                        background-color: #F3E5F5;
                        border-left: 4px solid #9C27B0;
                        padding: 20px;
                        border-radius: 8px;
                        text-align: center;
                        height: auto;
                    ">
                        <p style="
                            font-size: 1.05rem;
                            font-weight: 700;
                            color: #424242;
                            margin: 0;
                            line-height: 1.0;
                        ">
                        "Your feelings matter. You matter."
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_right:
                    # Smaller video on the right
                    st.video(video_path)
            else:
                st.error("Video file not found. Please check the file path.")
                st.info(f"Expected path: {video_path}")

        # ------- SEVERE: MENTAL HEALTH RESOURCES -------
        else:  # Severe
            st.markdown("#### 🆘 Get Professional Support")
            st.markdown("It's important to reach out for help. Here are trusted resources:")
            
            st.markdown(
                """
                <div style="
                    border: 2px solid #3b82f6;
                    border-radius: 12px;
                    padding: 20px;
                    background-color: #eff6ff;
                    margin: 20px 0;
                ">
                    <h4 style="margin-top: 0; color: #1e40af;">
                        MALAYSIAN NATIONAL MENTAL HEALTH RESOURCES
                    </h4>
                    <ul style="line-height: 1.8; color: #1e293b;">
                        <li><strong>Befrienders KL:</strong> 03-7627 2929 (24/7 helpline)</li>
                        <li><strong>MIASA (Malaysian Mental Health Association):</strong> 03-7782 5499</li>
                        <li><strong>Talian Kasih:</strong> 15999 (Counseling hotline)</li>
                        <li><strong>Mental Health Psychosocial Support Service (MHPSS):</strong><br>
                            03-2935 9935 (Mon-Fri, 9 AM-5 PM)</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown(
                """
                <div style="
                    border: 3px solid #dc2626;
                    border-radius: 12px;
                    padding: 20px;
                    background-color: #fef2f2;
                    margin: 20px 0;
                ">
                    <h4 style="margin-top: 0; color: #991b1b;">
                        🚨 EMERGENCY SUPPORT
                    </h4>
                    <p style="color: #1e293b; line-height: 1.8;">
                        <strong>If you're having thoughts of self-harm or suicide:</strong>
                    </p>
                    <ul style="line-height: 1.8; color: #1e293b;">
                        <li>🚨 <strong>Call 999</strong> (Malaysia Emergency Services)</li>
                        <li>🚨 <strong>Go to nearest hospital Emergency Department</strong></li>
                        <li>🚨 <strong>Call Befrienders:</strong> 03-7627 2929 (Available 24/7)</li>
                    </ul>
                    <p style="
                        text-align: center;
                        font-weight: 700;
                        font-size: 1.1em;
                        color: #991b1b;
                        margin-bottom: 0;
                        margin-top: 15px;
                    ">
                        YOU ARE NOT ALONE. HELP IS AVAILABLE.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )