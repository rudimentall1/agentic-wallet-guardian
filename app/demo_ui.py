from fastapi.responses import HTMLResponse


def demo_ui_page():

    html = """
<!DOCTYPE html>
<html>

<head>

<title>Agentic Wallet Guardian v2</title>

<style>

body {
    font-family: Arial, sans-serif;
    background: #0b1020;
    color: white;
    padding: 40px;
}


h1 {
    text-align: center;
}


.subtitle {
    text-align:center;
    color:#94a3b8;
}


.container {

    display:flex;
    gap:20px;
    justify-content:center;
    flex-wrap:wrap;
    margin-top:40px;

}


.card {

    background:#151c35;
    border-radius:15px;
    padding:25px;
    width:300px;

}


.safe {
    border:2px solid #22c55e;
}


.warn {
    border:2px solid #eab308;
}


.danger {
    border:2px solid #ef4444;
}


.decision {

    font-size:28px;
    font-weight:bold;

}


.score {

    font-size:22px;

}


.reason {

    color:#cbd5e1;

}


.pipeline {

    margin:50px auto;
    max-width:600px;
    background:#111827;
    padding:25px;
    border-radius:15px;
    text-align:center;

}


.step {

    padding:10px;
    font-size:18px;

}


</style>

</head>


<body>


<h1>
Agentic Wallet Guardian v2
</h1>


<div class="subtitle">
AI Security Layer for Autonomous Web3 Agents
</div>



<div class="pipeline">

<h2>Security Pipeline</h2>

<div class="step">
🤖 Agent Request
</div>

<div class="step">
↓
</div>

<div class="step">
🔍 Wallet Analysis
</div>

<div class="step">
↓
</div>

<div class="step">
📜 Policy Engine
</div>

<div class="step">
↓
</div>

<div class="step">
⭐ Agent Reputation
</div>

<div class="step">
↓
</div>

<div class="step">
⚡ Risk Fusion Engine
</div>

<div class="step">
↓
</div>

<div class="step">
🛡 Guardian Decision
</div>

</div>



<div id="results" class="container">

Loading Guardian analysis...

</div>



<script>


function cardClass(decision){

    if(decision === "ALLOW"){
        return "safe";
    }

    if(decision === "WARN"){
        return "warn";
    }

    return "danger";

}



function render(data){

    let html = "";


    data.results.forEach(item => {


        let details = item.details;


        let explanation =
            details.security_explanation;


        html += `

        <div class="card ${cardClass(item.decision)}">

            <h2>${item.scenario}</h2>


            <p class="score">
                Risk Score:
                ${item.risk_score}/100
            </p>


            <p class="decision">
                ${item.decision}
            </p>


            <p class="reason">
                ${explanation.explanation}
            </p>


            <p>
                Threat:
                ${details.threat_type}
            </p>


            <p>
                Factors:
                ${explanation.risk_factors.join(", ")}
            </p>


        </div>

        `;


    });


    document.getElementById(
        "results"
    ).innerHTML = html;

}



fetch("/demo")

.then(response => response.json())

.then(data => render(data))


.catch(error => {

    document.getElementById(
        "results"
    ).innerHTML =
    "Guardian connection error";

});


</script>


</body>

</html>
"""

    return HTMLResponse(html)
