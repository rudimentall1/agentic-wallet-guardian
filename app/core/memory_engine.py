"""
Guardian Memory Engine v1

Stores previous Guardian decisions.

Purpose:
- remember wallet interactions
- remember agent behavior
- improve future decisions
"""

import json
import os
from datetime import datetime


MEMORY_FILE = "data/guardian_memory.json"



def _load_memory():

    if not os.path.exists(MEMORY_FILE):

        return []


    try:

        with open(
            MEMORY_FILE,
            "r"
        ) as f:

            return json.load(f)


    except Exception:

        return []



def _save_memory(memory):

    os.makedirs(
        "data",
        exist_ok=True
    )


    with open(
        MEMORY_FILE,
        "w"
    ) as f:

        json.dump(
            memory,
            f,
            indent=4
        )



def save_decision(
    agent,
    wallet,
    action,
    decision,
    risk_score
):

    memory = _load_memory()


    record = {

        "timestamp":
            datetime.utcnow().isoformat(),


        "agent":
            agent,


        "wallet":
            wallet,


        "action":
            action,


        "decision":
            decision,


        "risk_score":
            risk_score

    }


    memory.append(
        record
    )


    _save_memory(
        memory
    )


    return record



def get_wallet_history(wallet):

    memory = _load_memory()


    return [

        item

        for item in memory

        if item.get("wallet") == wallet

    ]



def get_agent_history(agent):

    memory = _load_memory()


    return [

        item

        for item in memory

        if item.get("agent") == agent

    ]



def analyze_memory(
    agent=None,
    wallet=None
):

    result = {

        "previous_interactions": 0,

        "previous_blocks": 0,

        "previous_warnings": 0

    }


    history = []


    if wallet:

        history.extend(
            get_wallet_history(wallet)
        )


    if agent:

        history.extend(
            get_agent_history(agent)
        )



    result["previous_interactions"] = len(
        history
    )


    for item in history:


        if item.get("decision") == "BLOCK":

            result["previous_blocks"] += 1


        elif item.get("decision") == "WARN":

            result["previous_warnings"] += 1



    return result
