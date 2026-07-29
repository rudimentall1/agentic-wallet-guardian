"""
Decision Agent

Final reasoning layer.

Combines:
- Risk Engine
- Security Intelligence
- Data Quality
- Approval Intelligence

Produces final wallet action.
"""


def make_final_decision(
    wallet_data,
    risk_engine,
    security
):

    confidence = wallet_data.get(
        "data_quality",
        {}
    ).get(
        "confidence",
        0
    )


    reasons = []


    #
    # Risk Engine decision
    #

    risk_decision = risk_engine.get(
        "decision",
        "REVIEW"
    )


    risk_level = risk_engine.get(
        "risk_level",
        "UNKNOWN"
    )


    #
    # Collect reasoning
    #

    for item in risk_engine.get(
        "signals",
        {}
    ).get(
        "positive",
        []
    ):

        reasons.append(item)


    for item in risk_engine.get(
        "signals",
        {}
    ).get(
        "unknown",
        []
    ):

        reasons.append(item)



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

        reasons.append(
            "Approval data unavailable"
        )


    #
    # Final decision
    #

    if risk_decision == "ALLOW":


        if confidence >= 0.8:

            final_decision = (
                "ALLOW_WITH_LIMITATIONS"
            )

            action = (
                "INTERACT_WITH_CAUTION"
            )


        else:

            final_decision = (
                "REVIEW"
            )

            action = (
                "LIMITED_DATA_REVIEW"
            )


    elif risk_decision == "REVIEW":


        final_decision = (
            "REVIEW"
        )

        action = (
            "INVESTIGATE_BEFORE_INTERACTION"
        )


    else:


        final_decision = (
            "BLOCK"
        )

        action = (
            "DO_NOT_INTERACT"
        )


    return {


        "final_decision": final_decision,


        "risk_level": risk_level,


        "confidence": round(
            confidence,
            2
        ),


        "recommended_action": action,


        "reasoning": reasons,


        "security_summary": {

            "risk": security.get(
                "risk"
            ),

            "findings": security.get(
                "findings",
                []
            )

        }

    }
