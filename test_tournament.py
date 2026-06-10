from src.predictor import GoalOraclePredictor
from src.simulation.tournament_engine import TournamentEngine

predictor = GoalOraclePredictor()
engine = TournamentEngine(predictor)

standings, matches = engine.simulate_group("A")

print("Group A standings")
print(standings)

print("\nGroup A matches")
print(matches)

result = engine.simulate_tournament_once()

print("\nChampion:", result["champion"])
print("\nFinal")
print(result["knockout_rounds"]["Final"])