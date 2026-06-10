from src.predictor import GoalOraclePredictor

predictor = GoalOraclePredictor()
result = predictor.predict_match("Argentina","Portugal")

print(result["team_a"], "vs", result["team_b"])
print("Base xG :", result["base_xg_a"], "-", result["base_xg_b"])
print("Final xG:", result["xg_a"], "-", result["xg_b"])
print(result["team_a"], "win:", round(result["team_a_win"] * 100, 2), "%")
print("Draw:", round(result["draw"] * 100, 2), "%")
print(result["team_b"], "win:", round(result["team_b_win"] * 100, 2), "%")
print("Most likely score:", result["most_likely_score"])
print("Top scorelines:")

for item in result["top_scorelines"]:
    print(item["score"], round(item["probability"] * 100, 2), "%")