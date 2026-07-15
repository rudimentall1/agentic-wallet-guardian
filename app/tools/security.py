def check_address_risk(address, wallet_data):

    findings = []

    positive = []
    negative = []
    unknown = []


    security_score = 100



    #
    # Basic data
    #

    transactions = wallet_data.get(
        "transactions"
    )


    balance = wallet_data.get(
        "balance_eth"
    )


    age = wallet_data.get(
        "wallet_age_days"
    )



    #
    # Transaction analysis
    #

    if transactions is not None:


        if transactions < 5:

            security_score -= 20

            findings.append(
                "Very low wallet activity"
            )

            negative.append(
                "Very low wallet activity"
            )


        elif transactions > 1000:


            positive.append(
                "Large transaction history"
            )


    else:

        security_score -= 10

        findings.append(
            "Transaction data unavailable"
        )

        unknown.append(
            "Transaction data unavailable"
        )



    #
    # Balance analysis
    #

    if balance is not None:


        if balance > 1000:


            positive.append(
                "Large ETH balance detected"
            )


    else:

        security_score -= 10

        findings.append(
            "Balance data unavailable"
        )

        unknown.append(
            "Balance unavailable"
        )



    #
    # Wallet age
    #

    if age is not None:


        if age < 7:


            security_score -= 30

            findings.append(
                "New wallet created recently"
            )

            negative.append(
                "New wallet"
            )


    else:

        unknown.append(
            "Wallet age unavailable"
        )



    #
    # Token intelligence
    #

    token_activity = wallet_data.get(
        "token_activity"
    )


    if token_activity:


        token_quality = token_activity.get(
            "token_quality"
        )


        if token_quality == "LIMITED":


            security_score -= 10


            findings.append(
                "Limited token intelligence"
            )


            unknown.append(
                "Token analysis incomplete"
            )


        elif token_quality == "FAILED":


            security_score -= 20


            findings.append(
                "Token intelligence unavailable"
            )


            unknown.append(
                "Token analysis failed"
            )



    #
    # Contract analysis
    #

    contract_analysis = wallet_data.get(
        "contract_analysis"
    )


    if contract_analysis:


        unknown_contracts = contract_analysis.get(
            "unknown_contracts",
            0
        )


        if unknown_contracts > 0:


            security_score -= 25


            findings.append(
                "Unknown contract interactions detected"
            )


            negative.append(
                "Unknown contracts"
            )



    #
    # Final security level
    #

    security_score = max(
        security_score,
        0
    )


    if security_score >= 80:

        risk = "LOW"


    elif security_score >= 50:

        risk = "MEDIUM"


    else:

        risk = "HIGH"



    #
    # Threat level
    #

    if len(negative) > 0:

        threat_level = "ELEVATED"

    elif len(unknown) > 0:

        threat_level = "LIMITED_DATA"

    else:

        threat_level = "LOW"



    return {


        "security_score":
            security_score,


        "risk":
            risk,


        "threat_level":
            threat_level,


        "reason":
            "Security intelligence analysis completed",


        "findings":
            findings,


        "signals":{

            "positive":
                positive,


            "negative":
                negative,


            "unknown":
                unknown

        }

    }
