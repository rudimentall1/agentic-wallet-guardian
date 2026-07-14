from web3 import Web3
import time


RPC_URL = "https://ethereum-rpc.publicnode.com"


def get_eth_wallet_data(address):

    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    checksum = w3.to_checksum_address(address)

    balance = w3.eth.get_balance(checksum)

    latest_block = w3.eth.block_number


    return {
        "address": checksum,

        "network": "ethereum",

        "balance_eth": round(
            w3.from_wei(balance, "ether"),
            5
        ),

        "latest_block": latest_block,

        "wallet_age_days": estimate_age(
            latest_block
        ),

        "token_concentration": 50,

        "unknown_contracts": 0,

        "transactions": get_tx_count(
            w3,
            checksum
        )
    }



def get_tx_count(w3, address):

    try:
        count = w3.eth.get_transaction_count(address)

        return count

    except:

        return 0



def estimate_age(block):

    try:
        current_block = block

        blocks_per_day = 7200

        estimated_days = int(
            current_block / blocks_per_day
        )

        return estimated_days

    except:

        return 0
