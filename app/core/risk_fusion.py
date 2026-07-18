"""
Guardian Risk Fusion Engine v1

Combines multiple security dimensions:

- transaction risk
- wallet trust
- contract risk
- policy risk

Produces unified risk score and reasoning.
"""


def calculate_risk_fusion(
    policy_result,
    wallet_result,
    request
):

    risk_score = 0

    reasons = []


    #
    # Policy risk
    #

    policy_risk = policy_result.get(
        "policy_risk_score",
        0
    )

    risk_score += policy_risk


    reasons.extend(
        policy_result.get(
            "policy_reasons",
            []
        )
    )


    #
    # Wallet trust
    #

    wallet_trust = None


    if isinstance(wallet_result, dict):

        wallet_trust = wallet_result.get(
            "trust_score"
        )


    if wallet_trust is not None:


        if wallet_trust < 30:

            risk_score += 50

            reasons.append(
                "Wallet trust critically low"
            )


        elif wallet_trust < 50:

            risk_score += 25

            reasons.append(
                "Wallet trust requires review"
            )


    #
    # Contract interaction
    #

    contract = request.get(
        "target_contract"
    )


    if contract:

        risk_score += 20

        reasons.append(
            "External contract interaction"
        )


    #
    # Normalize
    #

    risk_score = min(
        risk_score,
        100
    )


    #
    # Decision
    #

    if risk_score >= 80:

        decision = "BLOCK"


    elif risk_score >= 40:

        decision = "WARN"


    else:

        decision = "ALLOW"



    return {

        "risk_score":
            risk_score,


        "decision":
            decision,


        "reasoning":
            list(set(reasons))

    }
