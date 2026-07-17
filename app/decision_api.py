from pydantic import BaseModel

from app.policy_engine import evaluate_policy


class DecisionRequest(BaseModel):

    agent: str
    action: str
    wallet: str

    target_contract: str | None = None
    token: str | None = None
    amount: float | None = None



def evaluate_action(request: DecisionRequest):


    policy = evaluate_policy(
        amount=request.amount,
        contract=request.target_contract
    )


    return {

        "guardian":
            "Agentic Wallet Guardian",


        "decision":
            policy["policy_decision"],


        "risk_score":
            policy["policy_risk_score"],


        "request": {

            "agent": request.agent,
            "action": request.action,
            "wallet": request.wallet,
            "target_contract": request.target_contract,
            "token": request.token,
            "amount": request.amount

        },


        "policy": {

            "reasons":
                policy["policy_reasons"]

        },


        "guardian_action":

            {
                "ALLOW":
                    "Execution allowed",

                "WARN":
                    "User confirmation required",

                "BLOCK":
                    "Execution blocked"

            }[policy["policy_decision"]]

    }
