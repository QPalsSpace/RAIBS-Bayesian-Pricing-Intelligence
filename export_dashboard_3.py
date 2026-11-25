# export_dashboard.py
# Generated executive export version

from pathlib import Path
import multiprocessing
import base64

from dashboard import (
    build_data,
    create_demand_curve,
    create_revenue_curve,
    create_posterior_chart
)

def encode_logo():
    logo_path = Path("assets/RAIBS LLC - Logo-modified.png")
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

def export_dashboard():
    df, trace, summary, result, optimization_df = build_data()

    demand_fig = create_demand_curve(df)
    revenue_fig = create_revenue_curve(optimization_df)
    posterior_fig = create_posterior_chart(summary)

    demand_html = demand_fig.to_html(full_html=False, include_plotlyjs="cdn")
    revenue_html = revenue_fig.to_html(full_html=False, include_plotlyjs=False)
    posterior_html = posterior_fig.to_html(full_html=False, include_plotlyjs=False)

    logo_b64 = encode_logo()

    if logo_b64:
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo">'
    else:
        logo_html = "<div>Logo not found</div>"

    html_report = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>RAIBS Executive Pricing Intelligence</title>
<style>
body{
margin:0;
padding:40px;
background:radial-gradient(circle at top left, rgba(216,176,106,0.12), rgba(0,0,0,0) 40%), #030303;
color:#D8B06A;
font-family:Segoe UI, Arial, sans-serif;
}
</style>
</head>
<body>
{logo_html}
<h1>RAIBS LLC Bayesian Pricing Intelligence</h1>
<h2>Optimal Price: ${result['optimal_price']:.2f}</h2>
<h2>Expected Revenue: ${result['expected_revenue']:.2f}</h2>
{demand_html}
{revenue_html}
{posterior_html}
</body>
</html>'''

    Path("RAIBS_Executive_Report.html").write_text(html_report, encoding="utf-8")
    print("RAIBS_Executive_Report.html generated")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    export_dashboard()
