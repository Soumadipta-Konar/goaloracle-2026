import numpy as np
from scipy.stats import poisson


def score_matrix(lambda_a, lambda_b, max_goals=6):
    matrix = np.zeros((max_goals + 1, max_goals + 1))

    for goals_a in range(max_goals + 1):
        for goals_b in range(max_goals + 1):
            matrix[goals_a, goals_b] = (
                poisson.pmf(goals_a, lambda_a)
                * poisson.pmf(goals_b, lambda_b)
            )

    return matrix


def match_probabilities(lambda_a, lambda_b, max_goals=6):
    matrix = score_matrix(lambda_a, lambda_b, max_goals)

    team_a_win = np.tril(matrix, -1).sum()
    draw = np.trace(matrix)
    team_b_win = np.triu(matrix, 1).sum()

    score = np.unravel_index(np.argmax(matrix), matrix.shape)

    return {
        "team_a_win": float(team_a_win),
        "draw": float(draw),
        "team_b_win": float(team_b_win),
        "most_likely_score": (int(score[0]), int(score[1])),
        "score_matrix": matrix
    }
def top_scorelines(lambda_a, lambda_b, max_goals=6, n=5):
    matrix = score_matrix(lambda_a, lambda_b, max_goals)

    scores = []

    for goals_a in range(matrix.shape[0]):
        for goals_b in range(matrix.shape[1]):
            scores.append({
                "score": (int(goals_a), int(goals_b)),
                "probability": float(matrix[goals_a, goals_b])
            })

    scores = sorted(scores, key=lambda x: x["probability"], reverse=True)

    return scores[:n]