def evaluate_policy(
    amount=None,
    contract=None,
    wallet_risk=None
):

    risks = []
    decision = "ALLOW"

    risk_score = 10


    # Large transaction policy

    if amount and amount >= 100:

        risks.append(
            "Large transaction requires review"
        )

        decision = "WARN"
        risk_score += 30


    # Unknown contract policy

    if contract:

        risks.append(
            "Smart contract interaction detected"
        )

        if decision == "ALLOW":
            decision = "WARN"

        risk_score += 20


    # Wallet risk policy

    if wallet_risk:

        if wallet_risk >= 80:

            risks.append(
                "High wallet risk detected"
            )

            decision = "BLOCK"
            risk_score = 90


    return {

        "policy_decision": decision,

        "policy_risk_score": min(
            risk_score,
            100
        ),

        "policy_reasons": risks

    }
