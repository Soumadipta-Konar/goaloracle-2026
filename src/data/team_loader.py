from pathlib import Path
import pandas as pd


DATA_PATH = Path("data/raw/wc_2026_teams.csv")


def load_teams(path: str | Path = DATA_PATH) -> pd.DataFrame:
    """
    Load base team data for GoalOracle 2026.
    Required columns:
    team, confederation, fifa_rank, host, group
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Team data file not found: {path}")

    df = pd.read_csv(path)

    required_columns = {"team", "confederation", "fifa_rank", "host", "group"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["team"] = df["team"].astype(str)
    df["confederation"] = df["confederation"].astype(str)
    df["fifa_rank"] = df["fifa_rank"].astype(int)
    df["host"] = df["host"].astype(int)
    df["group"] = df["group"].astype(str)

    return df


def get_team_names(df: pd.DataFrame) -> list[str]:
    return sorted(df["team"].unique().tolist())