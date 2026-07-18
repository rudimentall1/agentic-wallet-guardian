"""
Guardian Threat Simulation Engine v2

Creates realistic AI agent scenarios
for ChainHack demonstration.

Scenarios:

safe_agent
    trusted autonomous agent

suspicious_agent
    unknown agent with risky behavior

malicious_agent
    malicious AI agent attack
"""


def malicious_agent_attack():

    return {

        "agent":
            "drainer-agent-777",

        "wallet":
            "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",

        "action":
            "transfer",

        "amount":
            500,

        "target_contract":
            "0xBAD0000000000000000000000000000000000001"

    }



def suspicious_agent_attack():

    return {

        "agent":
            "unknown-agent-x",

        "wallet":
            "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",

        "action":
            "transfer",

        "amount":
            50,

        "target_contract":
            None

    }



def safe_agent_action():

    return {

        "agent":
            "trusted-trading-agent",

        "wallet":
            "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",

        "action":
            "swap",

        "amount":
            5,

        "target_contract":
            None

    }
