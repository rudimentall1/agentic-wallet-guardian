def calculate_risk(wallet):

    score = 100

    findings = []

    positive = []
    negative = []
    unknown = []


    #
    # TRANSACTIONS
    #

    tx = wallet.get(
        "transactions"
    )


    if tx is None:

        score -= 10

        unknown.append(
            "Transaction data unavailable"
        )


    elif tx < 10:

        score -= 20

        negative.append(
            "Very low wallet activity"
        )

        findings.append(
            "Low transaction activity"
        )


    elif tx > 1000:

        positive.append(
            "Large transaction history"
        )


    #
    # BALANCE
    #

    balance = wallet.get(
        "balance_eth"
    )


    if balance is None:

        unknown.append(
            "Balance unavailable"
        )


    elif balance > 1000:

        positive.append(
            "Large ETH balance detected"
        )


    #
    # APPROVALS
    #

    approvals = wallet.get(
        "approvals",
        {}
    )


    approval_total = approvals.get(
        "total"
    )


    if approval_total is None:

        unknown.append(
            "Approval intelligence limited"
        )


    elif approval_total > 0:

        score -= 20

        negative.append(
            "Token approvals detected"
        )

        findings.append(
            "Existing token approvals detected"
        )


    #
    # TOKEN INTELLIGENCE
    #

    token = wallet.get(
        "token_activity",
        {}
    )


    if token.get(
        "token_quality"
    ) == "LIMITED":

        unknown.append(
            "Token intelligence limited"
        )


    #
    # FINAL
    #

    if score >= 80:

        level = "LOW"

    elif score >= 50:

        level = "MEDIUM"

    else:

        level = "HIGH"


    return {

        "security_score": score,

        "risk_level": level,

        "findings": findings,

        "signals": {

            "positive": positive,

            "negative": negative,

            "unknown": unknown

        }

    }
