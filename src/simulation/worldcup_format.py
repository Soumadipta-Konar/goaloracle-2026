import pandas as pd


EXPECTED_GROUPS = list("ABCDEFGHIJKL")
TEAMS_PER_GROUP = 4
TOTAL_TEAMS = 48


def validate_worldcup_teams(teams_df: pd.DataFrame) -> dict:

    errors = []

    total_teams = len(teams_df)
    if total_teams != TOTAL_TEAMS:
        errors.append(f"Expected {TOTAL_TEAMS} teams, found {total_teams}.")

    groups = sorted(teams_df["group"].unique().tolist())
    if groups != EXPECTED_GROUPS:
        errors.append(f"Expected groups {EXPECTED_GROUPS}, found {groups}.")

    group_counts = teams_df.groupby("group")["team"].count().to_dict()

    for group in EXPECTED_GROUPS:
        count = group_counts.get(group, 0)
        if count != TEAMS_PER_GROUP:
            errors.append(f"Group {group} should have {TEAMS_PER_GROUP} teams, found {count}.")

    duplicate_teams = teams_df[teams_df["team"].duplicated()]["team"].tolist()
    if duplicate_teams:
        errors.append(f"Duplicate teams found: {duplicate_teams}")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "total_teams": total_teams,
        "groups": group_counts,
    }


def get_groups(teams_df: pd.DataFrame) -> dict[str, list[str]]:

    groups = {}

    for group_name in EXPECTED_GROUPS:
        group_df = teams_df[teams_df["group"] == group_name]
        groups[group_name] = group_df["team"].tolist()

    return groups


def create_group_fixtures(group_teams: list[str]) -> list[tuple[str, str]]:

    if len(group_teams) != 4:
        raise ValueError("Each group must contain exactly 4 teams.")

    fixtures = []

    for i in range(len(group_teams)):
        for j in range(i + 1, len(group_teams)):
            fixtures.append((group_teams[i], group_teams[j]))

    return fixtures


def create_all_group_fixtures(teams_df: pd.DataFrame) -> dict[str, list[tuple[str, str]]]:
    groups = get_groups(teams_df)

    all_fixtures = {}

    for group_name, group_teams in groups.items():
        all_fixtures[group_name] = create_group_fixtures(group_teams)

    return all_fixtures