"""
Guardian Demo Engine v2

Creates human-readable
security simulation output
for ChainHack presentation.
"""


def create_simulation(
    request,
    decision_result
):

    decision = decision_result.get(
        "decision"
    )

    risk_score = decision_result.get(
        "adjusted_risk_score",
        decision_result.get(
            "risk_score",
            0
        )
    )

    explanation = decision_result.get(
        "explanation",
        {}
    )

    wallet = request.get(
        "wallet"
    )

    agent = request.get(
        "agent"
    )

    action = request.get(
        "action"
    )

    amount = request.get(
        "amount"
    )


    threat_type = None

    if agent == "drainer-agent-777":

        threat_type = "AI agent transaction abuse"


    elif agent == "unknown-agent-x":

        threat_type = "Suspicious AI agent behavior"


    else:

        threat_type = "No threat detected"



    attack_detected = (
        decision in [
            "WARN",
            "BLOCK"
        ]
    )


    return {

        "simulation":
            "complete",


        "attack_detected":
            attack_detected,


        "threat_type":
            threat_type,


        "agent_request": {

            "agent":
                agent,

            "action":
                action,

            "amount":
                amount,

            "wallet":
                wallet

        },


        "guardian_analysis": {

            "risk_score":
                risk_score,

            "decision":
                decision

        },


        "security_explanation":
            explanation,


        "final_message":
            explanation.get(
                "agent_message"
            )

    }
