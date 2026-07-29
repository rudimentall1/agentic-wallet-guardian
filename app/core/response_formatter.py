"""
Guardian Response Formatter v1

Creates clean Agent Firewall API responses.
"""


from datetime import datetime



def format_guardian_response(result):

    decision = result.get(
        "decision"
    )


    adjusted_risk = result.get(
        "adjusted_risk_score",
        result.get(
            "risk_score",
            0
        )
    )


    reputation = result.get(
        "agent_reputation"
    )


    explanation = result.get(
        "explanation",
        {}
    )


    return {


        "guardian":
            "Agentic Wallet Guardian",


        "timestamp":
            datetime.utcnow().isoformat(),


        "decision":
            decision,


        "risk_score":
            result.get(
                "risk_score"
            ),


        "adjusted_risk_score":
            adjusted_risk,


        "security_level":
            explanation.get(
                "security_level"
            ),


        "message":
            explanation.get(
                "agent_message"
            ),


        "reasons":
            result.get(
                "reasons",
                []
            ),


        "explanation":

            explanation,


        "agent":
            {

                "id":
                    reputation.get(
                        "agent"
                    )
                    if reputation
                    else None,


                "reputation_score":
                    reputation.get(
                        "reputation_score"
                    )
                    if reputation
                    else None,


                "risk_modifier":
                    reputation.get(
                        "risk_modifier"
                    )
                    if reputation
                    else None

            },


        "guardian_action":
            result.get(
                "guardian_action"
            )

    }
