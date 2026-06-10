import pandas as pd
import os

matches = pd.read_csv("data/processed/wc_matches_1990_2022.csv")
matches["match_date"] = pd.to_datetime(matches["match_date"])
matches = matches.sort_values("match_date").reset_index(drop=True)


feature_rows = []

for _, row in matches.iterrows():
    team_a = row["team_a"]
    team_b = row["team_b"]

    goals_a = row["goals_a"]
    goals_b = row["goals_b"]

    xg_a = row["xg_a"]
    xg_b = row["xg_b"]

    feature_rows.append({
        "match_date": row["match_date"],
        "year": row["year"],
        "tournament": "FIFA World Cup",
        "stage": row["stage"],

        "team_a": team_a,
        "team_b": team_b,

        "goals_a": goals_a,
        "goals_b": goals_b,

        "xg_a": xg_a,
        "xg_b": xg_b,

        "goal_diff": goals_a - goals_b,
        "xg_diff": xg_a - xg_b,

        "team_a_win": goals_a > goals_b,
        "team_b_win": goals_b > goals_a,
        "draw": goals_a == goals_b
    })

match_features = pd.DataFrame(feature_rows)

os.makedirs("data/processed", exist_ok=True)
match_features.to_csv("data/processed/match_features_wc_1990_2022.csv", index=False)

print("Saved: data/processed/match_features_wc_1990_2022.csv")
print(match_features.head())
print(match_features.shape)