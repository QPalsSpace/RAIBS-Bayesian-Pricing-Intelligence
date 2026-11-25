from dash import Dash, html, dcc
import time
import plotly.express as px
import plotly.graph_objects as go

from data_generation import generate_synthetic_retail_data
from bayesian_model import fit_bayesian_elasticity
from optimization import find_optimal_price

# ==========================================================
# RAIBS LLC EXECUTIVE PALETTE
# ==========================================================

BG_COLOR = "#030303"

RAIBS_GOLD = "#D8B06A"
RAIBS_LIGHT_GOLD = "#F2D19A"
RAIBS_DARK_GOLD = "#9E6B2D"
RAIBS_BRONZE = "#7B4F20"

CARD_BG = "rgba(15,15,15,0.92)"
PLOT_BG = "#080808"

# ==========================================================
# BUILD DATA
# ==========================================================

def build_data():
    start = time.time()

    print("\nLoading Dashboard Data...\n")

    df = generate_synthetic_retail_data()

    model, trace, summary = fit_bayesian_elasticity(df)

    result, optimization_df = find_optimal_price(trace)

    print(f"Build Data Time = {time.time()-start:.2f} seconds")

    return (
        df,
        trace,
        summary,
        result,
        optimization_df
    )

# ==========================================================
# COMMON FIGURE STYLE
# ==========================================================

def apply_raibs_style(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,

        font=dict(
            color=RAIBS_LIGHT_GOLD,
            family="Montserrat, Inter, Segoe UI, Arial"
        ),

        title_font=dict(
            color=RAIBS_GOLD,
            size=26
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),

        xaxis=dict(
            gridcolor="rgba(216,176,106,0.08)",
            zerolinecolor="rgba(216,176,106,0.12)"
        ),

        yaxis=dict(
            gridcolor="rgba(216,176,106,0.08)",
            zerolinecolor="rgba(216,176,106,0.12)"
        )
    )

    return fig

# ==========================================================
# DEMAND CURVE
# ==========================================================

def create_demand_curve(df):

    fig = px.scatter(
        df,
        x="price",
        y="units_sold",
        color="product",
        title="Demand Curve"
    )

    return apply_raibs_style(fig)

# ==========================================================
# REVENUE CURVE
# ==========================================================

def create_revenue_curve(optimization_df):

    fig = px.line(
        optimization_df,
        x="price",
        y="expected_revenue",
        title="Revenue Optimization"
    )

    fig.update_traces(
        line=dict(
            color= "#9467bd", #RAIBS_GOLD,
            width=3
        )
    )

    return apply_raibs_style(fig)

# ==========================================================
# POSTERIOR CHART
# ==========================================================

def create_posterior_chart(summary):

    fig = go.Figure()

    fig.add_trace(

        go.Bar(
            x=summary.index.astype(str),
            y=summary["mean"],

            marker=dict(
                color=  "#3eb863", #RAIBS_DARK_GOLD,
                line=dict(
                    color= RAIBS_LIGHT_GOLD,
                    width=1
                )
            )
        )
    )

    fig.update_layout(
        title="Bayesian Posterior Estimates",
        xaxis_title="Parameter",
        yaxis_title="Posterior Mean"
    )

    return apply_raibs_style(fig)

# ==========================================================
# SEPARATOR
# ==========================================================

def golden_separator():

    return html.Div(

        style={
            "height":"2px",
            "margin":"35px 0",
            "background":"""
            linear-gradient(
                90deg,
                rgba(0,0,0,0),
                rgba(216,176,106,0.7),
                rgba(0,0,0,0)
            )
            """
        }
    )

# ==========================================================
# EXECUTIVE CARD WRAPPER
# ==========================================================

def executive_panel(component):

    return html.Div(

        style={

            "background": CARD_BG,

            "padding":"20px",

            "borderRadius":"15px",

            "border":
            "1px solid rgba(216,176,106,0.15)",

            "boxShadow":
            "0px 0px 25px rgba(216,176,106,0.08)"
        },

        children=[component]
    )

# ==========================================================
# DASHBOARD
# ==========================================================

