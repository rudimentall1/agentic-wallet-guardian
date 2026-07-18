from app.analyzer import analyze
from app.policy_engine import evaluate_policy
from app.core.risk_fusion import calculate_risk_fusion


def evaluate_action(request):

    wallet_result = None


    #
    # Wallet Intelligence
    #

    if request.get("wallet"):

        try:

            wallet_result = analyze(
                request["wallet"]
            )

        except Exception as e:

            wallet_result = {
                "error": str(e)
            }



    #
    # Wallet trust score
    #

    wallet_score = None


    if isinstance(wallet_result, dict):

        wallet_score = wallet_result.get(
            "trust_score"
        )



    #
    # Policy Engine
    #

    policy_result = evaluate_policy(

        amount=request.get(
            "amount"
        ),

        contract=request.get(
            "target_contract"
        ),

        wallet_risk=wallet_score,

        action=request.get(
            "action"
        )

    )



    #
    # Risk Fusion Layer
    #

    fusion_result = calculate_risk_fusion(

        policy_result,

        wallet_result,

        request

    )


    decision = fusion_result.get(
        "decision",
        "ALLOW"
    )


    risk_score = fusion_result.get(
        "risk_score",
        0
    )


    reasons = fusion_result.get(
        "reasoning",
        []
    )



    #
    # Guardian Action
    #

    actions = {

        "ALLOW":
            "Execution allowed",

        "WARN":
            "User confirmation required",

        "BLOCK":
            "Execution blocked"

    }



    return {

        "guardian":
            "Agentic Wallet Guardian",


        "decision":
            decision,


        "risk_score":
            min(
                risk_score,
                100
            ),


        "reasons":
            reasons,


        "wallet_analysis":
            wallet_result,


        "fusion":

            fusion_result,


        "guardian_action":

            actions.get(
                decision
            )

    }
