import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from src.predictor import GoalOraclePredictor


GITHUB_URL = "https://github.com/Soumadipta-Konar/goaloracle-2026"


st.set_page_config(
    page_title="GoalOracle 2026",
    page_icon="⚽",
    layout="wide"
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.18), transparent 32%),
            radial-gradient(circle at top right, rgba(16, 185, 129, 0.10), transparent 28%),
            linear-gradient(180deg, #050505 0%, #09090B 45%, #000000 100%);
        color: #F5F5F7;
    }

    header, footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 2rem;
        max-width: 1180px;
    }

    .top-nav {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1.5rem;
    }

    .github-btn {
        text-decoration: none;
        color: #F5F5F7 !important;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.14);
        padding: 0.65rem 1.05rem;
        border-radius: 999px;
        font-size: 0.9rem;
        font-weight: 600;
        backdrop-filter: blur(18px);
        transition: 0.2s ease;
    }

    .github-btn:hover {
        background: rgba(255, 255, 255, 0.14);
        border: 1px solid rgba(255, 255, 255, 0.22);
    }

    .hero {
        text-align: center;
        margin-bottom: 2.3rem;
    }

    .eyebrow {
        color: #A1A1AA;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .title {
        font-size: 4.2rem;
        font-weight: 800;
        line-height: 1.02;
        letter-spacing: -0.08em;
        margin-bottom: 0.8rem;
        background: linear-gradient(90deg, #FFFFFF, #A1A1AA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: #A1A1AA;
        font-size: 1.1rem;
        max-width: 720px;
        margin: auto;
        line-height: 1.65;
    }

    .panel {
        background: rgba(24, 24, 27, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 32px;
        padding: 1.35rem;
        box-shadow: 0 30px 90px rgba(0,0,0,0.45);
        backdrop-filter: blur(24px);
    }

    .card {
        background: linear-gradient(180deg, rgba(39,39,42,0.82), rgba(24,24,27,0.82));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 1.35rem;
        height: 100%;
    }

    .small-label {
        color: #A1A1AA;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .big-number {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.06em;
        margin-top: 0.25rem;
        color: #FFFFFF;
    }

    .muted {
        color: #71717A;
        font-size: 0.92rem;
        margin-top: 0.35rem;
    }

    .score {
        text-align: center;
        font-size: 4.4rem;
        font-weight: 800;
        letter-spacing: -0.08em;
        color: #FFFFFF;
        margin-top: 0.25rem;
    }

    .score-caption {
        text-align: center;
        color: #A1A1AA;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 750;
        letter-spacing: -0.04em;
        margin: 1rem 0 0.8rem 0;
        color: #FFFFFF;
    }

    .stSelectbox label {
        color: #D4D4D8 !important;
        font-weight: 600;
    }

    div[data-baseweb="select"] > div {
        background: rgba(39, 39, 42, 0.95);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        color: #FFFFFF;
    }

    .stDataFrame {
        border-radius: 22px;
        overflow: hidden;
    }

    .stAlert {
        background: rgba(127, 29, 29, 0.35);
        border-radius: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_resource
def load_predictor():
    return GoalOraclePredictor()


@st.cache_data
def load_teams():
    ratings = pd.read_csv(ROOT / "data" / "processed" / "team_ratings_2026.csv")
    return sorted(ratings["team"].tolist())


def pct(x):
    return round(x * 100, 2)


def outcome_bar(result):
    outcomes = [
        f'{result["team_a"]} win',
        "Draw",
        f'{result["team_b"]} win'
    ]

    values = [
        pct(result["team_a_win"]),
        pct(result["draw"]),
        pct(result["team_b_win"])
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=values,
            y=outcomes,
            orientation="h",
            text=[f"{v:.2f}%" for v in values],
            textposition="outside",
            marker=dict(
                color=["#F5F5F7", "#A1A1AA", "#71717A"],
                line=dict(width=0)
            ),
            hovertemplate="%{y}: %{x:.2f}%<extra></extra>"
        )
    )

    fig.update_layout(
        height=310,
        margin=dict(l=10, r=50, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F5F5F7", size=14),
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False,
            title=""
        ),
        yaxis=dict(
            title="",
            autorange="reversed"
        ),
        showlegend=False
    )

    return fig


def xg_bar(result):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[result["team_a"], result["team_b"]],
            y=[result["xg_a"], result["xg_b"]],
            text=[result["xg_a"], result["xg_b"]],
            textposition="outside",
            marker=dict(
                color=["#F5F5F7", "#71717A"],
                line=dict(width=0)
            ),
            hovertemplate="%{x}: %{y:.2f} xG<extra></extra>"
        )
    )

    fig.update_layout(
        height=310,
        margin=dict(l=10, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F5F5F7", size=14),
        yaxis=dict(
            title="Expected goals",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            zeroline=False
        ),
        xaxis=dict(title=""),
        showlegend=False
    )

    return fig


def scoreline_df(result):
    rows = []

    for item in result["top_scorelines"]:
        a, b = item["score"]
        rows.append({
            "Scoreline": f"{a} - {b}",
            "Probability": f'{pct(item["probability"])}%'
        })

    return pd.DataFrame(rows)


def explanation_df(result):
    f = result["rating_features"]

    return pd.DataFrame({
        "Signal": [
            "Oracle rating",
            "Attack",
            "Defense",
            "Momentum",
            "Host edge"
        ],
        "Edge": [
            round(f["oracle_diff"], 2),
            round(f["attack_diff"], 2),
            round(f["defense_diff"], 2),
            round(f["momentum_diff"], 2),
            int(f["team_a_host"] - f["team_b_host"])
        ]
    })


predictor = load_predictor()
teams = load_teams()

st.markdown(
    f"""
    <div class="top-nav">
        <a class="github-btn" href="{GITHUB_URL}" target="_blank">
            View on GitHub ↗
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">FIFA World Cup 2026 Intelligence Engine</div>
        <div class="title">GoalOracle</div>
        <div class="subtitle">
            Predict match probabilities from expected goals, current team strength,
            and Poisson scoreline simulation.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        team_a = st.selectbox(
            "First team",
            teams,
            index=teams.index("Argentina") if "Argentina" in teams else 0
        )

    with c2:
        default_b = teams.index("Portugal") if "Portugal" in teams else 1
        team_b = st.selectbox(
            "Second team",
            teams,
            index=default_b
        )

    st.markdown("</div>", unsafe_allow_html=True)

if team_a == team_b:
    st.error("Choose two different teams.")
    st.stop()

result = predictor.predict_match(team_a, team_b)

st.write("")

a_score, b_score = result["most_likely_score"]

k1, k2, k3 = st.columns([1, 1.2, 1])

with k1:
    st.markdown(
        f"""
        <div class="card">
            <div class="small-label">{result["team_a"]}</div>
            <div class="big-number">{result["xg_a"]}</div>
            <div class="muted">Expected goals</div>
            <div class="muted">Base xG {result["base_xg_a"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="card">
            <div class="score-caption">Most likely score</div>
            <div class="score">{a_score} - {b_score}</div>
            <div class="muted" style="text-align:center;">{result["team_a"]} vs {result["team_b"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="card">
            <div class="small-label">{result["team_b"]}</div>
            <div class="big-number">{result["xg_b"]}</div>
            <div class="muted">Expected goals</div>
            <div class="muted">Base xG {result["base_xg_b"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

left, right = st.columns([1.25, 1])

with left:
    st.markdown('<div class="section-title">Win probability</div>', unsafe_allow_html=True)
    st.plotly_chart(outcome_bar(result), use_container_width=True)

with right:
    st.markdown('<div class="section-title">Expected goals</div>', unsafe_allow_html=True)
    st.plotly_chart(xg_bar(result), use_container_width=True)

st.write("")

bottom_left, bottom_right = st.columns([1, 1])

with bottom_left:
    st.markdown('<div class="section-title">Top scorelines</div>', unsafe_allow_html=True)
    st.dataframe(scoreline_df(result), use_container_width=True, hide_index=True)

with bottom_right:
    st.markdown('<div class="section-title">Rating signals</div>', unsafe_allow_html=True)
    st.dataframe(explanation_df(result), use_container_width=True, hide_index=True)