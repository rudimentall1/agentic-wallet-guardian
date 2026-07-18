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

            .container {
                display: flex;
                gap: 20px;
                justify-content: center;
                margin-top: 40px;
            }

            .card {
                background: #151c35;
                border-radius: 15px;
                padding: 25px;
                width: 280px;
            }

            .safe {
                border: 2px solid #22c55e;
            }

            .warn {
                border: 2px solid #eab308;
            }

            .danger {
                border: 2px solid #ef4444;
            }

            .decision {
                font-size: 28px;
                font-weight: bold;
            }

            .score {
                font-size: 22px;
            }

        </style>
    </head>


    <body>

        <h1>
            Agentic Wallet Guardian v2
        </h1>

        <h2 style="text-align:center">
            AI Security Layer for Autonomous Web3 Agents
        </h2>


        <div class="container">


            <div class="card safe">

                <h2>🟢 SAFE AGENT</h2>

                <p class="score">
                    Risk Score: 10/100
                </p>

                <p class="decision">
                    ALLOW
                </p>

                <p>
                    Trusted agent behavior detected.
                </p>

            </div>



            <div class="card warn">

                <h2>🟡 UNKNOWN AGENT</h2>

                <p class="score">
                    Risk Score: 50/100
                </p>

                <p class="decision">
                    WARN
                </p>

                <p>
                    Limited reputation.
                    Monitoring required.
                </p>

            </div>



            <div class="card danger">

                <h2>🔴 MALICIOUS AGENT</h2>

                <p class="score">
                    Risk Score: 100/100
                </p>

                <p class="decision">
                    BLOCK
                </p>

                <p>
                    Malicious behavior detected.
                </p>

            </div>


        </div>


    </body>
    </html>
    """

    return HTMLResponse(html)
