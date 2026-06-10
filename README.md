# GoalOracle 2026 ⚽

### FIFA World Cup 2026 Match Intelligence Engine

I built **GoalOracle 2026** as a football analytics project that predicts FIFA World Cup match outcomes using expected goals modelling, custom team ratings, Poisson scoreline simulation, and an interactive Streamlit interface.

This is not a simple win/loss classifier.
The goal was to build something closer to a sports analytics product, where the model shows uncertainty instead of giving one overconfident answer.

---

## Live Demo

```text
https://goaloracle-2026.streamlit.app/
```

---

## Preview

```text
assets/screenshots/goaloracle_ui.png
```

---

## What I Built

GoalOracle V1 can:

- Predict expected goals for both teams
- Estimate win / draw / loss probabilities
- Generate the top 5 most likely scorelines
- Compare team strength using custom rating signals
- Reduce team-order bias using symmetric prediction correction
- Display everything inside a clean dark Streamlit interface
- Link directly to the GitHub repository from the app header

---

## Why I Built This

Most beginner football prediction projects directly predict:

```text
Team A wins
Team B wins
Draw
```

I wanted to take a more realistic approach.

In football, the better team is not guaranteed to win. So instead of giving only one final answer, GoalOracle predicts probabilities.

Example:

```text
Argentina win: 41%
Draw: 27%
Portugal win: 32%
```

This makes the system more honest, explainable, and closer to how real sports analytics models work.

---

## How GoalOracle Works

The prediction pipeline is:

```text
Historical World Cup Data
        ↓
Rolling Team Form Features
        ↓
Random Forest xG Model
        ↓
GoalOracle 2026 Rating Adjustment
        ↓
Symmetric Prediction Correction
        ↓
Poisson Scoreline Simulation
        ↓
Win / Draw / Loss Probabilities
```

---

## Core Idea

Instead of directly predicting the winner, I first predict expected goals:

```text
Team A xG
Team B xG
```

Then I use a Poisson distribution to convert those expected goals into realistic scoreline probabilities.

For example:

```text
Argentina xG: 1.45
Portugal xG: 1.26
```

Possible scorelines:

```text
1-1
1-0
0-1
2-1
1-2
```

From these scoreline probabilities, I calculate the final win / draw / loss chances.

---

## Features

### Match Predictor

The app allows users to select any two teams from the FIFA World Cup 2026 team list.

It returns:

- Expected goals for Team A
- Expected goals for Team B
- Win probability
- Draw probability
- Loss probability
- Most likely scoreline
- Top 5 scorelines
- Rating-based explanation signals

---

### Team Rating Engine

I created a custom rating engine that gives every team four indexes:

```text
oracle_rating
attack_index
defense_index
momentum_index
```

These are calculated using:

- FIFA rank
- Confederation strength
- Host advantage
- Custom weighted rating logic

---

### Symmetric Prediction Correction

During testing, I found that predictions could change too much when I reversed the team order.

Example:

```text
Argentina vs Portugal
Portugal vs Argentina
```

To fix this, I added a symmetric prediction correction.

The model predicts both directions and averages the corresponding xG values. This reduces team-order bias and makes the predictions more stable.

---

### Poisson Scoreline Engine

I use Poisson probability to estimate realistic football scores from expected goals.

The app does not only show one predicted score. It shows a distribution of possible scorelines.

Example:

```text
1-1  → 12.78%
1-0  → 10.17%
0-1  → 10.15%
0-0  → 8.08%
2-1  → 8.05%
```

This makes the output more useful and more realistic.

---

## Tech Stack

| Area               | Tools         |
| ------------------ | ------------- |
| Language           | Python        |
| Data Processing    | Pandas, NumPy |
| Machine Learning   | Scikit-learn  |
| Probability Engine | SciPy         |
| Model Saving       | Joblib        |
| App Framework      | Streamlit     |
| Visualization      | Plotly        |
| Version Control    | Git, GitHub   |

---

## Project Structure

```text
goaloracle-2026/
│
├── app.py
├── requirements.txt
├── test_predictor.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── day2_xg_baseline.ipynb
│
├── Scripts/
│   ├── create_wc_1990_2022.py
│   ├── create_match_features.py
│   └── create_team_ratings_2026.py
│
├── models/
│   └── xg_random_forest_wc_baseline.pkl
│
└── src/
    ├── predictor.py
    │
    ├── ratings/
    │   └── rating_engine.py
    │
    └── simulation/
        ├── match_engine.py
        └── bivariate_poisson.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Soumadipta-Konar/goaloracle-2026.git
cd goaloracle-2026
```

Create and activate environment:

```bash
conda create -n goaloracle python=3.11
conda activate goaloracle
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

---

## Sample Output

```text
Argentina vs Portugal

Base xG : 1.418 - 0.666
Final xG: 1.450 - 0.634

Argentina win: 56.88%
Draw: 26.79%
Portugal win: 16.25%

Most likely score: 1 - 0
```

The model does not say the lower-probability team cannot win.
It only estimates the probability of different outcomes.

---

## Current Limitations

This is **Version 1**, so I am keeping the limitations clear.

- The baseline model is mainly trained on historical World Cup data.
- Euro, Copa America, qualifiers, and recent friendlies are not fully integrated yet.
- Player-level injuries, squad depth, and tactical setups are not included yet.
- The current system focuses on match prediction, not full tournament deployment.
- Penalty shootout modelling is not included in V1.
- The rating engine is custom-built and will improve with more real-world data.

---

## Roadmap

For the next versions, I plan to add:

- Euro and Copa America datasets
- Recent friendlies and qualifiers as momentum updates
- Penalty shootout resolver
- Goalkeeper and penalty strength indexes
- Full tournament simulator inside the app
- Monte Carlo champion probability simulation
- Team dashboard
- Group-stage explorer
- SHAP-based explainability
- Streamlit Cloud deployment

---

## Version Status

```text
V1: Hybrid xG Match Predictor + Poisson Scoreline Engine + Streamlit UI
```

GoalOracle V1 focuses on building the core match prediction engine and presenting it like a sports analytics product.

---

## Author

Built by **Soumadipta Konar**

I am a B.Tech IT student at IIEST Shibpur, interested in AI/ML, sports analytics, startups, and data-driven products.

GitHub: [Soumadipta-Konar](https://github.com/Soumadipta-Konar)
