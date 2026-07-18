"""
Guardian Explanation Engine v1

Converts technical security signals
into human and AI-agent readable reasoning.

Purpose:

Decision
    +
Risk Score
    +
Reasons

become:

Security explanation
Recommendation
Agent message
"""


def generate_explanation(
    decision,
    risk_score,
    reasons
):

    #
    # Security level
    #

    if risk_score >= 80:

        security_level = "CRITICAL"


    elif risk_score >= 40:

        security_level = "WARNING"


    else:

        security_level = "SAFE"



    #
    # Default reasoning
    #

    if not reasons:

        reasons = [
            "No significant security risks detected"
        ]



    #
    # Decision explanation
    #

    if decision == "ALLOW":

        explanation = (
            "Transaction passed Guardian security checks "
            "and can be executed."
        )

        agent_message = (
            "Action approved. "
            "Risk level is acceptable."
        )

        recommendation = (
            "Proceed with execution."
        )



    elif decision == "WARN":

        explanation = (
            "Transaction requires additional review "
            "because potential risk factors were detected."
        )

        agent_message = (
            "I recommend user confirmation "
            "before executing this action."
        )

        recommendation = (
            "Request human approval."
        )



    else:

        explanation = (
            "Transaction was blocked because "
            "security policies identified critical risk."
        )

        agent_message = (
            "I cannot safely execute this action "
            "without additional authorization."
        )

        recommendation = (
            "Do not execute until risk is resolved."
        )



    return {

        "security_level":
            security_level,


        "explanation":
            explanation,


        "agent_message":
            agent_message,


        "recommendation":
            recommendation,


        "risk_factors":
            reasons

    }
