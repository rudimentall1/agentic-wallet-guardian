"""
Approval Intelligence Layer v2

Explainable ERC20 approval risk analysis.

Current:
- Safe RPC fallback mode
- Explainable risk scoring
- Ready for indexers

Future:
- ERC20 Approval events
- Unlimited allowances
- Spender reputation
- Revoke recommendations
"""


def analyze_approval_risk(data):

    risk_score = 30

    signals = []


    if data.get("available") is False:

        signals.append(
            "Approval history unavailable"
        )

        risk_score += 20


    return {

        "risk_score": risk_score,

        "signals": signals

    }



def get_wallet_approvals(address):


    #
    # Current RPC mode
    #

    approval_data = {

        "available": False,

        "total": None,

        "unlimited": None,

        "high_risk": None

    }


    risk = analyze_approval_risk(
        approval_data
    )


    return {


        "status": "limited",


        "confidence": 0.3,


        "source": "rpc",



        "total":

            approval_data["total"],


        "unlimited":

            approval_data["unlimited"],


        "high_risk":

            approval_data["high_risk"],



        "risk_score":

            risk["risk_score"],



        "signals":

            risk["signals"],



        "recommendation":

            "Approval monitoring recommended",



        "reason":

            (
                "Historical ERC20 Approval events "
                "require indexed blockchain data."
            )

    }
