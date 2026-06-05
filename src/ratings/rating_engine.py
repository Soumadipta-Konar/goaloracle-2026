import pandas as pd
import numpy as np


def normalize_rank(rank: int, max_rank: int = 100) -> float:
    """
    Lower FIFA rank is better.
    Rank 1 should get close to 100.
    Rank 100 should get lower value.
    """
    rank = max(1, min(rank, max_rank))
    return 100 * (1 - (rank - 1) / max_rank)


def calculate_team_ratings(teams_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create GoalOracle's initial team rating system.

    Ratings:
    - oracle_rating: overall team strength
    - attack_index: estimated attacking strength
    - defense_index: estimated defensive strength
    - momentum_index: current/recent form proxy
    """

    df = teams_df.copy()

    df["rank_strength"] = df["fifa_rank"].apply(normalize_rank)

    # Host boost for USA, Mexico, Canada.
    df["host_boost"] = np.where(df["host"] == 1, 3.0, 0.0)

    # Confederation strength proxy.
    confed_bonus = {
        "UEFA": 3.0,
        "CONMEBOL": 3.0,
        "CONCACAF": 1.0,
        "CAF": 1.5,
        "AFC": 1.0,
        "OFC": 0.0,
    }

    df["confed_bonus"] = df["confederation"].map(confed_bonus).fillna(0.0)

    # Base indexes.
    df["oracle_rating"] = (
        0.85 * df["rank_strength"]
        + df["host_boost"]
        + df["confed_bonus"]
    )

    # Attack and defense are currently estimated from rank strength.
    # Later we will replace these using historical goals scored/conceded.
    df["attack_index"] = (
        0.90 * df["rank_strength"]
        + 0.60 * df["confed_bonus"]
        + 0.40 * df["host_boost"]
    )

    df["defense_index"] = (
        0.88 * df["rank_strength"]
        + 0.70 * df["confed_bonus"]
        + 0.30 * df["host_boost"]
    )

    df["momentum_index"] = (
        0.75 * df["rank_strength"]
        + 0.25 * df["oracle_rating"]
    )

    rating_cols = [
        "oracle_rating",
        "attack_index",
        "defense_index",
        "momentum_index",
    ]

    for col in rating_cols:
        df[col] = df[col].clip(0, 100).round(2)

    return df