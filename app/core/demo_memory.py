"""
Guardian Demo Memory

Static reputation memory for ChainHack showcase.
Does not modify real agent memory.
"""


DEMO_MEMORY = {


    "safe_agent": {

        "previous_interactions": 10,
        "previous_blocks": 0,
        "previous_warnings": 0

    },


    "suspicious_agent": {

        "previous_interactions": 3,
        "previous_blocks": 0,
        "previous_warnings": 2

    },


    "malicious_agent": {

        "previous_interactions": 15,
        "previous_blocks": 15,
        "previous_warnings": 0

    }

}



def get_demo_memory(agent):


    return DEMO_MEMORY.get(

        agent,

        {

            "previous_interactions": 0,
            "previous_blocks": 0,
            "previous_warnings": 0

        }

    )
