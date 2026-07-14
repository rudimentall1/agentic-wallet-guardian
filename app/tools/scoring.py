def calculate_score(data):

    score = 100
    signals = []


    if data["wallet_age_days"] < 7:
        score -= 30
        signals.append(
            "New wallet created recently"
        )


    if data["token_concentration"] > 80:
        score -= 25
        signals.append(
            "High token concentration"
        )


    if data["unknown_contracts"] > 0:
        score -= 20
        signals.append(
            "Unknown contract interaction"
        )


    if score >= 70:
        risk = "LOW"

    elif score >= 40:
        risk = "MEDIUM"

    else:
        risk = "HIGH"


    return {
        "trust_score": max(score,0),
        "risk_level": risk,
        "signals": signals
    }
