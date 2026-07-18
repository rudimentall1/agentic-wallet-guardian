from fastapi.responses import HTMLResponse


def demo_ui_page():

    html = """
<!DOCTYPE html>
<html>

<head>

<title>Agentic Wallet Guardian v2</title>

<style>

body {
    margin:0;
    padding:20px;
    background:#070b14;
    color:#e5e7eb;
    font-family:Arial, sans-serif;
}


.container {
    max-width:1000px;
    margin:auto;
}


.header {
    text-align:center;
    margin-bottom:35px;
}


h1 {
    font-size:22px;
    font-weight:600;
    margin:0;
}


.subtitle {
    color:#94a3b8;
    margin-top:10px;
}


.panel {

    background:#111827;
    border:1px solid #1e293b;
    border-radius:16px;
    padding:16px;
    margin-bottom:12px;

}


.title {

    color:#94a3b8;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:1px;
    margin-bottom:20px;

}


input {

    width:75%;
    background:#0b1220;
    border:1px solid #334155;
    color:white;
    padding:10px;
    border-radius:8px;
    font-size:13px;

}


button {

    background:#2563eb;
    border:0;
    color:white;
    padding:10px 18px;
    border-radius:8px;
    cursor:pointer;

}


.grid {

    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:20px;

}


.metric {

    background:#0b1220;
    padding:14px;
    border-radius:10px;

}


.label {

    color:#94a3b8;
    font-size:13px;

}


.value {

    font-size:20px;
    margin-top:6px;
    font-weight:600;

}


.low {

    color:#22c55e;

}


.result {

    line-height:1.8;
    color:#cbd5e1;

}


.signal {

    margin-top:8px;

}


</style>

</head>


<body>


<div class="container">


<div class="header">

<h1>
Agentic Wallet Guardian v2
</h1>

<div class="subtitle">
AI Security Intelligence Layer for Autonomous Web3 Agents
</div>

</div>



<div class="panel">

<div class="title">
Wallet Analysis
</div>


<input id="wallet"
value="0x742d35Cc6634C0532925a3b844Bc454e4438f44e">


<button onclick="analyze()">
Analyze
</button>


</div>




<div id="output">


<div class="panel">

<div class="title">
Security Assessment
</div>

<div class="result">
Waiting for wallet analysis...
</div>

</div>


</div>



</div>




<script>

async function analyze(){


const address =
document.getElementById("wallet").value;


const response =
await fetch("/agent",
{

method:"POST",

headers:
{
"Content-Type":"application/json"
},

body:
JSON.stringify(
{
address:address
}
)

});


const data =
await response.json();


const a =
data.result.analysis;



document.getElementById("output").innerHTML = `


<div class="panel">

<div class="title">
Security Decision
</div>

<div class="grid">


<div class="metric">

<div class="label">
Trust Score
</div>

<div class="value">
${a.trust_score}/100
</div>

</div>


<div class="metric">

<div class="label">
Risk Level
</div>

<div class="value low">
${a.risk_level}
</div>

</div>


<div class="metric">

<div class="label">
Decision
</div>

<div class="value">
${a.final_decision.final_decision.replaceAll("_"," ")}
</div>

</div>


<div class="metric">

<div class="label">
Confidence
</div>

<div class="value">
${a.final_decision.confidence*100}%
</div>

</div>


</div>

</div>



<div class="panel">

<div class="title">
Wallet Intelligence
</div>

<div class="result">

Balance:
${Number(a.wallet_metrics.balance_eth).toLocaleString(undefined,{maximumFractionDigits:0})} ETH

<br><br>

Transactions:
${a.wallet_metrics.transactions.toLocaleString()}

<br><br>

Wallet Age:
${a.wallet_metrics.wallet_age_days} days

</div>

</div>



<div class="panel">

<div class="title">
Security Indicators
</div>

<div class="result">

${a.signals.map(
x => "<div class='signal'>"+x+"</div>"
).join("")}

</div>

</div>

`;

}


</script>


</body>

</html>

"""

    return HTMLResponse(content=html)
