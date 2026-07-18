from app.analyzer import analyze
from app.policy_engine import evaluate_policy

from app.core.risk_fusion import calculate_risk_fusion
from app.core.explanation_engine import generate_explanation

from app.core.memory_engine import save_decision
from app.core.reputation_engine import calculate_agent_reputation
from app.core.reputation_adjustment import apply_reputation_adjustment
from app.core.final_decision_engine import calculate_final_decision



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
    # Wallet trust extraction
    #

    wallet_score = None


    if isinstance(wallet_result, dict):

        wallet_score = wallet_result.get(
            "trust_score"
        )



    #
    # Policy Layer
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


    base_risk_score = fusion_result.get(
        "risk_score",
        0
    )


    reasons = fusion_result.get(
        "reasoning",
        []
    )



    #
    # Agent Reputation Layer
    #

    agent_reputation = None


    if request.get("agent"):

        agent_reputation = calculate_agent_reputation(

            request.get(
                "agent"
            )

        )



    #
    # Reputation Adjustment
    #

    adjusted_risk_score = apply_reputation_adjustment(

        base_risk_score,

        agent_reputation

    )


    if agent_reputation:

        if agent_reputation.get("risk_modifier", 0) > 0:

            reasons.append(
                "Agent reputation risk detected"
            )


    #
    # Final Guardian Decision
    #

    final_decision = calculate_final_decision(

        adjusted_risk_score

    )


    decision = final_decision.get(
        "decision"
    )



    #
    # Memory Layer
    # Save final decision
    #

    save_decision(

        agent=request.get(
            "agent"
        ),

        wallet=request.get(
            "wallet"
        ),

        action=request.get(
            "action"
        ),

        decision=decision,

        risk_score=adjusted_risk_score

    )



    #
    # Explanation Layer
    #

    explanation = generate_explanation(

        decision,

        adjusted_risk_score,

        reasons

    )



    #
    # Guardian action
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
            base_risk_score,


        "adjusted_risk_score":
            adjusted_risk_score,


        "reasons":
            reasons,


        "explanation":
            explanation,


        "final_guardian_decision":
            final_decision,


        "wallet_analysis":
            wallet_result,


        "policy":
            policy_result,


        "risk_fusion":
            fusion_result,


        "guardian_action":
            actions.get(
                decision
            ),


        "agent_reputation":
            agent_reputation,


        "request":
            request

    }
