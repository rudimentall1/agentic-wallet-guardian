"""
Guardian Demo Scenarios v2

Creates fake attack history
for ChainHack demonstrations.
"""

from app.core.memory_engine import save_decision


WALLET = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"



def seed_suspicious_agent():

    agent = "unknown-agent-x"


    history = [

        {
            "decision": "WARN",
            "risk_score": 70
        },

        {
            "decision": "WARN",
            "risk_score": 75
        },

        {
            "decision": "WARN",
            "risk_score": 80
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

        "history_added": len(history)

    }





def seed_malicious_agent():

    agent = "drainer-agent-777"


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

        "history_added": len(history)

    }
