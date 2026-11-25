from pathlib import Path
import multiprocessing

from dashboard import (
    build_data,
    create_demand_curve,
    create_revenue_curve,
    create_posterior_chart
)


def export_dashboard():

    # ==========================================================
    # BUILD EVERYTHING
    # ==========================================================

    (
        df,
        trace,
        summary,
        result,
        optimization_df
    ) = build_data()

    demand_fig = create_demand_curve(df)

    revenue_fig = create_revenue_curve(
        optimization_df
    )

    posterior_fig = create_posterior_chart(
        summary
    )

    # ==========================================================
    # FIGURES TO HTML
    # ==========================================================

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

    # ==========================================================
    # REPORT
    # ==========================================================

    html_report = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>
RAIBS Bayesian Pricing Intelligence
</title>

<style>

body {{

    background:#030303;

    color:#D8B06A;

    font-family:
    Segoe UI,
    Arial,
    sans-serif;

    margin:40px;
}}

.header {{

    display:flex;

    align-items:center;

    gap:50px;

    margin-bottom:40px;
}}

.logo {{

    width:220px;
}}

.title {{

    font-size:52px;

    font-weight:bold;

    margin-bottom:20px;
}}

.card-container {{

    display:flex;

    gap:25px;
}}

.card {{

    background:#111111;

    border:1px solid #D8B06A;

    border-radius:15px;

    padding:20px;

    min-width:250px;
}}

.card-title {{

    color:#F2D19A;

    font-size:15px;
}}

.card-value {{

    color:white;

    font-size:32px;

    font-weight:bold;
}}

.separator {{

    height:1px;

    background:#D8B06A;

    margin:40px 0;
}}

</style>

</head>

<body>

<div class="header">

<img
src="assets/RAIBS LLC - Logo-modified.png"
class="logo"
>

<div>

<div class="title">
RAIBS Bayesian Pricing Intelligence
</div>

<div class="card-container">

<div class="card">

<div class="card-title">
OPTIMAL PRICE
</div>

<div class="card-value">
${result['optimal_price']:.2f}
</div>

</div>

<div class="card">

<div class="card-title">
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

{demand_html}

<div class="separator"></div>

{revenue_html}

<div class="separator"></div>

{posterior_html}

</body>

</html>
"""

    Path(
        "RAIBS_Dashboard_Report.html"
    ).write_text(
        html_report,
        encoding="utf-8"
    )

    print()
    print("=====================================")
    print("REPORT EXPORTED SUCCESSFULLY")
    print("=====================================")
    print()
    print("RAIBS_Dashboard_Report.html")
    print()


if __name__ == "__main__":

    multiprocessing.freeze_support()

    export_dashboard()