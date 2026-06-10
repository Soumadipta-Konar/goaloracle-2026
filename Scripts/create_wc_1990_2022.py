import pandas as pd


matches = pd.read_csv("data/raw/matches_1930_2022.csv")


matches["match_date"] = pd.to_datetime(matches["match_date"])


wc_1990_2022 = matches[
    (matches["match_date"].dt.year >= 1990) &
    (matches["match_date"].dt.year <= 2022)
].copy()


wc_1990_2022 = wc_1990_2022[
    [
        "match_date",
        "stage_name",
        "group_stage",
        "knockout_stage",
        "home_team_name",
        "away_team_name",
        "home_team_score",
        "away_team_score",
        "home_team_win",
        "away_team_win",
        "draw"
    ]
]


wc_1990_2022 = wc_1990_2022.rename(columns={
    "home_team_name": "team_a",
    "away_team_name": "team_b",
    "home_team_score": "goals_a",
    "away_team_score": "goals_b",
    "home_team_win": "team_a_win",
    "away_team_win": "team_b_win"
})

# Save clean CSV
wc_1990_2022.to_csv("data/processed/wc_matches_1990_2022.csv", index=False)

print("Saved: data/processed/wc_matches_1990_2022.csv")
print(wc_1990_2022.head())
print(wc_1990_2022.shape)