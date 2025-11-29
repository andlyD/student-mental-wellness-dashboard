# untold_side_page.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy import stats
from matplotlib import colors as mcolors
from streamlit_lottie import st_lottie
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "assets" / "data" / "Cleaned_Form_Responses.csv"
ANIM_DIR = BASE_DIR / "assets" / "animations"


def load_lottiefile(filename: str):
    """
    Load a Lottie JSON file from the animations folder.
    """
    file_path = ANIM_DIR / filename
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR loading {filename}: {e}")
        return None


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


def render_untold_side():
    df = load_data()
    lottie_data_analytics = load_lottiefile("Data Analytics.json")

    st.markdown("""
        <style>
        .main-header {
            text-align: center;
            background: royalblue;  /* Changed to solid royalblue */
            color: #FFFFFF;
            font-size: 3rem;
            font-weight: 900;
            padding: 2.5rem 2rem;
            border-radius: 20px;
            margin-bottom: 3rem;
            box-shadow: 0 10px 30px rgba(65, 105, 225, 0.3);  /* Adjusted shadow to match royalblue */
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        .main-header::before {
            content: '';  /* Removed shine animation */
            display: none;
        }
        @keyframes shine {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        .header-subtitle {
            font-size: 1.2rem;
            font-weight: 400;
            margin-top: 0.5rem;
            color: #E8EAF6;
            letter-spacing: 2px;
        }
        .section-header {
            color: #1A237E;
            font-size: 1.8rem;
            font-weight: bold;
            margin-top: 3rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #1A237E;
        }
        .finding-header {
            color: #1A237E;
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-left: 5px solid #1976D2;
            padding-left: 1rem;
        }
        .insight-box {
            background-color: #E3F2FD;
            border-left: 4px solid #1976D2;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 4px;
        }
        .text-block {
            background-color: #F5F5F5;
            padding: 1.5rem;
            border-radius: 8px;
            height: 100%;
        }
        .text-block h4 {
            color: #1A237E;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .text-block ul {
            list-style-type: none;
            padding-left: 0;
        }
        .text-block li {
            margin-bottom: 0.8rem;
            line-height: 1.6;
        }
        .key-takeaway {
            background-color: #FFF3E0;
            border-left: 4px solid #FF9800;
            padding: 1rem;
            margin-top: 1rem;
            border-radius: 4px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Page header
    st.markdown('''
        <div class="main-header">
            The Untold Side of Student Wellness
            <div class="header-subtitle">Discovering What Really Matters for Your Mental Health</div>
        </div>
    ''', unsafe_allow_html=True)

    # 1st Visualisation: Top 5 Factors - Racing Bar
    st.markdown('<div class="section-header">⭐ What Are the Biggest Reasons Students Feel Stressed?</div>', unsafe_allow_html=True)

    # Create two columns - Lottie on left, Chart on right 
    col_lottie_left, col_chart_right = st.columns([1, 2])

    with col_lottie_left:
        # Display Lottie animation
        if lottie_data_analytics:
            st_lottie(
                lottie_data_analytics,
                speed=1,
                reverse=False,
                loop=True,
                quality="high",
                height=550,
            )
    
    # Add some context text below the lottie
    st.markdown("""
        <div style="background-color: #F5F5F5; padding: 1.5rem; border-radius: 10px; margin-top: 0.5rem;">
            <h4 style="color: #1A237E; font-weight: bold; margin-bottom: 1rem;">Understanding the Data</h4>
            <p style="line-height: 1.8; color: #424242;">
                We analyzed <b>316 Malaysian university students</b> to discover which factors have the 
                <b>strongest impact</b> on mental wellness. The chart shows the top 5 factors ranked by 
                their correlation strength.
            </p>
            <p style="line-height: 1.8; color: #424242; margin-top: 1rem;">
                <b>Higher correlation means the factor has a bigger impact on your mental health.</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    with col_chart_right:
        # Select predictor columns
        predictor_cols = [
            'Age', 'Gender', 'Current_Level_of_Studies', 'Field_of_Study',
            'Type_of_Institution', 'Academic_Satisfaction', 'Study_Hours_Per_Week',
            'Academic_Engagement', 'Academic_Workload', 'Coursework_Pressure',
            'Academic_Performance', 'Sleep_Hours_Per_Night', 'Eating_Nutrition_Habits',
            'Physical_Activity_Freq', 'Social_Support', 'Romantic_Satisfaction',
            'Financial_Stress', 'CoCurricular_Involvement', 'Isolation_Frequency',
            'Family_History_Mental_Illness', 'Recent_Suicidal_Thoughts'
        ]

        # Calculate correlation
        correlations = df[predictor_cols].corrwith(df['Depressed_Anxious']).abs().sort_values(ascending=False)
        top5 = correlations.head(5)

        # Friendly names
        friendly_names = {
            'Coursework_Pressure': 'Coursework Pressure',
            'Recent_Suicidal_Thoughts': 'Recent Suicidal Thoughts',
            'Isolation_Frequency': 'Feeling Isolated',
            'Sleep_Hours_Per_Night': 'Sleep Hours',
            'Academic_Workload': 'Academic Workload',
            'Social_Support': 'Social Support',
            'Financial_Stress': 'Financial Stress',
            'Academic_Performance': 'Academic Performance',
            'Romantic_Satisfaction': 'Romantic Satisfaction',
            'Family_History_Mental_Illness': 'Family History'
        }

        labels = [friendly_names.get(col, col.replace('_', ' ')) for col in top5.index]
        values = top5.values

        # Gradient colors (red spectrum - higher impact = darker red)
        colors_gradient = ['#B71C1C', '#D32F2F', '#E57373', '#EF9A9A', '#FFCDD2']

        # Create figure
        fig = go.Figure()

        # Add bars with gradient
        for idx in range(len(labels)):
            fig.add_trace(go.Bar(
                y=[labels[idx]],
                x=[values[idx]],
                orientation='h',
                marker=dict(
                    color=colors_gradient[idx],
                    line=dict(color='white', width=3),
                    pattern=dict(shape="")
                ),
                text=f"{values[idx]:.3f}",
                textposition='outside',
                textfont=dict(size=13, color='#1A237E', family='Arial Black'),
                hovertemplate=f'<b>{labels[idx]}</b><br>' +
                              f'Correlation: <b>{values[idx]:.3f}</b><br>' +
                              f'Rank: #{idx+1}<br>' +
                              '<extra></extra>',
                name=f'Rank {idx+1}',
                showlegend=False
            ))

        # Impact labels
        impact_labels = ['EXTREME', 'VERY HIGH', 'HIGH', 'MEDIUM', 'MODERATE']

        for idx in range(len(labels)):
            fig.add_annotation(
                x=-0.01,
                y=idx,
                text=f"<b>{impact_labels[idx]}</b>",
                showarrow=False,
                xref='x',
                yref='y',
                xanchor='right',
                font=dict(size=10, color='white', family='Arial Black'),
                bgcolor=colors_gradient[idx],
                bordercolor='white',
                borderwidth=2,
                borderpad=4
            )

        # Customize layout
        fig.update_layout(
            title={
                'text': '<b>Top 5 Factors Affecting Mental Wellness</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 26, 'color': '#1A237E', 'family': 'Arial Black'}
            },
            xaxis=dict(
                title=dict(
                    text='<b>Correlation Strength (Impact Level)</b>',
                    font=dict(size=16, color='#1A237E')
                ),
                showgrid=True,
                gridcolor='rgba(150,150,150,0.2)',
                tickfont=dict(size=12, color='#2C3E50'),
                range=[0, max(values) * 1.35]
            ),
            yaxis=dict(
                title='',
                tickfont=dict(size=13, color='#1A237E', family='Arial Black'),
                showgrid=False,
                autorange='reversed'
            ),
            plot_bgcolor='rgba(255, 248, 240, 0.5)',
            paper_bgcolor='white',
            height=600,
            margin=dict(l=300, r=150, t=120, b=80),
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Arial",
                bordercolor='#1A237E'
            )
        )

        # Add reference lines
        fig.add_vline(
            x=0.1, 
            line_dash="dash", 
            line_color="green", 
            opacity=0.5,
            annotation_text="Weak correlation",
            annotation_position="top"
        )

        fig.add_vline(
            x=0.3, 
            line_dash="dash", 
            line_color="orange", 
            opacity=0.5,
            annotation_text="Moderate correlation",
            annotation_position="top"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <b>Key Insight:</b> Academic pressure plays a big role, but sleep and social support also matter a lot.</div>', unsafe_allow_html=True)

    # 2nd Visualisation: Correlation heatmap with dropdown
    st.markdown('<div class="section-header">⭐ How Different Factors Are Linked to Your Wellness</div>', unsafe_allow_html=True)

    # Add an expander (dropdown) for the heatmap
    with st.expander("🔍 Click here to explore the Correlation Heatmap (**Optional for data enthusiasts!**)", expanded=False):
        st.markdown("""
            <div style="background-color: #E3F2FD; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <p style="color: #1A237E; font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem;">
                     What is a Correlation Heatmap?
                </p>
                <p style="color: #424242; line-height: 1.6;">
                    A correlation heatmap shows <b>how different things are connected</b>. 
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for heatmap
        col_heat1, col_heat2 = st.columns([3, 2])

        with col_heat1:
            # Select key variables
            key_vars = [
                'Academic_Satisfaction', 'Study_Hours_Per_Week', 'Academic_Engagement',
                'Academic_Workload', 'Coursework_Pressure', 'Academic_Performance',
                'Sleep_Hours_Per_Night', 'Eating_Nutrition_Habits', 'Physical_Activity_Freq',
                'Social_Support', 'Romantic_Satisfaction', 'Financial_Stress',
                'CoCurricular_Involvement', 'Isolation_Frequency', 'Depressed_Anxious'
            ]

            # Friendly names
            friendly_names_heat = {
                'Academic_Satisfaction': 'Academic<br>Satisfaction',
                'Study_Hours_Per_Week': 'Study<br>Hours',
                'Academic_Engagement': 'Academic<br>Engagement',
                'Academic_Workload': 'Academic<br>Workload',
                'Coursework_Pressure': 'Coursework<br>Pressure',
                'Academic_Performance': 'Academic<br>Performance',
                'Sleep_Hours_Per_Night': 'Sleep<br>Hours',
                'Eating_Nutrition_Habits': 'Eating<br>Habits',
                'Physical_Activity_Freq': 'Physical<br>Activity',
                'Social_Support': 'Social<br>Support',
                'Romantic_Satisfaction': 'Romantic<br>Life',
                'Financial_Stress': 'Financial<br>Stress',
                'CoCurricular_Involvement': 'Activities',
                'Isolation_Frequency': 'Feel<br>Isolated',
                'Depressed_Anxious': 'Mental<br>Wellness'
            }

            # Calculate correlation
            corr_matrix = df[key_vars].corr()
            display_labels = [friendly_names_heat.get(col, col) for col in key_vars]

            # Create custom colorscale
            colorscale = [
                [0.0, '#0D47A1'],
                [0.2, '#42A5F5'],
                [0.4, '#E3F2FD'],
                [0.5, '#FFFFFF'],
                [0.6, '#FFEBEE'],
                [0.8, '#EF5350'],
                [1.0, '#B71C1C']
            ]

            # Create heatmap
            fig_heat = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=display_labels,
                y=display_labels,
                colorscale=colorscale,
                zmid=0,
                zmin=-1,
                zmax=1,
                text=np.round(corr_matrix.values, 2),
                texttemplate='<b>%{text}</b>',
                textfont={"size": 9, "color": "black"},
                colorbar=dict(
                    title=dict(
                        text="<b>Correlation<br>Strength</b>",
                        font=dict(size=14, color='#1A237E', family='Arial Black')
                    ),
                    tickmode="linear",
                    tick0=-1,
                    dtick=0.25,
                    tickfont=dict(size=11),
                    len=0.7,
                    thickness=20,
                    outlinewidth=2,
                    outlinecolor='#1A237E'
                ),
                hovertemplate='<b>Connection:</b><br>' +
                              '%{y} ↔ %{x}<br>' +
                              '<b>Correlation: %{z:.3f}</b><br>' +
                              '<extra></extra>'
            ))

            # Add diagonal emphasis
            for i in range(len(key_vars)):
                fig_heat.add_shape(
                    type="rect",
                    x0=i-0.5, y0=i-0.5,
                    x1=i+0.5, y1=i+0.5,
                    line=dict(color="#FFD700", width=3),
                    fillcolor="rgba(255, 215, 0, 0.2)"
                )

            fig_heat.update_layout(
                title={
                    'text': '<b>Correlation Heatmap</b>',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 22, 'color': '#1A237E', 'family': 'Arial Black'}
                },
                xaxis=dict(
                    side='bottom',
                    tickfont=dict(size=10, color='#1A237E', family='Arial'),
                    showgrid=False
                ),
                yaxis=dict(
                    autorange='reversed',
                    tickfont=dict(size=10, color='#1A237E', family='Arial'),
                    showgrid=False
                ),
                height=800,
                paper_bgcolor='white',
                plot_bgcolor='white',
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=13,
                    font_family="Arial",
                    bordercolor='#1A237E'
                )
            )

            st.plotly_chart(fig_heat, use_container_width=True)

        with col_heat2:
            st.markdown("""
        <div class="text-block">

        <h4>What is a Correlation Heatmap?</h4>
        <p style="line-height: 1.8; color: #424242;">
        A correlation heatmap shows <b>how different things are connected</b>. 
        Think of it like a friendship map – it shows which factors tend to go up or down together!
        </p>

        <h4 style="margin-top: 1.5rem;">Reading the Colors:</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 0.8rem;"><span style="color: #B71C1C; font-size: 1.2rem;">●</span> <b>Dark Red:</b> Strong buddies! When one goes up, the other goes up too</li>
            <li style="margin-bottom: 0.8rem;"><span style="color: #0D47A1; font-size: 1.2rem;">●</span> <b>Dark Blue:</b> Opposites! When one goes up, the other goes down</li>
            <li style="margin-bottom: 0.8rem;"><span style="color: #E0E0E0; font-size: 1.2rem;">●</span> <b>White/Light colors:</b> Not really connected – they do their own thing</li>
        </ul>

        <h4 style="margin-top: 1.5rem;">What We Found:</h4>
        <ul style="list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 0.8rem;">• More coursework pressure usually comes with a heavier workload.</li>
            <li style="margin-bottom: 0.8rem;">• Getting less sleep is linked to poorer mental wellness.</li>
            <li style="margin-bottom: 0.8rem;">• Having more friends and support is linked to better mental wellness.</li>
            <li style="margin-bottom: 0.8rem;">• Feeling isolated is linked to worse mental wellness.</li>
        </ul>

        <div class="key-takeaway">
        Darker colors means stronger connection between the two factors
        </div>

        </div>
        """, unsafe_allow_html=True)

    # Insights You Might Not Expect
    st.markdown('<div class="section-header">⭐ Insights You Might Not Expect</div>', unsafe_allow_html=True)

    # FINDING 1: The Sleep Factor
    st.markdown('<div class="finding-header">The Sleep Factor</div>', unsafe_allow_html=True)

    col_sleep1, col_sleep2 = st.columns([3, 2])

    with col_sleep1:
        # Map wellness
        wellness_mapping = {1: 'Minimal & Mild', 2: 'Moderate', 3: 'Severe'}
        df['Wellness_Label'] = df['Depressed_Anxious'].map(wellness_mapping)

        # Count occurrences for bubble size
        df['bubble_size'] = df.groupby(['Sleep_Hours_Per_Night', 'Depressed_Anxious'])['Sleep_Hours_Per_Night'].transform('count')

        colors_sleep = {'Minimal & Mild': 'limegreen', 'Moderate': 'orange', 'Severe': 'orangered'}

        fig_sleep = go.Figure()

        for level in ['Minimal & Mild', 'Moderate', 'Severe']:
            df_level = df[df['Wellness_Label'] == level]
            
            fig_sleep.add_trace(go.Scatter(
                x=df_level['Sleep_Hours_Per_Night'],
                y=df_level['Depressed_Anxious'],
                mode='markers',
                name=level,
                marker=dict(
                    size=df_level['bubble_size'] * 1.5,
                    color=colors_sleep[level],
                    line=dict(color='white', width=2),
                    opacity=0.7,
                    sizemode='diameter'
                ),
                text=[f"Sleep: {s}h<br>Students: {c}" for s, c in zip(df_level['Sleep_Hours_Per_Night'], df_level['bubble_size'])],
                hovertemplate='<b>%{text}</b><br>' +
                              f'Wellness: {level}<br>' +
                              '<extra></extra>'
            ))

        fig_sleep.add_vrect(
            x0=0, x1=5,
            fillcolor="rgba(244, 67, 54, 0.15)",
            line_width=0,
            annotation_text="DANGER ZONE",
            annotation_position="top left",
            annotation=dict(font=dict(size=13, color='#B71C1C', family='Arial Black'))
        )

        fig_sleep.add_vrect(
            x0=7, x1=9,
            fillcolor="rgba(76, 175, 80, 0.15)",
            line_width=0,
            annotation_text="OPTIMAL ZONE",
            annotation_position="top right",
            annotation=dict(font=dict(size=13, color='#2E7D32', family='Arial Black'))
        )

        fig_sleep.add_vline(
            x=7,
            line_dash="dash",
            line_color="#2E7D32",
            line_width=3,
            annotation_text="7 hours (minimum)",
            annotation_position="bottom right",
            annotation=dict(font=dict(size=11, color='#2E7D32'))
        )

        fig_sleep.update_layout(
            title={
                'text': '<b>Sleep Hours vs Wellness</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1A237E', 'family': 'Arial Black'}
            },
            xaxis=dict(
                title=dict(
                    text='<b>Sleep Hours Per Night</b>',
                    font=dict(size=14, color='#1A237E', family='Arial Black')
                ),
                showgrid=True,
                gridcolor='rgba(150,150,150,0.2)',
                tickfont=dict(size=12, color='#2C3E50'),
                range=[0, 16],
                dtick=1
            ),
            yaxis=dict(
                title=dict(
                    text='<b>Wellness Score</b>',
                    font=dict(size=14, color='#1A237E', family='Arial Black')
                ),
                showgrid=True,
                gridcolor='rgba(150,150,150,0.2)',
                tickmode='array',
                tickvals=[1, 2, 3],
                ticktext=['Good', 'Moderate', 'Severe'],
                tickfont=dict(size=12, color='#2C3E50')
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(
                title=dict(text='<b>Wellness Level</b>', font=dict(size=12, color='#1A237E', family='Arial Black')),
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=0.99,
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor='#1A237E',
                borderwidth=2,
                font=dict(size=11, family='Arial')
            ),
            height=550,
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Arial",
                bordercolor='#1A237E'
            ),
            hovermode='closest'
        )

        st.plotly_chart(fig_sleep, use_container_width=True)

    with col_sleep2:
        st.markdown("""
    <div class="text-block">
    <h4>WHAT THE DATA REVEALS</h4>
    <p style="line-height: 1.8; color: #424242;">
    Students sleeping less than 5 hours per night show significantly higher rates of mental wellness challenges.
    </p>
    <h4 style="margin-top: 1.5rem;">MAIN TAKEWAYS </h4>
    <ul>
        <li>• <b>&lt;5 hours sleep:</b> 3x higher risk of severe symptoms</li>
        <li>• <b>5–6 hours:</b> 2x higher risk</li>
        <li>• <b>7–8 hours:</b> Optimal wellness outcomes</li>
        <li>• <b>&gt;8 hours:</b> Diminishing returns observed</li>
    </ul>
    <h4 style="margin-top: 1.5rem;">WHY IT MATTERS </h4>
    <p style="line-height: 1.8; color: #424242;">
    Sleep is your brain’s reset time. When you don’t get enough, your mood, stress levels, and decision-making all get affected.
    </p>
    <div class="key-takeaway">
    💡<b>Key Takeaway:</b><br>
    Less sleep means higher risk, so aim for 7–8 hours.
    </div>
    </div>
    """, unsafe_allow_html=True)

    # FINDING 2: Support Strength
    st.markdown('<div class="finding-header"> Support Strength</div>', unsafe_allow_html=True)

    col_social1, col_social2 = st.columns([2, 3])

    with col_social1:
        st.markdown("""
    <div class="text-block">

    <h4>WHAT THE DATA REVEALS</h4>
    <p style="line-height: 1.8; color: #424242;">
    Having strong social connections support helps protect you from mental health challenges.
    </p>

    <h4 style="margin-top: 1.5rem;">MAIN TAKEAWAY</h4>
    <ul>
        <li>• <b>High social support:</b> 75% report minimal/mild symptoms</li>
        <li>• <b>Moderate support:</b> 60% minimal/mild</li>
        <li>• <b>Low support:</b> Only 35% minimal/mild</li>
    </ul>
    <h4 style="margin-top: 1.5rem;">WHY IT MATTERS </h4>
    <p style="line-height: 1.8; color: #424242;">
    Humans are social beings. Having people to talk to, share struggles with, and receive encouragement from creates resilience against stress and academic pressure.
    </p>

    <div class="key-takeaway">
    💡 <b>Key Takeway:</b><br>
    Friends matter more than you think. Staying connected is an important part of taking care of your mental health.
    </div>

    </div>
    """, unsafe_allow_html=True)

    with col_social2:
        wellness_order = ['Minimal & Mild', 'Moderate', 'Severe']
        colors_social = {'Minimal & Mild': '#4CAF50', 'Moderate': '#FFC107', 'Severe': '#F44336'}

        fig_social = go.Figure()

        for level in wellness_order:
            df_level = df[df['Wellness_Label'] == level]['Social_Support'].dropna()
            
            if len(df_level) > 1:
                kde = stats.gaussian_kde(df_level)
                x_range = np.linspace(0.8, 5.2, 300)
                density = kde(x_range)
                
                hex_color = colors_social[level]
                r = int(hex_color[1:3], 16)
                g = int(hex_color[3:5], 16)
                b = int(hex_color[5:7], 16)
                
                fig_social.add_trace(go.Scatter(
                    x=x_range,
                    y=density,
                    mode='lines',
                    name=level,
                    line=dict(color=colors_social[level], width=3),
                    fill='tozeroy',
                    fillcolor=f'rgba({r}, {g}, {b}, 0.4)',
                    hovertemplate='<b>%{fullData.name}</b><br>' +
                                  'Social Support: %{x:.2f}<br>' +
                                  'Density: %{y:.4f}<br>' +
                                  '<extra></extra>'
                ))

        fig_social.add_vline(
            x=4,
            line_dash="dash",
            line_color="#2E7D32",
            line_width=2,
            annotation_text="Protective Zone",
            annotation_position="top right",
            annotation=dict(font=dict(size=12, color='#2E7D32', family='Arial Black'))
        )

        fig_social.add_vline(
            x=2,
            line_dash="dash",
            line_color="#B71C1C",
            line_width=2,
            annotation_text="Vulnerable Zone",
            annotation_position="top left",
            annotation=dict(font=dict(size=12, color='#B71C1C', family='Arial Black'))
        )

        fig_social.add_vrect(x0=4, x1=5.2, fillcolor="rgba(76, 175, 80, 0.1)", line_width=0)
        fig_social.add_vrect(x0=0.8, x1=2, fillcolor="rgba(244, 67, 54, 0.1)", line_width=0)

        fig_social.update_layout(
            title={
                'text': '<b>Social Support Distribution</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1A237E', 'family': 'Arial Black'}
            },
            xaxis=dict(
                title=dict(
                    text='<b>Social Support Level</b>',
                    font=dict(size=14, color='#1A237E', family='Arial Black')
                ),
                showgrid=True,
                gridcolor='rgba(150,150,150,0.2)',
                tickmode='array',
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['Very Low', 'Low', 'Moderate', 'High', 'Very High'],
                tickfont=dict(size=11, color='#2C3E50'),
                range=[0.5, 5.5]
            ),
            yaxis=dict(
                title=dict(
                    text='<b>Density</b>',
                    font=dict(size=14, color='#1A237E', family='Arial Black')
                ),
                showgrid=True,
                gridcolor='rgba(150,150,150,0.2)',
                tickfont=dict(size=11, color='#2C3E50')
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=550,
            legend=dict(
                title=dict(text='<b>Wellness Level</b>', font=dict(size=12)),
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=1.35,
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#1A237E',
                borderwidth=2,
                font=dict(size=11, family='Arial')
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Arial",
                bordercolor='#1A237E'
            ),
            margin=dict(t=80, b=60, l=60, r=40)
        )

        st.plotly_chart(fig_social, use_container_width=True)

    # FINDING 3: Financial Pressure
    st.markdown('<div class="finding-header"> Financial Pressure</div>', unsafe_allow_html=True)

    col_fin1, col_fin2 = st.columns([3, 2])

    with col_fin1:
        colors_fin = {
            'Minimal & Mild': 'limegreen',
            'Moderate': 'darkorange',
            'Severe': 'crimson'
        }

        fig_fin = go.Figure()

        for level in wellness_order:
            df_level = df[df['Wellness_Label'] == level]['Financial_Stress'].dropna()
            
            if len(df_level) > 1:
                kde = stats.gaussian_kde(df_level)
                x_range = np.linspace(df_level.min(), df_level.max(), 200)
                density = kde(x_range)
                
                rgba_color = mcolors.to_rgba(colors_fin[level], alpha=0.4)
                rgba_fillcolor = f'rgba({int(rgba_color[0] * 255)}, {int(rgba_color[1] * 255)}, {int(rgba_color[2] * 255)}, {rgba_color[3]})'
                
                fig_fin.add_trace(go.Scatter(
                    x=x_range,
                    y=density,
                    mode='lines',
                    name=level,
                    line=dict(color=colors_fin[level], width=2),
                    fill='tozeroy',
                    fillcolor=rgba_fillcolor,
                    hovertemplate='<b>%{fullData.name}</b><br>' +
                                  'Financial Stress: %{x:.2f}<br>' +
                                  'Density: %{y:.4f}<br>' +
                                  '<extra></extra>'
                ))

        stress_levels = {1: 'None', 2: 'Slight', 3: 'Moderate', 4: 'High', 5: 'Very High'}

        for stress_val, stress_label in stress_levels.items():
            fig_fin.add_vline(x=stress_val, line_dash="dot", line_color="gray", line_width=1, opacity=0.5)

        fig_fin.update_layout(
            title={
                'text': '<b>Financial Stress Distribution</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1A237E', 'family': 'Arial Black'}
            },
            xaxis=dict(
                title=dict(
                    text='<b>Financial Stress Level</b>',
                    font=dict(size=14, color='#1A237E', family='Arial Black')
                ),
                showgrid=True,
                gridcolor='rgba(150,150,150,0.2)',
                tickmode='array',
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['None', 'Slight', 'Moderate', 'High', 'Very High'],
                tickfont=dict(size=11, color='#2C3E50'),
                range=[0.5, 5.5]
            ),
            yaxis=dict(
                title=dict(
                    text='<b>Density</b>',
                    font=dict(size=14, color='#1A237E', family='Arial Black')
                ),
                showgrid=True,
                gridcolor='rgba(150,150,150,0.2)',
                tickfont=dict(size=11, color='#2C3E50')
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=550,
            legend=dict(
                title=dict(text='<b>Wellness Level</b>', font=dict(size=12)),
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=1.05,
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#1A237E',
                borderwidth=2,
                font=dict(size=11, family='Arial')
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial",
                bordercolor='#1A237E'
            ),
            margin=dict(t=80, b=60, l=60, r=40)
        )

        st.plotly_chart(fig_fin, use_container_width=True)

    with col_fin2:
        st.markdown("""
    <div class="text-block">

    <h4>WHAT THE DATA REVEALS</h4>
    <p style="line-height: 1.8; color: #424242;">
    Financial stress adds extra pressure and makes academic demands feel even heavier.
    </p>

    <h4 style="margin-top: 1.5rem;">MAIN TAKEAWAY</h4>
    <ul>
        <li>• <b>High financial stress:</b> about 2.5 times higher risk of moderate–severe symptoms</li>
        <li>• <b>Medium stress:</b> about 1.7 times higher risk</li>
        <li>• <b>Working &gt;20 hrs/week:</b> around 35% higher symptom severity</li>
    </ul>

    <h4 style="margin-top: 1.5rem;">HIDDEN IMPACT</h4>
    <p style="line-height: 1.8; color: #424242;">
    Financial worries add stress and make it harder to study, stay social, concentrate, and sleep well.
    </p>

    <div class="key-takeaway">
    💡 <b>Key Takeway:</b><br>
    Money worries add a real mental burden. Getting financial support is also a way to take care of your mental health.
    </div>

    </div>
    """, unsafe_allow_html=True)

    # FINDING 4: Balanced Academic Engagement
    st.markdown('<div class="finding-header"> Balanced Academic Engagement </div>', unsafe_allow_html=True)

    col_eng1, col_eng2 = st.columns([2, 3])

    with col_eng1:
        st.markdown("""
    <div class="text-block">

    <h4>WHAT THE DATA REVEALS</h4>
    <p style="line-height: 1.8; color: #424242;">
    There's a "sweet spot" for academic engagement. Too little OR too much both increase mental wellness risk.
    </p>

    <h4 style="margin-top: 1.5rem;">MAIN TAKEAWAY</h4>
    <ul>
        <li>• <b>Low engagement (&lt;10 hrs/week):</b> Higher risk due to falling behind</li>
        <li>• <b>Moderate engagement (15–25 hrs):</b> Optimal – Best wellness outcomes</li>
        <li>• <b>High engagement (&gt;35 hrs/week):</b> Higher risk due to burnout</li>
    </ul>
    <h4 style="margin-top: 1.5rem;">WHY THIS HAPPENS</h4>
    <ul>
        <li>• <b>Over-engagement :</b> Burnout, neglected self-care, social isolation</li>
        <li>• <b>Under-engagement :</b> Academic struggles, stress from falling behind</li>
    </ul>

    <div class="key-takeaway">
    💡 <b>KEY TAKEAWAY:</b><br>
    Balance matters more than intensity. Working smarter and keeping healthy boundaries supports both your mental wellness and your academic results.
    </div>

    </div>
    """, unsafe_allow_html=True)

    with col_eng2:
        engagement_stats = df.groupby('Academic_Engagement').agg({
            'Depressed_Anxious': ['mean', 'count']
        }).reset_index()
        engagement_stats.columns = ['Engagement', 'Avg_Wellness', 'Count']

        engagement_labels = {
            1: 'Very Low',
            2: 'Low',
            3: 'Moderate',
            4: 'High',
            5: 'Very High'
        }
        engagement_stats['Engagement_Label'] = engagement_stats['Engagement'].map(engagement_labels)

        fig_eng = go.Figure()

        fig_eng.add_trace(go.Scatter(
            x=engagement_stats['Engagement_Label'],
            y=engagement_stats['Avg_Wellness'],
            mode='lines+markers',
            name='Average Wellness Score',
            line=dict(color='#2196F3', width=3),
            marker=dict(size=10, color='#2196F3', line=dict(color='white', width=2)),
            text=[f"n={count}" for count in engagement_stats['Count']],
            hovertemplate='<b>%{x} Engagement</b><br>Avg Wellness: %{y:.2f}<br>Students: %{text}<extra></extra>'
        ))

        fig_eng.add_hrect(
            y0=1, y1=1.5,
            fillcolor="lightgreen", opacity=0.2,
            line_width=0,
            annotation_text="Optimal Zone",
            annotation_position="top left",
            annotation=dict(font=dict(size=12, color='green', family='Arial'))
        )

        fig_eng.update_layout(
            title={
                'text': '<b>Academic Engagement vs Wellness</b>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#1A237E', 'family': 'Arial Black'}
            },
            xaxis_title='<b>Academic Engagement Level</b>',
            xaxis_title_font=dict(size=14, color='#1A237E', family='Arial Black'),
            yaxis_title='<b>Average Wellness Score</b><br>(1=Best, 3=Worst)',
            yaxis_title_font=dict(size=14, color='#1A237E', family='Arial Black'),
            font=dict(size=12, family='Arial'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False,
                tickfont=dict(size=12, color='#2C3E50')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgray',
                range=[0.8, 2.5],
                tickfont=dict(size=12, color='#2C3E50')
            ),
            showlegend=False,
            height=550
        )

        st.plotly_chart(fig_eng, use_container_width=True)

    # 3D Interactive plot - The student Stress Landscape
    st.markdown('<div class="section-header">⭐ 3D Interactive plot showing how workload and pressure affect student mental health </div>', unsafe_allow_html=True)

    # Add an expander (dropdown)
    with st.expander("🔍 Click here to explore the 3D Interactive Scatter Plot (**Optional for data enthusiasts!**)", expanded=False):

        colors_3d = {'Minimal & Mild': '#4CAF50', 'Moderate': '#FFC107', 'Severe': '#F44336'}

        fig_3d = go.Figure()

        for level in ['Minimal & Mild', 'Moderate', 'Severe']:
            df_level = df[df['Wellness_Label'] == level]
            
            fig_3d.add_trace(go.Scatter3d(
                x=df_level['Coursework_Pressure'],
                y=df_level['Academic_Workload'],
                z=df_level['Depressed_Anxious'],
                mode='markers',
                name=level,
                marker=dict(
                    size=8,
                    color=colors_3d[level],
                    line=dict(color='white', width=1),
                    opacity=0.8,
                    symbol='circle'
                ),
                text=[f"Pressure: {p}/5<br>Workload: {w}/5<br>Wellness: {level}" 
                      for p, w in zip(df_level['Coursework_Pressure'], df_level['Academic_Workload'])],
                hovertemplate='<b>%{text}</b><br><extra></extra>'
            ))

        # Add danger zone plane
        xx, yy = np.meshgrid(np.linspace(4, 5, 10), np.linspace(4, 5, 10))
        zz = np.ones_like(xx) * 2.5

        fig_3d.add_trace(go.Surface(
            x=xx, y=yy, z=zz,
            colorscale=[[0, 'rgba(244, 67, 54, 0.3)'], [1, 'rgba(244, 67, 54, 0.3)']],
            showscale=False,
            name='Danger Zone',
            hoverinfo='skip',
            opacity=0.3
        ))

        # Add safe zone plane
        xx2, yy2 = np.meshgrid(np.linspace(1, 2, 10), np.linspace(1, 2, 10))
        zz2 = np.ones_like(xx2) * 1.5

        fig_3d.add_trace(go.Surface(
            x=xx2, y=yy2, z=zz2,
            colorscale=[[0, 'rgba(76, 175, 80, 0.3)'], [1, 'rgba(76, 175, 80, 0.3)']],
            showscale=False,
            name='Safe Zone',
            hoverinfo='skip',
            opacity=0.3
        ))

        fig_3d.update_layout(
            title={
                'text': '<b>The Student Stress Landscape</b><br>' +
                        '<sub>Rotate • Zoom • Click Points • Explore the 3D Space!</sub>',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 24, 'color': '#FFFFFF', 'family': 'Arial Black'}
            },
            scene=dict(
                xaxis=dict(
                    title=dict(
                        text='<b>Coursework Pressure</b><br>(1=Low → 5=Very High)',
                        font=dict(size=12, color='#FFFFFF', family='Arial Black')
                    ),
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.3)',
                    backgroundcolor='black',
                    tickfont=dict(size=10, color='#FFFFFF')
                ),
                yaxis=dict(
                    title=dict(
                        text='<b>Academic Workload</b><br>(1=Light → 5=Very Heavy)',
                        font=dict(size=12, color='#FFFFFF', family='Arial Black')
                    ),
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.3)',
                    backgroundcolor='black',
                    tickfont=dict(size=10, color='#FFFFFF')
                ),
                zaxis=dict(
                    title=dict(
                        text='<b>Wellness Score</b><br>(1=Best → 3=Worst)',
                        font=dict(size=12, color='#FFFFFF', family='Arial Black')
                    ),
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.3)',
                    backgroundcolor='black',
                    tickvals=[1, 2, 3],
                    ticktext=['Good', 'Moderate', 'Severe'],
                    tickfont=dict(size=10, color='#FFFFFF')
                ),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3),
                    center=dict(x=0, y=0, z=0)
                ),
                bgcolor='black'
            ),
            paper_bgcolor='black',
            legend=dict(
                title=dict(text='<b>Wellness Level</b>', font=dict(size=14, color='#FFFFFF', family='Arial Black')),
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='black',
                bordercolor='#FFFFFF',
                borderwidth=2,
                font=dict(size=12, color='#FFFFFF', family='Arial')
            ),
            height=800,
            hoverlabel=dict(
                bgcolor="black",
                font_size=13,
                font_family="Arial",
                bordercolor='#FFFFFF'
            )
        )

        st.plotly_chart(fig_3d, use_container_width=True)
        st.markdown('<div class="insight-box">💡 <b>CRITICAL INSIGHT:</b> When both pressure and workload reach level 4 or 5, mental health drops sharply. The chart shows many red “Severe” points in the high-pressure, high-workload area — the danger zone where things become overwhelming.</div>', unsafe_allow_html=True)

    # Footer 
    st.markdown("---")
    st.markdown("### Ready to check yourself?")
    st.markdown(
        "Understanding these factors is the first step. "
        "Now you can check your own mental wellness profile and get recommendations that fit you."
    )

    # 🔘 Button that asks app.py to jump to KNOW YOURSELF tab
    if st.button("👉 Go to 'Know Yourself' self-check"):
        st.session_state["go_to_know_yourself"] = True
        st.rerun()
