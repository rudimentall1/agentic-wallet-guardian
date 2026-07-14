from app.analyzer import analyze


def analyze_wallet(address):

    result = analyze(address)

    return {
        "agent": "Agentic Wallet Guardian",
        "wallet": address,
        "analysis": result
    }
