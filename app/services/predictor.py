from app.services.team_features import (
    build_team_features,
)

def calculate_team_score(
    features,
):
    """
    Weighted score used for predictions.
    """

    score = 0

    score += features["win_pct"] * 0.40

    score += features["point_diff"] * 3

    score += features["recent_form"] * 2

    score += features["win_streak"] * 1.5

    return max(score, 1)

def predict_matchup(
    db,
    team_a,
    team_b,
):
    """
    Predict a matchup between two teams.
    """

    a = build_team_features(
        db,
        team_a,
    )

    b = build_team_features(
        db,
        team_b,
    )

    team_a_score = calculate_team_score(
        a
    )

    team_b_score = calculate_team_score(
        b
    )

    total = (
        team_a_score
        + team_b_score
    )

    team_a_probability = round(
        team_a_score
        / total
        * 100,
        1,
    )

    team_b_probability = round(
        team_b_score
        / total
        * 100,
        1,
    )

    predicted_winner = (
        team_a
        if team_a_probability
        > team_b_probability
        else team_b
    )

    return {
        "team_a": team_a,
        "team_b": team_b,
        "team_a_probability":
            team_a_probability,
        "team_b_probability":
            team_b_probability,
        "predicted_winner":
            predicted_winner,
    }