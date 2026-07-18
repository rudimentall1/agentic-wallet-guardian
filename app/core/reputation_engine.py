"""
Guardian Agent Reputation Engine v1

Calculates trust score for autonomous agents
based on previous Guardian decisions.
"""


from app.core.memory_engine import analyze_memory



def calculate_agent_reputation(agent):

    memory = analyze_memory(
        agent=agent
    )


    reputation = 100


    reputation -= (
        memory["previous_warnings"] * 5
    )


    reputation -= (
        memory["previous_blocks"] * 20
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
