from src.data.team_loader import load_teams
from src.ratings.rating_engine import calculate_team_ratings
from src.features.team_features import create_match_features


def main():
    teams = load_teams()
    ratings = calculate_team_ratings(teams)

    print("\n=== GoalOracle 2026: Day 1 Rating Table ===\n")
    print(
        ratings[
            [
                "team",
                "confederation",
                "fifa_rank",
                "host",
                "group",
                "oracle_rating",
                "attack_index",
                "defense_index",
                "momentum_index",
            ]
        ].sort_values("oracle_rating", ascending=False)
    )

    print("\n=== Sample Match Features ===\n")
    features = create_match_features(ratings, "Argentina", "France")

    for key, value in features.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()