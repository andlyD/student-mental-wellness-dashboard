# who_we_are.py
# 👥 TAB 1: WHO WE ARE (Descriptive Analytics · Magazine Layout)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_lottie import st_lottie
from pathlib import Path

from components.home_lottie import lottie_doctor


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "assets" / "data" / "Cleaned_Form_Responses.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def run_who_we_are_tab():
    df = load_data()

    # ---------- UNIVERSAL INSIGHT TEXT (simple, no coloured box) ----------
    def insight_box(text: str):
        st.markdown(
            f"""
<div style="margin-top:0.4rem; font-size:0.9rem; line-height:1.55; color:#111827;">
  <span style="font-size:1.05rem; margin-right:3px;">💡</span>
  <strong style="color:#0F1E53;">Insight:</strong> {text}
</div>
""",
            unsafe_allow_html=True,
        )

    # -------------------------------------------------------------------
    # GLOBAL STYLING – MONTSERRAT + MAGAZINE FEEL + CARD SHADOW
    # -------------------------------------------------------------------
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');

/* =========================================================
   GLOBAL FONT + BACKGROUND
   ========================================================= */
html, body, [class*="css"], .stMarkdown, .stText, .stButton, .stSelectbox, .stPlotlyChart {
    font-family: 'Montserrat', sans-serif !important;
}

/* Keseluruhan app putih bersih */
.stApp {
    background:#ffffff !important;
    color:#111827;
}
div[data-testid="stAppViewContainer"],
div[data-testid="stAppViewContainer"] > .main {
    background-color:#ffffff !important;
}
div[data-testid="stAppViewContainer"] > .main {
    padding-left:3.2rem;
    padding-right:3.2rem;
    padding-top:1.2rem;
}

/* =========================================================
   HERO SECTION
   ========================================================= */
