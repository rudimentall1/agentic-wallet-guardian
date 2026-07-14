from app.tools.scoring import calculate_score
from app.wallet import get_wallet_data


def analyze(address):

    wallet_data = get_wallet_data(address)

    result = calculate_score(
        wallet_data
    )

    result["wallet_metrics"] = wallet_data


    if result["risk_level"] == "LOW":

        if len(result["signals"]) > 0:

            result["recommendation"] = (
                "Low risk wallet. Review detected signals."
            )

        else:

            result["recommendation"] = (
                "Wallet appears safe."
            )


    elif result["risk_level"] == "MEDIUM":

        result["recommendation"] = (
            "Proceed with caution. Review wallet activity."
        )


    else:

        result["recommendation"] = (
            "Avoid interaction until wallet is reviewed."
        )


    return result
