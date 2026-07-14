from app.tools.ethereum import get_eth_wallet_data


def get_wallet_data(address):

    try:

        return get_eth_wallet_data(address)


    except Exception as e:

        return {

            "address": address,

            "network": "ethereum",

            "error": str(e),

            "wallet_age_days": 0,

            "token_concentration": 0,

            "unknown_contracts": 0,

            "transactions": 0

        }
