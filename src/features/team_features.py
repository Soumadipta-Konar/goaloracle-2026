import pandas as pd


def get_team_row(ratings_df: pd.DataFrame, team_name: str) -> pd.Series:
    row = ratings_df[ratings_df["team"] == team_name]

    if row.empty:
        raise ValueError(f"Team not found: {team_name}")

    return row.iloc[0]


def create_match_features(
    ratings_df: pd.DataFrame,
    team_a: str,
    team_b: str
) -> dict:
    """
    Create feature differences between two teams.
    These features will feed the match predictor later.
    """

    if team_a == team_b:
        raise ValueError("Team A and Team B cannot be the same.")

    a = get_team_row(ratings_df, team_a)
    b = get_team_row(ratings_df, team_b)

    features = {
        "team_a": team_a,
        "team_b": team_b,

        "oracle_diff": round(float(a["oracle_rating"] - b["oracle_rating"]), 2),
        "attack_diff": round(float(a["attack_index"] - b["attack_index"]), 2),
        "defense_diff": round(float(a["defense_index"] - b["defense_index"]), 2),
        "momentum_diff": round(float(a["momentum_index"] - b["momentum_index"]), 2),

        "team_b_oracle": round(float(b["oracle_rating"])),
        "team_a_oracle": round(float(a["oracle_rating"])),

        "team_b_attack": round(float(b["attack_index"])),
        "team_a_attack": round(float(a["attack_index"])),

        "team_b_defense": round(float(b["defense_index"])),
        "team_a_defense": round(float(a["defense_index"])),

        "team_a_host": int(a["host"]),
        "team_b_host": int(b["host"]),
    }

    return features