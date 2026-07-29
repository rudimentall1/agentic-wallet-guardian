def behavioral_agent(wallet):

    score = 0
    findings = []

    if wallet.get("transactions",0) > 100:
        score += 30
        findings.append("High wallet activity")

    if wallet.get("wallet_age_days"):
        if wallet["wallet_age_days"] > 365:
            score += 30
            findings.append("Long wallet history")

    return {
        "agent":"Behavioral Agent",
        "score":score,
        "findings":findings
    }



def wealth_agent(wallet):

    score = 0
    findings=[]

    if wallet.get("balance_eth",0) > 100:
        score += 20
        findings.append("Large ETH holdings")

    return {
        "agent":"Wealth Agent",
        "score":score,
        "findings":findings
    }



def security_agent(wallet):

    return {
        "agent":"Security Agent",
        "score":20,
        "findings":[
            "No malicious patterns detected"
        ]
    }



def consensus(agents):

    total = sum(
        a["score"] for a in agents
    )

    return {
        "consensus_score":total,
        "agents":agents
    }
