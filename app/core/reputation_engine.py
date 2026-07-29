"""
Guardian Agent Reputation Engine v2

Calculates trust score for autonomous AI agents
based on previous Guardian decisions.
"""

from app.core.memory_engine import analyze_memory
from app.core.demo_memory import get_demo_memory


def calculate_agent_reputation(
    agent,
    demo=False
):

    if demo:

        memory = get_demo_memory(
            agent
        )

    else:

        memory = analyze_memory(
            agent=agent
        )


    reputation = 100


    reputation -= (
        memory["previous_warnings"] * 10
    )


    reputation -= (
        memory["previous_blocks"] * 25
    )


    if reputation < 0:
        reputation = 0


    risk_modifier = 100 - reputation


    return {

        "agent": agent,

        "reputation_score":
            reputation,

        "risk_modifier":
            risk_modifier,

        "history":
            memory

    }
