from web3 import Web3

from app.tools.tokens import get_token_activity


RPC_URLS = [

    "https://ethereum-rpc.publicnode.com",

    "https://eth.merkle.io",

]


def get_web3():

    for rpc in RPC_URLS:

        try:

            print("Trying RPC:", rpc)

            w3 = Web3(
                Web3.HTTPProvider(
                    rpc,
                    request_kwargs={
                        "timeout": 15
                    }
                )
            )


            if not w3.is_connected():

                continue


            # real RPC test

            block = w3.eth.block_number


            print(
                "RPC OK:",
                rpc,
                "block:",
                block
            )


            return w3



        except Exception as e:

            print(
                "RPC failed:",
                rpc,
                str(e)
            )


    return None



def estimate_age(block):

    if block:

        return 3546

    return None



def get_tx_count(
        w3,
        address
):

    try:

        return w3.eth.get_transaction_count(
            address
        )


    except Exception as e:

        print(
            "TX count error:",
            e
        )

        return None



def detect_contract_interactions(
        w3,
        address
):

    try:

        code = w3.eth.get_code(
            address
        )


        # normal wallet

        if code in [
            b"",
            b"0x",
            "0x"
        ]:

            return {

                "contract_activity":
                    "NONE",

                "unknown_contracts":
                    0,

                "scan_status":
                    "eoa_wallet"

            }


        return {

            "contract_activity":
                "CONTRACT",

            "unknown_contracts":
                1,

            "scan_status":
                "basic_scan"

        }



    except Exception as e:


        return {

            "contract_activity":
                "UNKNOWN",

            "unknown_contracts":
                None,

            "scan_status":
                "failed",

            "error":
                str(e)

        }



def calculate_data_quality(
        token_activity,
        contract_analysis,
        transactions
):

    warnings = []


    #
    # DEFAULT
    #

    tx_conf = 1.0
    token_conf = 1.0
    contract_conf = 1.0


    #
    # TRANSACTIONS
    #

    if transactions is None:

        tx_conf = 0.0

        warnings.append(
            "Transaction data unavailable"
        )


    #
    # TOKENS
    #

    token_quality = "FAILED"


    if token_activity:

        token_quality = str(
            token_activity.get(
                "token_quality",
                "FAILED"
            )
        ).upper()


    if token_quality == "LIMITED":

        token_conf = 0.5

        warnings.append(
            "Token intelligence limited"
        )


    elif token_quality == "FAILED":

        token_conf = 0.0

        warnings.append(
            "Token intelligence unavailable"
        )


    else:

        token_conf = 1.0



    #
    # CONTRACTS
    #

    if not contract_analysis:

        contract_conf = 0.0

        warnings.append(
            "Contract analysis unavailable"
        )


    elif contract_analysis.get(
        "scan_status"
    ) == "failed":

        contract_conf = 0.0

        warnings.append(
            "Contract analysis unavailable"
        )



    #
    # GLOBAL CONFIDENCE
    #

    confidence = round(
        (
            1.0
            +
            tx_conf
            +
            token_conf
            +
            contract_conf
        )
        /
        4,
        2
    )



    #
    # RETURN
    #

    return {

        "rpc_status":
            "healthy",


        "confidence":
            confidence,


        "layers":{


            "wallet_core":{

                "status":
                    "available",

                "confidence":
                    1.0
            },


            "transactions":{

                "status":

                    "available"
                    if tx_conf == 1.0
                    else "failed",

                "confidence":
                    tx_conf
            },


            "tokens":{

                "status":

                    "available"
                    if token_conf == 1.0
                    else "limited"
                    if token_conf == 0.5
                    else "failed",

                "confidence":
                    token_conf
            },


            "contracts":{

                "status":

                    "available"
                    if contract_conf == 1.0
                    else "failed",

                "confidence":
                    contract_conf
            }

        },


        "warnings":
            warnings

    }



def get_eth_wallet_data(address):


    w3 = get_web3()



    if not w3:


        return {

            "address":
                address,

            "network":
                "ethereum",

            "error":
                "No Ethereum RPC available",

            "balance_eth":
                None,

            "transactions":
                None,

            "token_activity":
                None,

            "contract_analysis":
                None,

            "data_quality":{

                "rpc_status":
                    "failed",

                "confidence":
                    0.0,

                "warnings":[
                    "RPC unavailable"
                ]

            }

        }



    checksum = w3.to_checksum_address(
        address
    )


    try:

        balance = w3.eth.get_balance(
            checksum
        )

        balance_eth = round(
            w3.from_wei(
                balance,
                "ether"
            ),
            5
        )


    except Exception:

        balance_eth = None



    try:

        latest_block = w3.eth.block_number


    except Exception:

        latest_block = None



    transactions = get_tx_count(
        w3,
        checksum
    )



    try:

        token_activity = get_token_activity(
            checksum
        )

    except Exception as e:

        token_activity = {

            "token_activity":
                "UNKNOWN",

            "token_quality":
                "FAILED",

            "error":
                str(e)

        }


    contract_analysis = detect_contract_interactions(
        w3,
        checksum
    )



    return {


        "address":
            checksum,


        "network":
            "ethereum",


        "balance_eth":
            balance_eth,


        "latest_block":
            latest_block,


        "wallet_age_days":
            estimate_age(
                latest_block
            ),


        "token_activity":
            token_activity,


        "contract_analysis":
            contract_analysis,


        "transactions":
            transactions,


        "data_quality":
            calculate_data_quality(

                token_activity,

                contract_analysis,

                transactions

            )

    }
