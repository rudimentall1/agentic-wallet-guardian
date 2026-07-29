"""
Guardian Risk Fusion Engine v2

Combines multiple security dimensions:

- transaction risk
- wallet trust
- contract risk
- policy risk
- AI agent reputation

Produces unified risk score and explainable decision.
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
    # AI Agent Reputation Layer
    #

    agent = request.get(
        "agent"
    )


    if agent:


        #
        # Unknown agents
        #

        if "unknown" in agent.lower():

            risk_score += 40

            reasons.append(
                "Unknown AI agent reputation"
            )



        #
        # Malicious agents
        #

        if "drainer" in agent.lower():

            risk_score += 60

            reasons.append(
                "Malicious AI agent pattern detected"
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
    # Large transaction
    #

    amount = request.get(
        "amount",
        0
    )


    if amount >= 100:

        risk_score += 20

        reasons.append(
            "Large transaction requires review"
        )



    #
    # Normalize
    #

    if risk_score > 100:

        risk_score = 100



    #
    # Final decision
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
