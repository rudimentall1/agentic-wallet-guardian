"""
Risk Fusion Engine v3

Combines:
- behavior scoring
- security intelligence
- approval intelligence
- token intelligence
- contract intelligence
- data confidence

Principle:

Unknown data != dangerous

Missing data reduces confidence,
but does not create fake threats.
"""


def calculate_risk_engine(
    wallet_data,
    behavior_result,
    security_result
):

    score = 100

    positive = []
    negative = []
    unknown = []


    #
    # Behavior layer
    #

    behavior_score = behavior_result.get(
        "trust_score",
        0
    )


    if behavior_score < 50:

        score -= 30

        negative.append(
            "Poor wallet behavior score"
        )


    elif behavior_score >= 80:

        positive.append(
            "Healthy wallet behavior"
        )



    #
    # Security layer
    #

    security_risk = security_result.get(
        "risk",
        "UNKNOWN"
    )


    if security_risk == "HIGH":

        score -= 40

        negative.append(
            "High security risk detected"
        )


    elif security_risk == "MEDIUM":

        score -= 20

        negative.append(
            "Medium security risk detected"
        )


    else:

        positive.append(
            "No major security threats detected"
        )



    #
    # Approval intelligence
    #

    approvals = wallet_data.get(
        "approvals",
        {}
    )


    if approvals.get(
        "status"
    ) == "limited":

        unknown.append(
            "Approval data unavailable"
        )


    if approvals.get(
        "high_risk"
    ):

        score -= 30

        negative.append(
            "High risk approvals detected"
        )



    #
    # Token intelligence
    #

    token_intelligence = wallet_data.get(
        "token_intelligence",
        {}
    )


    token_risk = token_intelligence.get(
        "risk_score",
        0
    )


    if token_risk >= 50:

        score -= 25

        negative.append(
            "High token risk detected"
        )


    elif token_risk > 0:

        unknown.append(
            "Token data incomplete"
        )



    #
    # Contract intelligence
    #

    contract_intelligence = wallet_data.get(
        "contract_intelligence",
        {}
    )


    contract_risk = contract_intelligence.get(
        "risk_score",
        0
    )


    if contract_risk >= 50:

        score -= 25

        negative.append(
            "Risky contract interaction detected"
        )


    elif contract_risk > 0:

        unknown.append(
            "Contract data incomplete"
        )



    #
    # Data confidence
    #

    data_quality = wallet_data.get(
        "data_quality",
        {}
    )


    confidence = data_quality.get(
        "confidence",
        0
    )


    if confidence < 0.7:

        score -= 10

        unknown.append(
            "Low data confidence"
        )



    #
    # Unknown information penalty
    #
    # Unknown is not a threat.
    # It only prevents perfect score.
    #

    uncertainty_penalty = (
        len(unknown) * 3
    )


    score -= uncertainty_penalty



    #
    # Normalize
    #

    score = max(
        min(score, 100),
        0
    )



    #
    # Risk classification
    #

    if score >= 80:

        risk_level = "LOW"


    elif score >= 50:

        risk_level = "MEDIUM"


    else:

        risk_level = "HIGH"



    return {

        "risk_score":
            score,


        "trust_score":
            score,


        "risk_level":
            risk_level,


        "confidence":
            round(
                confidence,
                2
            ),


        "signals": {

            "positive":
                positive,


            "negative":
                negative,


            "unknown":
                unknown

        },


        "decision":

            "ALLOW"
            if risk_level == "LOW"

            else

            "REVIEW"
            if risk_level == "MEDIUM"

            else

            "BLOCK"

    }
