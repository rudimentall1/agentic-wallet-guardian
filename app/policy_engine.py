"""
Guardian Policy Engine v2

Transaction-level security rules.

Evaluates:
- transaction amount
- contract interaction
- wallet risk signals

Returns:
ALLOW / WARN / BLOCK
"""


def evaluate_policy(
    amount=None,
    contract=None,
    wallet_risk=None,
    action=None
):

    reasons = []

    decision = "ALLOW"

    risk_score = 10


    #
    # High value transaction
    #

    if amount is not None:

        if amount >= 1000:

            reasons.append(
                "Critical transaction value detected"
            )

            decision = "BLOCK"

            risk_score += 70


        elif amount >= 100:

            reasons.append(
                "Large transaction requires review"
            )

            if decision != "BLOCK":
                decision = "WARN"

            risk_score += 30


    #
    # Smart contract interaction
    #

    if contract:

        reasons.append(
            "Smart contract interaction detected"
        )

        if decision == "ALLOW":

            decision = "WARN"

        risk_score += 20



    #
    # Wallet risk
    #

    if wallet_risk is not None:


        if wallet_risk < 30:

            reasons.append(
                "Wallet trust score critically low"
            )

            decision = "BLOCK"

            risk_score += 50



        elif wallet_risk < 50:

            reasons.append(
                "Wallet trust score is low"
            )

            if decision == "ALLOW":

                decision = "WARN"

            risk_score += 25



    return {

        "policy_decision": decision,

        "policy_risk_score": min(
            risk_score,
            100
        ),

        "policy_reasons": reasons

    }
