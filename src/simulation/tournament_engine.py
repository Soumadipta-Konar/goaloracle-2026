import random

import pandas as pd


class TournamentEngine:
    def __init__(self, predictor, ratings_path="data/processed/team_ratings_2026.csv", seed=42):
        self.predictor = predictor
        self.teams = pd.read_csv(ratings_path)
        random.seed(seed)

    def simulate_group_match(self, team_a, team_b):
        result = self.predictor.predict_match(team_a, team_b)

        outcomes = [team_a, "Draw", team_b]
        probs = [
            result["team_a_win"],
            result["draw"],
            result["team_b_win"]
        ]

        winner = random.choices(outcomes, weights=probs, k=1)[0]

        if winner == team_a:
            goals_a, goals_b = 1, 0
        elif winner == team_b:
            goals_a, goals_b = 0, 1
        else:
            goals_a, goals_b = 1, 1

        return {
            "team_a": team_a,
            "team_b": team_b,
            "winner": winner,
            "goals_a": goals_a,
            "goals_b": goals_b,
            "team_a_win_prob": result["team_a_win"],
            "draw_prob": result["draw"],
            "team_b_win_prob": result["team_b_win"]
        }

    def simulate_group(self, group_name):
        group_teams = self.teams[self.teams["group"] == group_name]["team"].tolist()

        table = {
            team: {
                "team": team,
                "played": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0,
                "goal_difference": 0,
                "points": 0
            }
            for team in group_teams
        }

        matches = []

        for i in range(len(group_teams)):
            for j in range(i + 1, len(group_teams)):
                team_a = group_teams[i]
                team_b = group_teams[j]

                match = self.simulate_group_match(team_a, team_b)
                matches.append(match)

                goals_a = match["goals_a"]
                goals_b = match["goals_b"]

                table[team_a]["played"] += 1
                table[team_b]["played"] += 1

                table[team_a]["goals_for"] += goals_a
                table[team_a]["goals_against"] += goals_b

                table[team_b]["goals_for"] += goals_b
                table[team_b]["goals_against"] += goals_a

                if goals_a > goals_b:
                    table[team_a]["wins"] += 1
                    table[team_b]["losses"] += 1
                    table[team_a]["points"] += 3

                elif goals_b > goals_a:
                    table[team_b]["wins"] += 1
                    table[team_a]["losses"] += 1
                    table[team_b]["points"] += 3

                else:
                    table[team_a]["draws"] += 1
                    table[team_b]["draws"] += 1
                    table[team_a]["points"] += 1
                    table[team_b]["points"] += 1

        standings = pd.DataFrame(table.values())
        standings["goal_difference"] = standings["goals_for"] - standings["goals_against"]

        standings = standings.sort_values(
            ["points", "goal_difference", "goals_for"],
            ascending=[False, False, False]
        ).reset_index(drop=True)

        return standings, pd.DataFrame(matches)

    def simulate_knockout_match(self, team_a, team_b):
        result = self.predictor.predict_match(team_a, team_b)

        probs = [
            result["team_a_win"],
            result["team_b_win"]
        ]

        winner = random.choices([team_a, team_b], weights=probs, k=1)[0]

        return {
            "team_a": team_a,
            "team_b": team_b,
            "winner": winner,
            "team_a_win_prob": result["team_a_win"],
            "team_b_win_prob": result["team_b_win"],
            "most_likely_score": result["most_likely_score"]
        }

    def simulate_tournament_once(self):
        group_winners = []
        group_runners_up = []
        third_place_teams = []
        group_results = {}

        for group in sorted(self.teams["group"].unique()):
            standings, matches = self.simulate_group(group)

            group_results[group] = {
                "standings": standings,
                "matches": matches
            }

            group_winners.append(standings.iloc[0]["team"])
            group_runners_up.append(standings.iloc[1]["team"])

            third_place = standings.iloc[2].copy()
            third_place["group"] = group
            third_place_teams.append(third_place)

        third_place_df = pd.DataFrame(third_place_teams)

        best_thirds = third_place_df.sort_values(
            ["points", "goal_difference", "goals_for"],
            ascending=[False, False, False]
        ).head(8)["team"].tolist()

        knockout_teams = group_winners + group_runners_up + best_thirds
        random.shuffle(knockout_teams)

        rounds = {}
        current_round = knockout_teams

        round_names = [
            "Round of 32",
            "Round of 16",
            "Quarter-finals",
            "Semi-finals",
            "Final"
        ]

        for round_name in round_names:
            next_round = []
            matches = []

            for i in range(0, len(current_round), 2):
                team_a = current_round[i]
                team_b = current_round[i + 1]

                match = self.simulate_knockout_match(team_a, team_b)
                matches.append(match)
                next_round.append(match["winner"])

            rounds[round_name] = pd.DataFrame(matches)
            current_round = next_round

        champion = current_round[0]

        return {
            "champion": champion,
            "group_results": group_results,
            "best_thirds": best_thirds,
            "knockout_rounds": rounds
        }