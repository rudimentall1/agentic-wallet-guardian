from fastapi import FastAPI
from pydantic import BaseModel

from app.agent import analyze_wallet


app = FastAPI(
    title="Agentic Wallet Guardian",
    description="AI agent for crypto wallet trust and risk analysis",
    version="1.0.0"
)


class WalletRequest(BaseModel):
    address: str


@app.get("/")
def home():
    return {
        "agent": "Agentic Wallet Guardian",
        "status": "online",
        "version": "1.0.0"
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
            "wallet risk analysis",
            "trust score calculation",
            "transaction behavior analysis",
            "risk explanation",
            "wallet profiling"
        ]
    }


@app.post("/analyze")
def analyze(request: WalletRequest):

    return analyze_wallet(request.address)


@app.post("/agent")
def agent_request(request: WalletRequest):

    result = analyze_wallet(request.address)

    return {
        "service": "wallet_risk_analysis",
        "agent": "Agentic Wallet Guardian",
        "result": result
    }
