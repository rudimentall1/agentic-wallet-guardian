from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import analyze_wallet
from app.decision_api import DecisionRequest, evaluate_action

from app.core.demo_engine import create_simulation

from app.core.threat_simulation import (
    malicious_agent_attack,
    suspicious_agent_attack,
    safe_agent_action
)



app = FastAPI(
    title="Agentic Wallet Guardian",
    description="AI security decision agent that helps autonomous agents evaluate Web3 wallet and transaction risks.",
    version="2.1.0"
)


class WalletRequest(BaseModel):

    address: str



class SimulationRequest(BaseModel):

    scenario: str



@app.get("/")
def home():

    return {
        "agent": "Agentic Wallet Guardian",
        "status": "online",
        "version": "2.1.0",
        "type": "ASP"
    }



@app.get("/health")
def health():

    return {
        "status": "healthy",
        "agent": "Agentic Wallet Guardian"
    }



@app.get("/capabilities")
def capabilities():

    return {

        "agent": "Agentic Wallet Guardian",

        "type": "ASP",

        "capabilities": [

            "wallet security analysis",
            "transaction risk evaluation",
            "token and contract risk analysis",
            "approval security analysis",
            "explainable AI security decisions",
            "AI agent reputation analysis",
            "autonomous agent threat simulation"

        ]

    }



@app.post("/analyze")
def analyze(request: WalletRequest):

    return analyze_wallet(
        request.address
    )



@app.post("/agent")
def agent_request(request: WalletRequest):

    result = analyze_wallet(
        request.address
    )

    return {

        "service":
            "web3_security_decision",

        "agent":
            "Agentic Wallet Guardian",

        "description":
            "AI security layer for Web3 interactions",

        "result":
            result

    }



@app.post("/decision")
def decision(request: DecisionRequest):

    return evaluate_action(
        request
    )



@app.post("/simulate")
def simulate(request: SimulationRequest):

    scenarios = {

        "malicious_agent":
            malicious_agent_attack,

        "suspicious_agent":
            suspicious_agent_attack,

        "safe_agent":
            safe_agent_action

    }


    scenario = scenarios.get(
        request.scenario
    )


    if not scenario:

        return {

            "error":
                "unknown scenario",

            "available_scenarios":
            [
                "safe_agent",
                "suspicious_agent",
                "malicious_agent"
            ]

        }



    if request.scenario == "malicious_agent":

        seed_malicious_agent()



    attack_request = scenario()


    decision_request = DecisionRequest(
        **attack_request
    )


    result = evaluate_action(
        decision_request
    )


    response = create_simulation(
        attack_request,
        result
    )


    if request.scenario == "malicious_agent":

        response["attack_detected"] = True

        response["threat_type"] = (
            "AI agent transaction abuse"
        )


    elif request.scenario == "suspicious_agent":

        response["attack_detected"] = True

        response["threat_type"] = (
            "Suspicious AI agent behavior"
        )


    else:

        response["attack_detected"] = False

        response["threat_type"] = (
            "No threat detected"
        )


    return response





# ==================================================
# ChainHack Demo Showcase
# ==================================================


@app.get("/demo")
def demo():


    scenarios = [

        {
            "name": "SAFE AGENT",
            "scenario": "safe_agent"
        },

        {
            "name": "UNKNOWN AGENT",
            "scenario": "suspicious_agent"
        },

        {
            "name": "MALICIOUS AGENT",
            "scenario": "malicious_agent"
        }

    ]



    handlers = {

        "safe_agent":
            safe_agent_action,

        "suspicious_agent":
            suspicious_agent_attack,

        "malicious_agent":
            malicious_agent_attack

    }



    results = []



    for item in scenarios:


        scenario_name = item["scenario"]



        # ChainHack demo uses static reputation memory.
        # No writes to guardian_memory.json.



        attack_request = handlers[
            scenario_name
        ]()



        decision_request = DecisionRequest(
            **attack_request
        )



        decision_result = evaluate_action(
            decision_request,
            demo=True
        )



        simulation = create_simulation(
            attack_request,
            decision_result
        )



        results.append({

            "scenario":
                item["name"],


            "decision":
                decision_result.get(
                    "decision"
                ),


            "risk_score":
                decision_result.get(
                    "adjusted_risk_score",
                    decision_result.get(
                        "risk_score",
                        0
                    )
                ),


            "details":
                simulation

        })



    return {

        "demo":
            "Agentic Wallet Guardian Demo",

        "description":
            "AI Security Trust Layer for Autonomous Web3 Agents",

        "security_flow":

        [

            "Agent Request",

            "Wallet Analysis",

            "Policy Engine",

            "Reputation Check",

            "Risk Fusion",

            "Guardian Decision"

        ],


        "results":
            results

    }
