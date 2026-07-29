"""
Guardian Demo Scenarios v2

Creates deterministic demo history
for ChainHack demonstrations.
"""

from app.core.memory_engine import (
    save_decision,
    get_agent_history,
)


WALLET = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"


def seed_suspicious_agent():

    agent = "unknown-agent-x"

    if get_agent_history(agent):
        return {
            "agent": agent,
            "history_added": 0,
            "already_seeded": True
        }

    history = [
        {
            "decision": "WARN",
            "risk_score": 55
        },
        {
            "decision": "WARN",
            "risk_score": 60
        }
    ]

    for item in history:

        save_decision(
            agent=agent,
            wallet=WALLET,
            action="transfer",
            decision=item["decision"],
            risk_score=item["risk_score"]
        )

    return {
        "agent": agent,
        "history_added": len(history),
        "already_seeded": False
    }


def seed_malicious_agent():

    agent = "drainer-agent-777"

    if get_agent_history(agent):
        return {
            "agent": agent,
            "history_added": 0,
            "already_seeded": True
        }

    history = [
        {
            "decision": "WARN",
            "risk_score": 40
        },
        {
            "decision": "WARN",
            "risk_score": 50
        },
        {
            "decision": "WARN",
            "risk_score": 60
        },
        {
            "decision": "BLOCK",
            "risk_score": 90
        },
        {
            "decision": "BLOCK",
            "risk_score": 95
        }
    ]

    for item in history:

        save_decision(
            agent=agent,
            wallet=WALLET,
            action="transfer",
            decision=item["decision"],
            risk_score=item["risk_score"]
        )

    return {
        "agent": agent,
        "history_added": len(history),
        "already_seeded": False
    }
