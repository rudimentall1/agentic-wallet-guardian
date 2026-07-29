"""
Guardian Reputation Risk Adjustment v1

Adjusts transaction risk based on agent reputation.
"""


def apply_reputation_adjustment(
    risk_score,
    reputation
):

    if not reputation:

        return risk_score


    modifier = reputation.get(
        "risk_modifier",
        0
    )


    adjusted_score = risk_score + modifier


    if adjusted_score > 100:

        adjusted_score = 100


    if adjusted_score < 0:

        adjusted_score = 0


    return adjusted_score