def create_dashboard():

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

    app = Dash(__name__)

    app.title = "RAIBS LLC Bayesian Pricing Intelligence"

    app.layout = html.Div(

        style={

            "backgroundColor": BG_COLOR,

            "color": RAIBS_GOLD,

            "padding": "40px",

            "fontFamily":
            "Montserrat, Inter, Segoe UI, Arial, sans-serif",

            "minHeight":"100vh",

            "background":"""
            radial-gradient(
                circle at top left,
                rgba(216,176,106,0.12),
                rgba(0,0,0,0) 40%
            ),
            #030303
            """
        },

        children=[

            # ==================================================
            # HEADER
            # ==================================================

            html.Div(

                style={

                    "height":"450px",

                    "display":"flex",

                    "alignItems":"center",

                    "justifyContent":"flex-start",

                    "marginBottom":"30px"
                },

                children=[

                    html.Div(

                        style={

                            "position":"relative",

                            "width":"360px",

                            "height":"360px"
                        },

                        children=[

                            html.Div(

                                style={

                                    "position":"absolute",

                                    "top":"50%",

                                    "left":"50%",

                                    "transform":"translate(-50%,-50%)",

                                    "width":"280px",

                                    "height":"280px",

                                    "borderRadius":"50%",

                                    "background":"""
                                    radial-gradient(
                                        circle,
                                        rgba(216,176,106,0.75) 0%,
                                        rgba(216,176,106,0.25) 45%,
                                        rgba(216,176,106,0.0) 90%
                                    )
                                    """,

                                    "filter":"blur(40px)"
                                }
                            ),

                            html.Img(

                                src="/assets/RAIBS LLC - Logo-modified.png",

                                style={

                                    "width":"270px",

                                    "height":"270px",

                                    "position":"relative",

                                    "zIndex":"2",

                                    "filter":"""
                                    drop-shadow(0px 0px 25px rgba(216,176,106,0.6))
                                    drop-shadow(0px 0px 50px rgba(216,176,106,0.3))
                                    """
                                }
                            )
                        ]
                    ),

                    html.Div(

                        style={

                            "paddingLeft":"60px",

                            "display":"flex",

                            "flexDirection":"column",

                            "alignItems":"flex-start",

                            "width":"100%"
                        },

                        children=[

                            html.H1(

                                "RAIBS LLC Bayesian Pricing Intelligence",

                                style={

                                    "color":RAIBS_GOLD,

                                    "fontSize":"58px",

                                    "fontWeight":"700",

                                    "letterSpacing":"1.5px",

                                    "marginBottom":"25px",

                                    "textShadow":
                                    "0px 0px 35px rgba(216,176,106,0.8)"
                                }
                            ),

                            html.Div(

                                style={

                                    "display":"flex",

                                    "gap":"25px"
                                },

                                children=[

                                    html.Div(

                                        style={

                                            "background":CARD_BG,

                                            "border":
                                            "1px solid rgba(216,176,106,0.3)",

                                            "borderRadius":"15px",

                                            "padding":"20px",

                                            "width":"280px"
                                        },

                                        children=[

                                            html.Div(
                                                "OPTIMAL PRICE",
                                                style={
                                                    "color":
                                                    RAIBS_LIGHT_GOLD
                                                }
                                            ),

                                            html.H2(
                                                f"${result['optimal_price']:.2f}",
                                                style={
                                                    "color":"white"
                                                }
                                            )
                                        ]
                                    ),

                                    html.Div(

                                        style={

                                            "background":CARD_BG,

                                            "border":
                                            "1px solid rgba(216,176,106,0.3)",

                                            "borderRadius":"15px",

                                            "padding":"20px",

                                            "width":"320px"
                                        },

                                        children=[

                                            html.Div(
                                                "EXPECTED REVENUE",
                                                style={
                                                    "color":
                                                    RAIBS_LIGHT_GOLD
                                                }
                                            ),

                                            html.H2(
                                                f"${result['expected_revenue']:.2f}",
                                                style={
                                                    "color":"white"
                                                }
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),

            golden_separator(),

            executive_panel(
                dcc.Graph(figure=demand_fig)
            ),

            golden_separator(),

            executive_panel(
                dcc.Graph(figure=revenue_fig)
            ),

            golden_separator(),

            executive_panel(
                dcc.Graph(figure=posterior_fig)
            )
        ]
    )

    return app

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    import multiprocessing

    multiprocessing.freeze_support()

    app = create_dashboard()

    app.run(
        debug=False,
        use_reloader=False
    )
