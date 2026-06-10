import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.features.rating_engine import calculate_team_ratings

teams_path = ROOT / "data" / "raw" / "wc_2026_teams.csv"
output_path = ROOT / "data" / "processed" / "team_ratings_2026.csv"

teams = pd.read_csv(teams_path)
ratings = calculate_team_ratings(teams)

output_path.parent.mkdir(parents=True, exist_ok=True)
ratings.to_csv(output_path, index=False)

print("Saved:", output_path)
print(ratings.head())
print(ratings.shape)