.mag-hero-wrap {
    display:flex;
    justify-content:center;
    margin-top:0.4rem;
    margin-bottom:1.2rem;
}
.mag-hero {
    max-width:1050px;
    width:100%;
    background:linear-gradient(135deg,#0F1E53,#1B2A6D,#26408B);
    border-radius:26px;
    padding:1.9rem 2.7rem 2.0rem 2.7rem;
    box-shadow:0 22px 55px rgba(15,23,42,0.55);
    color:#f9fafb;
    position:relative;
    overflow:hidden;
}
.mag-hero-orb {
    position:absolute;
    width:180px;height:180px;
    border-radius:999px;
    background:radial-gradient(circle at 30% 30%,#fbbf24,transparent);
    right:-50px;top:-40px;
    filter:blur(8px);
    opacity:0.7;
}
.mag-hero-kicker {
    font-size:0.78rem;
    letter-spacing:0.26em;
    text-transform:uppercase;
    opacity:0.9;
    margin-bottom:0.35rem;
}
.mag-hero-title {
    font-size:1.9rem;
    font-weight:800;
    letter-spacing:0.12em;
    text-transform:uppercase;
    margin-bottom:0.25rem;
}
.mag-hero-sub {
    font-size:0.96rem;
    font-weight:400;
    opacity:0.97;
}
.mag-hero-tag {
    position:absolute;
    right:1.8rem;
    bottom:1.2rem;
    font-size:0.78rem;
    text-transform:uppercase;
    letter-spacing:0.2em;
    padding:0.28rem 1rem;
    border-radius:999px;
    border:1px solid rgba(249,250,251,0.7);
    background:linear-gradient(135deg,rgba(15,23,42,0.08),rgba(15,23,42,0.35));
}

/* =========================================================
   SECTION HEADINGS + CHIPS
   ========================================================= */
.mag-intro {
    max-width:1050px;
    margin:0 auto 0.8rem auto;
    font-size:0.92rem;
    line-height:1.6;
    color:#111827;
}
.mag-chips {
    max-width:1050px;
    margin:0.2rem auto 1.0rem auto;
    display:flex;
    gap:0.6rem;
    flex-wrap:wrap;
}
.mag-chip {
    padding:0.35rem 0.9rem;
    border-radius:999px;
    font-size:0.8rem;
    font-weight:600;
    background:rgba(15,23,42,0.06);
    color:#374151;
}
.mag-section-heading {
    max-width:1050px;
    margin:1.5rem auto 0.2rem auto;
    font-size:0.78rem;
    text-transform:uppercase;
    letter-spacing:0.26em;
    color:#6b7280;
}
.mag-divider {
    max-width:1050px;
    margin:0 auto 0.9rem auto;
    height:1px;
    background:linear-gradient(90deg,
        rgba(156,163,175,0.1),
        rgba(17,24,39,0.7),
        rgba(156,163,175,0.1));
}

/* =========================================================
   MAIN CARDS – st.container(border=True)
   ========================================================= */
div[data-testid="stVerticalBlockBorderWrapper"] {
    max-width:1050px;
    margin:0 auto 1.4rem auto;
    background:#ffffff !important;
    border-radius:24px !important;
    border:none !important;
    padding:24px 26px !important;
    box-shadow:
        0 24px 60px rgba(15,23,42,0.12),
        0 10px 25px rgba(15,23,42,0.08) !important;
    transition:transform 0.22s ease-out, box-shadow 0.22s ease-out;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform:translateY(-2px);
    box-shadow:
        0 28px 70px rgba(15,23,42,0.16),
        0 12px 30px rgba(15,23,42,0.10) !important;
}

/* =========================================================
   PREMIUM BOX UNTUK TEKS DALAM DROPDOWN
   ========================================================= */
div[data-testid="stExpander"] .card-text-small {
    background:#E7F3FF !important;
    border-radius:10px !important;
    padding:0.85rem 1.0rem 0.95rem 1.0rem !important;
    border:1px solid #D3E6FF !important;
    box-shadow:0 4px 12px rgba(15,23,42,0.08) !important;
    font-size:0.88rem !important;
    line-height:1.6 !important;
    color:#0A1A33 !important;
}
div[data-testid="stExpander"] .card-text-small b {
    color:#0F1E53 !important;
    font-weight:700 !important;
}

/* =========================================================
   TEXT STYLE DALAM CARD
   ========================================================= */
.card-label {
    font-size:0.7rem;
    text-transform:uppercase;
    letter-spacing:0.26em;
    color:#9ca3af;
    margin-bottom:0.15rem;
}
.card-title-main {
    font-size:1.02rem;
    font-weight:800;
    letter-spacing:0.08em;
    text-transform:uppercase;
    margin-bottom:0.6rem;
    color:#111827;
}
.card-text {
    font-size:0.88rem;
    line-height:1.6;
    color:#374151;
}
.card-text-small {
    font-size:0.82rem;
    line-height:1.5;
    color:#4b5563;
}

/* =========================================================
   BOTTOM CTA PILL
   ========================================================= */
.mag-next-pill {
    max-width:1050px;
    margin:1.4rem auto 0 auto;
    text-align:center;
}
.mag-next-pill span {
    padding:0.6rem 1.6rem;
    border-radius:999px;
    border:1px solid #6366F1;
    background:rgba(129,140,248,0.08);
    font-weight:600;
    font-size:0.92rem;
}
</style>
""",
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------
    # HERO
    # -------------------------------------------------------------------
    st.markdown(
        """
        <div class="mag-hero">
          <div class="mag-hero-orb"></div>

          <p class="mag-hero-kicker">
            STUDENT MENTAL WELLNESS • TAB 1
          </p>

          <h1 class="mag-hero-title">
            WHO WE ARE
          </h1>

          <p class="mag-hero-sub" style="max-width:720px;">
            A descriptive snapshot of the students who took part in this mental wellness study.
          </p>

          <p style="
              font-size:0.95rem;
              max-width:780px;
              line-height:1.6;
              opacity:0.92;
              margin:0 0 0.7rem 0;
          ">
            Think of this page as a magazine profile of our respondents.
            You will see who joined this study by age, gender, level of study,
            programme and current mental wellness status.
          </p>

          <p style="
              font-size:0.9rem;
              font-weight:500;
              letter-spacing:0.02em;
              opacity:0.96;
              margin:0;
          ">
            📊 Descriptive analytics · 🧠 Mental wellness awareness · 🎓 Student focused
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ===================================================================
    # SECTION I – STUDENT SNAPSHOT
    # ===================================================================
    st.markdown(
        '<div class="mag-section-heading">SECTION I · STUDENT SNAPSHOT</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mag-divider"></div>', unsafe_allow_html=True)

    # --------------------------- ROW 1: AGE -----------------------------
    with st.container(border=True):
        top_col1, top_col2 = st.columns([1.35, 1])

        # --- Left: Chart ---
        with top_col1:
            st.markdown(
                "<div class='card-label'>01 · AGE PROFILE</div>"
                "<div class='card-title-main'>📈 Age distribution</div>",
                unsafe_allow_html=True,
            )

            age_counts = df["Age"].value_counts().sort_index()

            colors = [
                "#FF6B9D",
                "#C44569",
                "#FFA07A",
                "#FFD93D",
                "#6BCB77",
                "#4D96FF",
                "#9D84B7",
                "#FF5722",
                "#00BCD4",
                "#E91E63",
            ]
            bar_colors = [colors[i % len(colors)] for i in range(len(age_counts))]

            fig_age = go.Figure()
            fig_age.add_trace(
                go.Bar(
                    x=age_counts.index,
                    y=age_counts.values,
                    marker=dict(
                        color=bar_colors,
                        line=dict(color="white", width=2),
                    ),
                    text=age_counts.values,
                    textposition="outside",
                    textfont=dict(size=13, color="#2C3E50", family="Arial Black"),
                    hovertemplate="<b>Age: %{x}</b><br>Students: %{y}<extra></extra>",
                    name="",
                )
            )
            fig_age.add_trace(
                go.Scatter(
                    x=age_counts.index,
                    y=age_counts.values,
                    mode="lines",
                    line=dict(color="rgba(255, 0, 0, 0.5)", width=3, dash="dash"),
                    hoverinfo="skip",
                    name="",
                )
            )

            fig_age.update_layout(
                height=260,
                margin=dict(l=10, r=10, t=10, b=10),
                plot_bgcolor="white",
                paper_bgcolor="white",
                showlegend=False,
            )

            st.plotly_chart(fig_age, use_container_width=True)

        # --- Right: Text + Expander ---
        with top_col2:
            age_counts_right = df["Age"].value_counts().sort_index()
            peak_age = age_counts_right.idxmax()

            insight_box(
                f"Most respondents are between 19 and 21 years old, "
                f"and the largest group is age {peak_age}. "
                "This is a period where many students are managing academic demands, "
                "friendships and early career decisions at the same time."
            )

            with st.expander("🔎 What does this chart show?"):
                st.markdown(
                    """
<div class="card-text-small">
<b>Type of EDA:</b> Bar chart with a trend line.  

<b>Purpose:</b> To show how many students fall into each age group and which ages dominate the sample.

<b>How to read:</b>  
Each bar represents one age. A taller bar means more students at that age.  
The line on top helps you follow how the numbers rise and fall across the age range.
</div>
""",
                    unsafe_allow_html=True,
                )

    # --------------------------- ROW 2: GENDER + STUDY ------------------
    row2 = st.container()
    with row2:
        col_left, col_right = st.columns([1, 1])

        # ---- GENDER CARD ----
        with col_left:
            with st.container(border=True):
                st.markdown(
                    "<div class='card-label'>02 · GENDER MIX</div>"
                    "<div class='card-title-main'>⚧ Gender breakdown</div>",
                    unsafe_allow_html=True,
                )

                gender_map = {1: "Female", 2: "Male"}
                df["Gender_Label"] = df["Gender"].map(gender_map)
                gender_counts = df["Gender_Label"].value_counts()

                fig_gender = go.Figure(
                    data=[
                        go.Pie(
                            labels=gender_counts.index,
                            values=gender_counts.values,
                            hole=0.45,
                            marker=dict(colors=["deeppink", "dodgerblue"]),
                            textinfo="percent",
                        )
                    ]
                )
                fig_gender.update_layout(
                    height=272,
                    margin=dict(l=5, r=5, t=5, b=5),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.1,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=11),
                    ),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                )

                st.plotly_chart(fig_gender, use_container_width=True)

                total_gender = int(gender_counts.sum())
                female_pct = gender_counts.get("Female", 0) / total_gender * 100
                male_pct = gender_counts.get("Male", 0) / total_gender * 100

                insight_box(
                    f"Women make up about {female_pct:.1f}% of the sample "
                    f"and men about {male_pct:.1f}%. "
                    "The dataset therefore reflects perspectives from both genders in a fairly balanced way."
                )

                with st.expander("🔎 What does this chart show?"):
                    st.markdown(
                        """
<div class="card-text-small">
<b>Type of EDA:</b> Donut chart.  

<b>Purpose:</b> To visualise the proportion of students by gender.

<b>How to read:</b>  
Each coloured slice represents one gender.  
The size and percentage label show how many students come from that group.
</div>
""",
                        unsafe_allow_html=True,
                    )

        # ---- STUDY LEVEL CARD ----
        with col_right:
            with st.container(border=True):
                st.markdown(
                    "<div class='card-label'>03 · STUDY STAGE</div>"
                    "<div class='card-title-main'>🎓 Level of study</div>",
                    unsafe_allow_html=True,
                )

                study_level_mapping = {1: "Degree", 2: "Diploma", 3: "Foundation"}
                df["Study_Level_Label"] = df["Current_Level_of_Studies"].map(
                    study_level_mapping
                )

                study_counts = (
                    df["Study_Level_Label"].value_counts().sort_values(ascending=True)
                )
                study_pct = (study_counts / len(df) * 100).round(1)

                colors_mapping = {
                    "Degree": "mediumorchid",
                    "Diploma": "royalblue",
                    "Foundation": "lime",
                }

                fig_study = go.Figure()

                for level, count in study_counts.items():
                    pct = study_pct[level]
                    fig_study.add_trace(
                        go.Bar(
                            y=[level],
                            x=[count],
                            orientation="h",
                            marker=dict(
                                color=colors_mapping[level],
                                line=dict(color="white", width=3),
                            ),
                            text=f"{count} ({pct}%)",
                            textposition="outside",
                            textfont=dict(
                                size=14, color="#1A237E", family="Arial Black"
                            ),
                            hovertemplate=(
                                f"<b>{level}</b><br>"
                                f"Students: {count}<br>"
                                f"Percentage: {pct}%<extra></extra>"
                            ),
                            width=0.55,
                        )
                    )

                max_value = study_counts.max()

                fig_study.update_layout(
                    title_text="",
                    height=250,
                    margin=dict(l=80, r=150, t=10, b=10),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    showlegend=False,
                )

                fig_study.update_xaxes(
                    range=[0, max_value * 1.6],
                    showgrid=True,
                    gridcolor="rgba(150,150,150,0.2)",
                )

                st.plotly_chart(fig_study, use_container_width=True)

                degree_pct = study_pct.get("Degree", 0.0)

                insight_box(
                    f"More than half of the respondents are Degree students "
                    f"(about {degree_pct:.1f}%). "
                    "This group is usually dealing with heavier coursework, final year projects "
                    "and preparation for internships, which can place extra pressure on their wellbeing."
                )

                with st.expander("🔎 What does this chart show?"):
                    st.markdown(
                        """
<div class="card-text-small">
<b>Type of EDA:</b> Horizontal bar chart.  

<b>Purpose:</b> To compare how many students are at Foundation, Diploma and Degree level.

<b>How to read:</b>  
Each bar shows one level of study.  
The length of the bar and the label at the end indicate the number and percentage of students in that group.
</div>
""",
                        unsafe_allow_html=True,
                    )

    # -------------------------------------------------------------------
    # LOTTIE BREAK
    # -------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        st.markdown(
            """
            <div style="text-align:center; margin-bottom:0.6rem;">
              <p style="
                    font-size:1.15rem;
                    font-weight:700;
                    color:#1a237e;
                    margin:0 0 0.25rem 0;">
                It is quite interesting to see who is behind these numbers, right?
              </p>
              <p style="
                    font-size:0.9rem;
                    color:#4b5563;
                    margin:0;">
                You have just met the students who shaped this mental wellness story.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        left, center, right = st.columns([1, 1.4, 1])
        with center:
            if lottie_doctor:
                st_lottie(
                    lottie_doctor,
                    height=260,
                    key="mental_health_break_tab1",
                    loop=True,
                    quality="high",
                    speed=1,
                )
            else:
                st.info("Lottie animation could not be loaded.")

        st.markdown(
            """
            <div style="text-align:center; margin-top:0.6rem;">
              <p style="
                    font-size:0.95rem;
                    font-weight:600;
                    color:#1a237e;
                    margin:0;">
                Next, let us explore how their programmes and wellness levels connect to one another.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ===================================================================
    # SECTION II – FIELD OF STUDY
    # ===================================================================
    st.markdown(
        '<div class="mag-section-heading">SECTION II · FIELD OF STUDY</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mag-divider"></div>', unsafe_allow_html=True)

    with st.container(border=True):
        f_col1, f_col2 = st.columns([1.35, 1])

        # ------------------ LEFT: FIELD OF STUDY CHART ------------------
        with f_col1:
            st.markdown(
                "<div class='card-label'>04 · PROGRAMME MIX</div>"
                "<div class='card-title-main'>📚 Field of study</div>",
                unsafe_allow_html=True,
            )

            field_mapping = {
                1: "Arts and Humanities",
                2: "Business",
                3: "Health Sciences",
                4: "STEM",
                5: "Social Sciences",
            }
            df["Field_Label"] = df["Field_of_Study"].map(field_mapping)

            field_counts = df["Field_Label"].value_counts().sort_values(ascending=True)
            field_pct = (field_counts / len(df) * 100).round(1)

            field_colors = {
                "Arts and Humanities": "gold",
                "Business": "deeppink",
                "Health Sciences": "limegreen",
                "STEM": "dodgerblue",
                "Social Sciences": "red",
            }

            fig_field = go.Figure()

            for field, count in field_counts.items():
                pct = field_pct[field]
                color = field_colors[field]

                fig_field.add_trace(
                    go.Bar(
                        y=[field],
                        x=[count],
                        orientation="h",
                        name=field,
                        marker=dict(
                            color=color,
                            line=dict(color="white", width=3),
                            opacity=0.9,
                        ),
                        text=f"{count} ({pct}%)",
                        textposition="outside",
                        textfont=dict(
                            size=14, color="#1A237E", family="Arial Black"
                        ),
                        hovertemplate=(
                            f"<b>{field}</b><br>"
                            f"Students: {count}<br>"
                            f"Percentage: {pct}%<extra></extra>"
                        ),
                        width=0.7,
                    )
                )

            max_field_value = field_counts.max()

            fig_field.update_layout(
                title=dict(text=""),
                xaxis=dict(
                    title=dict(
                        text="<b>Number of Students</b>",
                        font=dict(size=14, color="#1A237E", family="Arial Black"),
                    ),
                    showgrid=True,
                    gridcolor="rgba(150,150,150,0.2)",
                    tickfont=dict(size=11, color="#2C3E50"),
                ),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=12, color="#1A237E", family="Arial Black"),
                    showgrid=False,
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                showlegend=False,
                height=360,
                margin=dict(l=140, r=190, t=10, b=40),
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=13,
                    font_family="Arial",
                    bordercolor="#1A237E",
                ),
            )

            fig_field.update_xaxes(range=[0, max_field_value * 2.0])

            st.plotly_chart(fig_field, use_container_width=True)

        # ------------------ RIGHT: TEXT EXPLANATION ---------------------
        with f_col2:
            stem_pct = field_pct.get("STEM", 0.0)

            insight_box(
                f"The largest group of respondents comes from STEM programmes "
                f"(about {stem_pct:.1f}%), followed by Business, Health Sciences, "
                "Social Sciences and Arts and Humanities. "
                "Each field brings its own academic load, such as laboratories, fieldwork, reports "
                "and group projects, which can influence how students experience stress and wellness."
            )

            with st.expander("🔎 What does this chart show?"):
                st.markdown(
                    """
<div class="card-text-small">
<b>Type of EDA:</b> Horizontal bar chart across programmes.  

<b>Purpose:</b> To show which academic fields contribute the most students to this study.

<b>How to read:</b>  
Each bar represents one field of study.  
Longer bars and larger labels indicate fields with more students in the sample.
</div>
""",
                    unsafe_allow_html=True,
                )

    # ===================================================================
    # SECTION III – MENTAL WELLNESS STATUS + WAFFLE
    # ===================================================================
    st.markdown(
        '<div class="mag-section-heading">SECTION III · MENTAL WELLNESS STATUS</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mag-divider"></div>', unsafe_allow_html=True)

    row4 = st.container()
    with row4:
        col_left4, col_right4 = st.columns([1, 1])

        # ---- WELLNESS STATUS CARD ----
        with col_left4:
            with st.container(border=True):
                st.markdown(
                    "<div class='card-label'>05 · REALITY CHECK</div>"
                    "<div class='card-title-main'>🧠 Overall wellness levels</div>",
                    unsafe_allow_html=True,
                )

                wellness_mapping = {
                    1: "Minimal and Mild",
                    2: "Moderate",
                    3: "Severe",
                }
                df["Wellness_Label"] = df["Depressed_Anxious"].map(wellness_mapping)

                wellness_order = ["Minimal and Mild", "Moderate", "Severe"]
                wellness_counts = (
                    df["Wellness_Label"].value_counts().reindex(wellness_order)
                )
                wellness_pct = (wellness_counts / len(df) * 100).round(1)

                colors_well = ["limegreen", "darkorange", "crimson"]

                fig_well = go.Figure(
                    data=[
                        go.Pie(
                            labels=wellness_counts.index,
                            values=wellness_counts.values,
                            hole=0.6,
                            marker=dict(
                                colors=colors_well,
                                line=dict(color="white", width=4),
                            ),
                            textinfo="percent",
                            textfont=dict(
                                size=18, color="white", family="Arial Black"
                            ),
                            pull=[0.05, 0.1, 0.15],
                            hovertemplate="<b>%{label}</b><br>"
                            "<b>Students:</b> %{value}<br>"
                            "<b>Percentage:</b> %{percent}<extra></extra>",
                            rotation=90,
                            direction="clockwise",
                            showlegend=True,
                        )
                    ]
                )

                fig_well.add_annotation(
                    text=f"<b>{len(df)}</b><br>"
                    "<span style='font-size:16px'>Students Surveyed</span>",
                    x=0.5,
                    y=0.5,
                    font=dict(size=30, color="#1A237E", family="Arial Black"),
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                )

                fig_well.update_layout(
                    title=dict(
                        text="<b>Mental Wellness Status</b>",
                        x=0.5,
                        xanchor="center",
                        font=dict(size=20, color="#1A237E", family="Arial Black"),
                    ),
                    paper_bgcolor="white",
                    plot_bgcolor="white",
                    height=627,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.05,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=11),
                    ),
                    hoverlabel=dict(
                        bgcolor="white",
                        font_size=14,
                        font_family="Arial",
                        bordercolor="#1A237E",
                    ),
                    margin=dict(t=60, b=40, l=20, r=20),
                )

                st.plotly_chart(fig_well, use_container_width=True)

                minimal_mild = int(wellness_counts.get("Minimal and Mild", 0))
                moderate = int(wellness_counts.get("Moderate", 0))
                severe = int(wellness_counts.get("Severe", 0))
                total = int(wellness_counts.sum())
                moderate_severe = moderate + severe
                ms_pct = (moderate_severe / total * 100) if total > 0 else 0

                insight_box(
                    f"Out of all respondents, {minimal_mild} students fall in the Minimal and Mild range, "
                    f"{moderate} in the Moderate range and {severe} in the Severe range. "
                    f"In total, almost {ms_pct:.0f}% of students, which is roughly one in three, "
                    "report moderate to severe symptoms."
                )

                with st.expander("🔎 What does this chart show?"):
                    st.markdown(
                        """
<div class="card-text-small">
<b>Type of EDA:</b> Donut chart.  

<b>Purpose:</b> To provide a quick overview of how serious the wellness situation is in this sample.

<b>How to read:</b>  
Each ring segment represents one severity level.  
Larger coloured segments indicate more students in that category.
</div>
""",
                        unsafe_allow_html=True,
                    )

        # ---- WAFFLE BY GENDER CARD ----
        with col_right4:
            with st.container(border=True):
                st.markdown(
                    "<div class='card-label'>06 · WHO IS MOST AFFECTED?</div>"
                    "<div class='card-title-main'>🕵️‍♀️ Waffle chart by gender</div>",
                    unsafe_allow_html=True,
                )

                # ====== PREP DATA ======
                gender_mapping = {1: "Female", 2: "Male"}
                wellness_mapping = {
                    1: "Minimal and Mild",
                    2: "Moderate",
                    3: "Severe",
                }

                df["Gender_Label"] = df["Gender"].map(gender_mapping)
                df["Wellness_Label"] = df["Depressed_Anxious"].map(wellness_mapping)

                female_data = (
                    df[df["Gender_Label"] == "Female"]["Wellness_Label"].value_counts()
                )
                male_data = (
                    df[df["Gender_Label"] == "Male"]["Wellness_Label"].value_counts()
                )

                female_total = int(female_data.sum())
                male_total = int(male_data.sum())

                # ambil count ikut kategori, kalau tak wujud jadikan 0
                female_severe = int(female_data.get("Severe", 0))
                female_moderate = int(female_data.get("Moderate", 0))
                female_minimal = int(female_data.get("Minimal and Mild", 0))

                male_severe = int(male_data.get("Severe", 0))
                male_moderate = int(male_data.get("Moderate", 0))
                male_minimal = int(male_data.get("Minimal and Mild", 0))

                colors_waffle = {
                    "Minimal and Mild": "limegreen",
                    "Moderate": "darkorange",
                    "Severe": "crimson",
                }

                # ====== HELPER FUNCTIONS ======
                def create_waffle_data(data_series, grid_cols=10):
                    """
                    Susunkan kotak ikut urutan:
                    baris atas = Severe, tengah = Moderate, bawah = Minimal and Mild.
                    """
                    order = ["Severe", "Moderate", "Minimal and Mild"]
                    squares = []
                    current_row = 0

                    for level in order:
                        count = data_series.get(level, 0)
                        if count > 0:
                            squares.extend([level] * count)
                            rows_for_level = int(np.ceil(count / grid_cols))
                            current_row += rows_for_level

                    total_local = data_series.sum()
                    grid_rows = int(np.ceil(total_local / grid_cols))

                    # penuhkan grid dengan "Empty" supaya bentuk grid cun
                    while len(squares) < grid_rows * grid_cols:
                        squares.append("Empty")

                    return squares, grid_rows, grid_cols

                def create_waffle_shapes(squares, grid_rows, grid_cols, colors_map):
                    shapes = []
                    idx = 0
                    for row in range(grid_rows):
                        for col in range(grid_cols):
                            if idx < len(squares):
                                level = squares[idx]
                                color = colors_map.get(level, "#EEEEEE")
                                shapes.append(
                                    dict(
                                        type="rect",
                                        x0=col,
                                        x1=col + 0.9,
                                        y0=grid_rows - row - 1,
                                        y1=grid_rows - row - 0.1,
                                        fillcolor=color,
                                        line=dict(color="white", width=3),
                                    )
                                )
                                idx += 1
                    return shapes

                # ====== BUILD GRIDS ======
                female_squares, female_rows, female_cols = create_waffle_data(
                    female_data, grid_cols=10
                )
                male_squares, male_rows, male_cols = create_waffle_data(
                    male_data, grid_cols=10
                )

                fig_waffle = make_subplots(
                    rows=1,
                    cols=2,
                    horizontal_spacing=0.15,
                    specs=[[{"type": "xy"}, {"type": "xy"}]],
                )

                # dummy trace untuk setiap subplot
                fig_waffle.add_trace(
                    go.Scatter(
                        x=[0],
                        y=[0],
                        mode="markers",
                        marker=dict(opacity=0),
                        showlegend=False,
                    ),
                    row=1,
                    col=1,
                )
                fig_waffle.add_trace(
                    go.Scatter(
                        x=[0],
                        y=[0],
                        mode="markers",
                        marker=dict(opacity=0),
                        showlegend=False,
                    ),
                    row=1,
                    col=2,
                )

                female_shapes = create_waffle_shapes(
                    female_squares, female_rows, female_cols, colors_waffle
                )
                male_shapes = create_waffle_shapes(
                    male_squares, male_rows, male_cols, colors_waffle
                )

                for shape in female_shapes:
                    shape["xref"] = "x1"
                    shape["yref"] = "y1"
                for shape in male_shapes:
                    shape["xref"] = "x2"
                    shape["yref"] = "y2"

                # ====== LAYOUT WAFFLE ======
                fig_waffle.update_layout(
                    shapes=female_shapes + male_shapes,
                    title=dict(
                        text="<b>Mental Wellness Distribution by Gender</b>",
                        x=0.5,
                        xanchor="center",
                        font=dict(size=18, color="#1A237E", family="Arial Black"),
                    ),
                    showlegend=False,
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    height=520,
                    margin=dict(t=70, b=80, l=40, r=40),
                )

                # label "Female Students" & "Male Students" di atas grid
                fig_waffle.add_annotation(
                    x=4.5,
                    y=female_rows + 1.2,
                    text="<b>Female Students</b>",
                    showarrow=False,
                    xref="x1",
                    yref="y1",
                    xanchor="center",
                    font=dict(size=16, family="Arial Black", color="#1A237E"),
                )
                fig_waffle.add_annotation(
                    x=4.5,
                    y=male_rows + 1.2,
                    text="<b>Male Students</b>",
                    showarrow=False,
                    xref="x2",
                    yref="y2",
                    xanchor="center",
                    font=dict(size=16, family="Arial Black", color="#1A237E"),
                )

                # TOTAL di bawah setiap grid
                fig_waffle.add_annotation(
                    x=4.5,
                    y=-0.8,
                    text=f"<b>Total: {female_total} students</b>",
                    showarrow=False,
                    xref="x1",
                    yref="y1",
                    font=dict(size=14, color="#1A237E", family="Arial Black"),
                )
                fig_waffle.add_annotation(
                    x=4.5,
                    y=-0.8,
                    text=f"<b>Total: {male_total} students</b>",
                    showarrow=False,
                    xref="x2",
                    yref="y2",
                    font=dict(size=14, color="#1A237E", family="Arial Black"),
                )

                # x & y axes – kosongkan tick
                max_rows = max(female_rows, male_rows)
                for i in [1, 2]:
                    fig_waffle.update_xaxes(
                        showgrid=False,
                        showticklabels=False,
                        zeroline=False,
                        range=[-0.5, 10.5],
                        row=1,
                        col=i,
                    )
                    fig_waffle.update_yaxes(
                        showgrid=False,
                        showticklabels=False,
                        zeroline=False,
                        range=[-1.2, max_rows + 2],
                        row=1,
                        col=i,
                    )

                st.plotly_chart(fig_waffle, use_container_width=True)

                # ====== RINGKASAN BERWARNA DI BAWAH GRAF ======
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(
                        f"""
<div style="font-size:0.9rem; line-height:1.5;">
  <b>Female students</b><br>
  <span style="color:crimson;">Severe: <b>{female_severe}</b></span><br>
  <span style="color:darkorange;">Moderate: <b>{female_moderate}</b></span><br>
  <span style="color:limegreen;">Minimal &amp; Mild: <b>{female_minimal}</b></span>
</div>
""",
                        unsafe_allow_html=True,
                    )

                with c2:
                    st.markdown(
                        f"""
<div style="font-size:0.9rem; line-height:1.5;">
  <b>Male students</b><br>
  <span style="color:crimson;">Severe: <b>{male_severe}</b></span><br>
  <span style="color:darkorange;">Moderate: <b>{male_moderate}</b></span><br>
  <span style="color:limegreen;">Minimal &amp; Mild: <b>{male_minimal}</b></span>
</div>
""",
                        unsafe_allow_html=True,
                    )

                insight_box(
                    "Each coloured square in the waffle chart represents a group of students at a certain wellness level. "
                    "A larger block of orange or red squares signals that more students in that gender group are experiencing "
                    "moderate or severe symptoms."
                )

                with st.expander("🔎 What does this chart show?"):
                    st.markdown(
                        """
<div class="card-text-small">
<b>Type of EDA:</b> Waffle chart by gender.  

<b>Purpose:</b> To make it easy to see which gender has more students in each wellness category.

<b>How to read:</b>  
The grid on the left shows female students and the grid on the right shows male students.  
Green squares represent Minimal and Mild wellness, orange squares represent Moderate wellness and red squares represent Severe wellness.
</div>
""",
                        unsafe_allow_html=True,
                    )

    # -------------------------------------------------------------------
    # BOTTOM CTA
    # -------------------------------------------------------------------
    if st.button("👉 NEXT: THE UNTOLD SIDE — Discover the story behind the patterns"):
        st.session_state["go_to_untold_side"] = True
        st.rerun()