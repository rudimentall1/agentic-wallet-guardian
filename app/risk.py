def calculate_risk(wallet):

    score = 100

    findings = []


    if wallet["approvals"] > 0:
        score -= 20
        findings.append(
            "Existing token approvals detected"
        )


    if wallet["transactions"] < 10:
        score -= 10
        findings.append(
            "Low wallet activity"
        )


    if score >= 80:
        level = "LOW"
    elif score >= 50:
        level = "MEDIUM"
    else:
        level = "HIGH"


    return {
        "score": score,
        "level": level,
        "findings": findings
    }
