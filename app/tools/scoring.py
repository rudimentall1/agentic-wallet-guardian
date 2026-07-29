def calculate_score(data):

    score = 100

    signals = []

    positive = []
    negative = []
    unknown = []


    #
    # Transaction activity
    #

    if data.get("transactions") is not None:

        if data["transactions"] < 5:

            score -= 20

            signals.append(
                "Very low wallet activity"
            )

            negative.append(
                "Very low wallet activity"
            )


        elif data["transactions"] > 1000:

            signals.append(
                "Highly active wallet"
            )

            positive.append(
                "Wallet is highly active"
            )



    #
    # ETH balance
    #

    if data.get("balance_eth") is not None:

        if data["balance_eth"] > 1000:

            signals.append(
                "Large ETH balance detected"
            )

            positive.append(
                "Large ETH balance detected"
            )



    #
    # Token intelligence
    #
    # Missing data = uncertainty, NOT risk
    #

    token_activity = data.get(
        "token_activity"
    )


    if token_activity is None:

        signals.append(
            "Token intelligence unavailable"
        )

        unknown.append(
            "Token intelligence unavailable"
        )


    elif token_activity.get(
        "token_quality"
    ) == "LIMITED":

        signals.append(
            "Token intelligence limited"
        )

        unknown.append(
            "Token intelligence limited"
        )


    elif token_activity.get(
        "error"
    ):

        signals.append(
            "Token intelligence unavailable"
        )

        unknown.append(
            "Token intelligence unavailable"
        )



    #
    # Contract intelligence
    #
    # Missing data = uncertainty, NOT risk
    #

    contract_analysis = data.get(
        "contract_analysis"
    )


    if (
        contract_analysis is None
        or contract_analysis.get("error")
    ):

        signals.append(
            "Contract intelligence unavailable"
        )

        unknown.append(
            "Contract analysis unavailable"
        )



    #
    # Wallet age
    #

    if (
        data.get("wallet_age_days") is not None
        and data["wallet_age_days"] < 7
    ):

        score -= 30

        signals.append(
            "New wallet created recently"
        )

        negative.append(
            "Wallet created recently"
        )



    #
    # Token concentration risk
    #

    if (
        data.get("token_concentration") is not None
        and data["token_concentration"] > 80
    ):

        score -= 25

        signals.append(
            "High token concentration risk"
        )

        negative.append(
            "High token concentration risk"
        )



    #
    # Unknown contracts
    #

    if (
        data.get("unknown_contracts") is not None
        and data["unknown_contracts"] > 0
    ):

        score -= 20

        signals.append(
            "Unknown contract interaction"
        )

        negative.append(
            "Unknown contract interaction detected"
        )



    #
    # Raw behavior score
    #

    behavior_score = max(score, 0)



    #
    # Data Quality Adjustment
    #

    data_quality = data.get(
        "data_quality",
        {}
    )


    data_confidence = data_quality.get(
        "confidence",
        1.0
    )


    final_score = round(
        behavior_score * data_confidence
    )



    #
    # Final risk
    #

    if final_score >= 70:

        risk = "LOW"

    elif final_score >= 40:

        risk = "MEDIUM"

    else:

        risk = "HIGH"



    return {

        "trust_score":
            final_score,


        "behavior_score":
            behavior_score,


        "data_quality_confidence":
            data_confidence,


        "risk_level":
            risk,


        "signals":
            signals,


        "explanation": {

            "positive":
                positive,


            "negative":
                negative,


            "unknown":
                unknown

        }

    }
