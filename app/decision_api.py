from pydantic import BaseModel
from typing import Optional

from app.core.guardian_engine import evaluate_action as guardian_evaluate
from app.core.response_formatter import format_guardian_response


class DecisionRequest(BaseModel):

    wallet: Optional[str] = None

    agent: Optional[str] = None

    action: Optional[str] = None

    amount: Optional[float] = None

    target_contract: Optional[str] = None

    token: Optional[str] = None



def evaluate_action(
    request: DecisionRequest,
    demo: bool = False
):

    request_dict = request.model_dump()


    if demo:
        request_dict["demo_mode"] = True


    result = guardian_evaluate(
        request_dict
    )


    return format_guardian_response(
        result
    )
