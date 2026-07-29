"""
Guardian Final Decision Engine v1

Produces final ALLOW / WARN / BLOCK
after all risk adjustments.
"""


def calculate_final_decision(
    risk_score
):

    if risk_score >= 80:

        return {

            "decision": "BLOCK",

            "security_level": "CRITICAL",

            "action":
                "Execution blocked"

        }


    elif risk_score >= 40:

        return {

            "decision": "WARN",

            "security_level": "WARNING",

            "action":
                "User confirmation required"

        }


    else:

        return {

            "decision": "ALLOW",

            "security_level": "SAFE",

            "action":
                "Execution allowed"

        }
