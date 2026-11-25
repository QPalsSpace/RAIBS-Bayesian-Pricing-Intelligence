from pathlib import Path
import multiprocessing
import base64

from dashboard import (
    build_data,
    create_demand_curve,
    create_revenue_curve,
    create_posterior_chart
)

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def export_dashboard():

    (
        df,
        trace,
        summary,
        result,
        optimization_df
    ) = build_data()

    demand_fig = create_demand_curve(df)
    revenue_fig = create_revenue_curve(optimization_df)
    posterior_fig = create_posterior_chart(summary)

    demand_html = demand_fig.to_html(
        full_html=False,
        include_plotlyjs="cdn"
    )

    revenue_html = revenue_fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    posterior_html = posterior_fig.to_html(
        full_html=False,
        include_plotlyjs=False
    )

    logo_path = "assets/RAIBS LLC - Logo-modified.png"
    logo_b64 = image_to_base64(logo_path)

    html_report = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>RAIBS Executive Report</title>

<style>

* {{
    box-sizing:border-box;
}}

body {{

    margin:0;
    padding:40px;

    background:
    radial-gradient(
        circle at top left,
        rgba(216,176,106,0.14),
        rgba(0,0,0,0) 40%
    ),
    #030303;

    color:#D8B06A;

    font-family:
    "Segoe UI",
    Arial,
    sans-serif;
}}

.container {{
    max-width:1800px;
    margin:auto;
}}

.header {{

    min-height:420px;

    display:flex;

    align-items:center;

    gap:60px;

    margin-bottom:40px;
}}

.logo-wrapper {{

    position:relative;

    width:340px;
    height:340px;

    flex-shrink:0;
}}

.logo-glow {{

    position:absolute;

    top:50%;
    left:50%;

    transform:
    translate(-50%,-50%);

    width:280px;
    height:280px;

    border-radius:50%;

    background:
    radial-gradient(
        circle,
        rgba(216,176,106,0.75) 0%,
        rgba(216,176,106,0.25) 45%,
        rgba(216,176,106,0.00) 90%
    );

    filter:blur(40px);
}}

.logo {{

    position:relative;

    z-index:2;

    width:270px;

    display:block;

    margin:auto;

    filter:
    drop-shadow(0px 0px 25px rgba(216,176,106,0.6))
    drop-shadow(0px 0px 50px rgba(216,176,106,0.3));
}}

.title {{

    color:#D8B06A;

    font-size:58px;

    font-weight:700;

    letter-spacing:1.5px;

    text-shadow:
    0px 0px 35px rgba(216,176,106,0.8);

    margin-bottom:30px;
}}

.cards {{

    display:flex;
    gap:25px;
    flex-wrap:wrap;
}}

.card {{

    background:rgba(15,15,15,0.92);

    border-radius:15px;

    padding:20px;

    min-width:280px;

    border:
    1px solid rgba(216,176,106,0.3);

    box-shadow:
    0px 0px 25px rgba(216,176,106,0.08);
}}

.card-label {{

    color:#F2D19A;

    font-size:14px;
}}

.card-value {{

    color:white;

    font-size:34px;

    font-weight:bold;

    margin-top:8px;
}}

.separator {{

    height:2px;

    margin:35px 0;

    background:
    linear-gradient(
        90deg,
        rgba(0,0,0,0),
        rgba(216,176,106,0.7),
        rgba(0,0,0,0)
    );
}}

.panel {{

    background:rgba(15,15,15,0.92);

    padding:20px;

    border-radius:15px;

    border:
    1px solid rgba(216,176,106,0.15);

    box-shadow:
    0px 0px 25px rgba(216,176,106,0.08);
}}

</style>
</head>

<body>

<div class="container">

<div class="header">

<div class="logo-wrapper">

<div class="logo-glow"></div>

<img
class="logo"
src="data:image/png;base64,{logo_b64}">

</div>

<div>

<div class="title">
RAIBS LLC Bayesian Pricing Intelligence
</div>

<div class="cards">

<div class="card">

<div class="card-label">
OPTIMAL PRICE
</div>

<div class="card-value">
${result['optimal_price']:.2f}
</div>

</div>

<div class="card">

<div class="card-label">
EXPECTED REVENUE
</div>

<div class="card-value">
${result['expected_revenue']:.2f}
</div>

</div>

</div>

</div>

</div>

<div class="separator"></div>

<div class="panel">
{demand_html}
</div>

<div class="separator"></div>

<div class="panel">
{revenue_html}
</div>

<div class="separator"></div>

<div class="panel">
{posterior_html}
</div>

</div>

</body>
</html>
"""

    Path("RAIBS_Executive_Report.html").write_text(
        html_report,
        encoding="utf-8"
    )

    print("RAIBS_Executive_Report.html generated")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    export_dashboard()

"""
path = "/mnt/data/export_dashboard_replacement.py"
Path(path).write_text(code, encoding="utf-8")
print(path)
"""