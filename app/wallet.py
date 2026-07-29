from app.tools.ethereum import get_eth_wallet_data
from app.tools.approvals import get_wallet_approvals
from app.tools.tokens import get_token_intelligence
from app.tools.contracts import get_contract_intelligence



def get_wallet_data(address):

    try:

        #
        # Core Wallet Intelligence
        #

        data = get_eth_wallet_data(address)



        #
        # Approval Intelligence Agent
        #

        approvals = get_wallet_approvals(
            address
        )

        data["approvals"] = approvals



        #
        # Token Intelligence Agent
        #

        tokens = get_token_intelligence(
            address
        )

        data["token_intelligence"] = tokens



        #
        # Contract Intelligence Agent
        #

        contracts = get_contract_intelligence(
            address,
            data
        )

        data["contract_intelligence"] = contracts



        #
        # Data Quality Calculation
        #

        wallet_ok = (
            data.get("balance_eth") is not None
        )


        transactions_ok = (
            data.get("transactions") is not None
        )


        tokens_ok = (
            tokens.get("status")
            !=
            "limited"
        )


        contracts_ok = (
            contracts.get("status")
            !=
            "limited"
        )



        confidence_points = [

            wallet_ok,

            transactions_ok,

            tokens_ok,

            contracts_ok

        ]



        confidence = round(

            sum(confidence_points)
            /
            len(confidence_points),

            2

        )



        warnings = []



        if not tokens_ok:

            warnings.append(
                "Token intelligence limited"
            )



        if approvals.get(
            "status"
        ) == "limited":

            warnings.append(
                "Approval intelligence limited"
            )



        if contracts.get(
            "status"
        ) == "limited":

            warnings.append(
                "Contract intelligence limited"
            )



        #
        # Unified Data Quality
        #

        data["data_quality"] = {


            "rpc_status":

                "healthy"
                if wallet_ok
                else
                "degraded",



            "confidence":

                confidence,



            "layers": {


                "wallet_core": {

                    "status":

                        "available"
                        if wallet_ok
                        else
                        "failed",

                    "confidence":

                        1.0
                        if wallet_ok
                        else
                        0.0

                },



                "transactions": {

                    "status":

                        "available"
                        if transactions_ok
                        else
                        "failed",

                    "confidence":

                        1.0
                        if transactions_ok
                        else
                        0.0

                },



                "tokens": {

                    "status":

                        "available"
                        if tokens_ok
                        else
                        "limited",

                    "confidence":

                        tokens.get(
                            "confidence",
                            0.0
                        )

                },



                "contracts": {

                    "status":

                        "available"
                        if contracts_ok
                        else
                        "limited",

                    "confidence":

                        contracts.get(
                            "confidence",
                            0.0
                        )

                }

            },


            "warnings":

                warnings

        }



        return data



    except Exception as e:


        return {


            "address":

                address,


            "network":

                "ethereum",



            "error":

                str(e),



            "data_quality": {


                "rpc_status":

                    "failed",


                "confidence":

                    0.2,


                "warnings":[

                    "Wallet data unavailable"

                ]

            }

        }
