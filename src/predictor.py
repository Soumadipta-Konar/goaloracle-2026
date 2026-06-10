from pathlib import Path

import joblib
import pandas as pd

from models.rating_adjustment import adjust_xg
from src.simulation.match_engine import match_probabilities
from src.simulation.match_engine import match_probabilities, top_scorelines

class GoalOraclePredictor:
    def __init__(self):
        self.root = Path(__file__).resolve().parents[1]

        self.model_path = self.root / "models" / "xg_random_forest_wc_baseline.pkl"
        self.features_path = self.root / "data" / "processed" / "match_features_wc_1990_2022.csv"
        self.ratings_path = self.root / "data" / "processed" / "team_ratings_2026.csv"

        self.model = joblib.load(self.model_path)
        self.match_features = pd.read_csv(self.features_path)
        self.ratings = pd.read_csv(self.ratings_path)

        self.rating_map = self.ratings.set_index("team").to_dict(orient="index")

        self.feature_cols = [
            "gf_diff",
            "ga_diff",
            "xgf_diff",
            "xga_diff",
            "form_diff",
            "experience_diff",
            "gf_avg_a",
            "ga_avg_a",
            "xgf_avg_a",
            "xga_avg_a",
            "points_avg_a",
            "gf_avg_b",
            "ga_avg_b",
            "xgf_avg_b",
            "xga_avg_b",
            "points_avg_b"
        ]

    def latest_team_state(self, team):
        a_rows = self.match_features[self.match_features["team_a"] == team]
        b_rows = self.match_features[self.match_features["team_b"] == team]

        records = []

        for _, r in a_rows.iterrows():
            records.append({
                "date": r["match_date"],
                "gf_avg": r["gf_avg_a"],
                "ga_avg": r["ga_avg_a"],
                "xgf_avg": r["xgf_avg_a"],
                "xga_avg": r["xga_avg_a"],
                "points_avg": r["points_avg_a"],
                "matches_played": r["matches_played_a"]
            })

        for _, r in b_rows.iterrows():
            records.append({
                "date": r["match_date"],
                "gf_avg": r["gf_avg_b"],
                "ga_avg": r["ga_avg_b"],
                "xgf_avg": r["xgf_avg_b"],
                "xga_avg": r["xga_avg_b"],
                "points_avg": r["points_avg_b"],
                "matches_played": r["matches_played_b"]
            })

        if not records:
            return {
                "gf_avg": 1.30,
                "ga_avg": 1.30,
                "xgf_avg": 1.30,
                "xga_avg": 1.30,
                "points_avg": 1.00,
                "matches_played": 0
            }

        return pd.DataFrame(records).sort_values("date").iloc[-1].drop("date").to_dict()

    def rating_features(self, team_a, team_b):
        if team_a not in self.rating_map:
            raise ValueError(f"{team_a} not found in rating table")

        if team_b not in self.rating_map:
            raise ValueError(f"{team_b} not found in rating table")

        a = self.rating_map[team_a]
        b = self.rating_map[team_b]

        return {
            "oracle_diff": a["oracle_rating"] - b["oracle_rating"],
            "attack_diff": a["attack_index"] - b["attack_index"],
            "defense_diff": a["defense_index"] - b["defense_index"],
            "momentum_diff": a["momentum_index"] - b["momentum_index"],
            "team_a_host": a["host"],
            "team_b_host": b["host"],
            "team_a_oracle": a["oracle_rating"],
            "team_b_oracle": b["oracle_rating"],
            "team_a_attack": a["attack_index"],
            "team_b_attack": b["attack_index"],
            "team_a_defense": a["defense_index"],
            "team_b_defense": b["defense_index"],
            "team_a_momentum": a["momentum_index"],
            "team_b_momentum": b["momentum_index"]
        }

    def build_prediction_row(self, team_a, team_b):
        a = self.latest_team_state(team_a)
        b = self.latest_team_state(team_b)

        return pd.DataFrame([{
            "gf_diff": a["gf_avg"] - b["gf_avg"],
            "ga_diff": b["ga_avg"] - a["ga_avg"],
            "xgf_diff": a["xgf_avg"] - b["xgf_avg"],
            "xga_diff": b["xga_avg"] - a["xga_avg"],
            "form_diff": a["points_avg"] - b["points_avg"],
            "experience_diff": a["matches_played"] - b["matches_played"],

            "gf_avg_a": a["gf_avg"],
            "ga_avg_a": a["ga_avg"],
            "xgf_avg_a": a["xgf_avg"],
            "xga_avg_a": a["xga_avg"],
            "points_avg_a": a["points_avg"],

            "gf_avg_b": b["gf_avg"],
            "ga_avg_b": b["ga_avg"],
            "xgf_avg_b": b["xgf_avg"],
            "xga_avg_b": b["xga_avg"],
            "points_avg_b": b["points_avg"]
        }])
    def top_scorelines(lambda_a, lambda_b, max_goals=6, n=5):
        matrix = score_matrix(lambda_a, lambda_b, max_goals)
        scores = []
        for goals_a in range(matrix.shape[0]):
            for goals_b in range(matrix.shape[1]):
                scores.append({
                    "score": (int(goals_a), int(goals_b)),
                    "probability": float(matrix[goals_a, goals_b])
                })



    def predict_match(self, team_a, team_b):
        if team_a == team_b:
            raise ValueError("Choose two different teams.")

        base_xg_a, base_xg_b = self.base_xg_symmetric(team_a, team_b)
        rating_data = self.rating_features(team_a, team_b)
        final_xg_a, final_xg_b = adjust_xg(base_xg_a, base_xg_b, rating_data)

        probs = match_probabilities(final_xg_a, final_xg_b)
        scorelines = top_scorelines(final_xg_a, final_xg_b)

        return {
            "team_a": team_a,
            "team_b": team_b,
            "base_xg_a": round(base_xg_a, 3),
            "base_xg_b": round(base_xg_b, 3),
            "xg_a": round(final_xg_a, 3),
            "xg_b": round(final_xg_b, 3),
            "team_a_win": round(probs["team_a_win"], 4),
            "draw": round(probs["draw"], 4),
            "team_b_win": round(probs["team_b_win"], 4),
            "most_likely_score": probs["most_likely_score"],
            "rating_features": rating_data,
            "top_scorelines": scorelines
        }
    def base_xg_symmetric(self, team_a, team_b):
        X_ab = self.build_prediction_row(team_a, team_b)
        pred_ab = self.model.predict(X_ab[self.feature_cols])[0]

        X_ba = self.build_prediction_row(team_b, team_a)
        pred_ba = self.model.predict(X_ba[self.feature_cols])[0]

        xg_a = (pred_ab[0] + pred_ba[1]) / 2
        xg_b = (pred_ab[1] + pred_ba[0]) / 2

        xg_a = max(0.05, xg_a)
        xg_b = max(0.05, xg_b)

        return xg_a, xg_b    