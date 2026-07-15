def generate_reasoning(result):

    signals = result.get("signals", [])

    if result["risk_level"] == "LOW":

        return {
            "agent": "Decision Agent",
            "thought": "Wallet behavior appears stable based on available signals.",
            "factors": signals,
            "action": "ALLOW"
        }

    elif result["risk_level"] == "MEDIUM":

        return {
            "agent": "Decision Agent",
            "thought": "Wallet requires additional verification before interaction.",
            "factors": signals,
            "action": "REVIEW"
        }

    else:

        return {
            "agent": "Decision Agent",
            "thought": "Wallet shows dangerous behavior patterns.",
            "factors": signals,
            "action": "BLOCK"
        }
