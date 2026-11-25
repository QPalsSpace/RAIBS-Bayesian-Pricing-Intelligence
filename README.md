# RAIBS-Bayesian-Pricing-Intelligence
Developed statistical and analytical pricing work to examine price, demand and revenue relationships and support pricing and commercial decision-making.
Bayesian Demand Modelling, Monte Carlo Simulation & Revenue Optimization | Python, PyMC, ArviZ, Plotly & Dash | RAIBS LLC.

# RAIBS LLC --- Financial & Commercial Analytics \| Bayesian Pricing Intelligence

**A quantitative pricing and revenue-optimization project by RAIBS LLC**

This project demonstrates a Bayesian approach to retail demand modelling
and price optimization. It combines synthetic retail data generation,
probabilistic parameter estimation, Monte Carlo revenue simulation,
numerical price search, and interactive visual reporting.

> **Important:** The repository currently uses synthetic data for
> demonstration and methodological exploration. Its outputs are not
> empirical estimates for a real retailer, product, or market, and
> should not be used as operational pricing recommendations without
> validation on appropriate real-world data.

------------------------------------------------------------------------

## Project Overview

Pricing decisions involve uncertainty about customer demand, promotional
effects, competitor prices, and the relationship between price and
revenue. This project explores how Bayesian inference can represent
uncertainty in demand-model parameters and how posterior samples can be
used in a revenue-oriented pricing exercise.

The workflow is designed to:

1.  Generate a synthetic retail dataset containing retailer, product,
    own-price, promotion, competitor-price, units-sold, revenue, and
    price-gap variables.
2.  Specify a Bayesian regression model for units sold.
3.  Estimate model parameters using Markov chain Monte Carlo (MCMC).
4.  summarize posterior parameter estimates with ArviZ.
5.  Draw parameter samples for candidate prices and estimate expected
    revenue through Monte Carlo simulation.
6.  Search a candidate price grid for the price associated with the
    highest simulated mean revenue.
7.  Present demand, posterior-estimate, and revenue-optimization
    visualizations in a RAIBS-branded dashboard and HTML report.

## Analytical Methodology

### 1. Synthetic retail data

The data-generation module creates a configurable dataset. The
checked-in CSV contains **4,000 synthetic observations** and the
following fields:

  Variable             Description
  -------------------- ------------------------------------------
  `retailer`           Simulated retailer label
  `product`            Simulated product label
  `price`              Simulated selling price
  `promotion`          Binary promotion indicator
  `competitor_price`   Simulated competitor price
  `units_sold`         Simulated unit demand, with random noise
  `revenue`            `price × units_sold`
  `price_gap`          `price − competitor_price`

The synthetic demand-generating relationship is:

\[ Q = 350 - 40P + 30D + 15P_c + `\epsilon`{=tex} \]

where (Q) is units sold, (P) is own price, (D) is the promotion
indicator, (P_c) is competitor price, and (`\epsilon`{=tex}) is normally
distributed noise.

The generator currently uses random sampling without a fixed seed by
default. Therefore, regenerated datasets and model results can vary
between runs.

### 2. Bayesian demand model

`bayesian_model.py` defines a PyMC model in which units sold are
conditionally normally distributed:

\[ Q_i `\sim `{=tex}`\mathcal{N}`{=tex}(`\mu`{=tex}\_i,`\sigma`{=tex})
\]

\[ `\mu`{=tex}\_i = `\alpha `{=tex}+ `\beta`{=tex}\_P P_i +
`\beta`{=tex}\_D D_i + `\beta`{=tex}*C P*{c,i} \]

The model assigns Normal prior distributions to the intercept and
regression coefficients, and a HalfNormal prior to the residual standard
deviation. Posterior sampling is performed with PyMC; ArviZ is used to
summarize the resulting inference data.

The estimated coefficients represent relationships within the specified
model and synthetic dataset. They should not be interpreted as causal
effects without an appropriate identification strategy and validation.

### 3. Monte Carlo revenue simulation and price search

`monte_carlo.py` samples posterior values for the intercept and
own-price coefficient, then calculates demand and revenue for a
candidate price. `optimization.py` evaluates a grid of 100 candidate
prices between 3 and 10 and selects the candidate with the highest
simulated mean revenue.

**Current implementation note:** the Monte Carlo pricing function uses
the posterior draws for the intercept and own-price coefficient only. It
does not currently condition the simulation on promotion or competitor
price, even though those variables appear in the Bayesian demand model.
The optimization output should therefore be understood as a simplified
price-only scenario, not a fully conditional optimization across all
model covariates.

## Dashboard & Outputs

The project includes a Dash application and HTML export scripts.

The dashboard presents:

-   **Demand Curve:** a scatter visualization of price against units
    sold, grouped by product.
-   **Revenue Optimization:** simulated expected revenue across
    candidate prices.
-   **Bayesian Posterior Estimates:** posterior mean estimates for model
    parameters.
-   **Executive Summary Cards:** the selected candidate price and
    corresponding simulated expected revenue.

The visual presentation uses the RAIBS LLC dark-and-gold executive
palette.

Relevant generated assets are stored under `outputs/`:

-   `outputs/data/pricing_data.csv` --- sample synthetic dataset.
-   `outputs/figures/posteriors.png` --- posterior visualization.
-   `outputs/figures/trace.png` --- MCMC trace visualization.
-   `outputs/figures/optimization.html` --- interactive optimization
    visualization.

The repository also contains exported HTML reports. These are generated
artifacts and may reflect a particular run or an earlier version of the
application; rerun the project to refresh them.

## Repository Structure

``` text
RAIBS_LLC-Brochure_VSC_Models/
│
├── main.py
├── dashboard.py
├── bayesian_model.py
├── data_generation.py
├── monte_carlo.py
├── optimization.py
├── visualizations.py
├── export_report.py
├── export_dashboard_1.py
├── export_dashboard_2.py
├── export_dashboard_3.py
├── requirements.txt
│
├── Jupyter Notebooks/
│   └── Bayesian Pricing Model - Analysis.ipynb
│
├── assets/
│   └── RAIBS LLC - Logo-modified.png
│
└── outputs/
    ├── data/
    │   └── pricing_data.csv
    └── figures/
        ├── optimization.html
        ├── posteriors.png
        └── trace.png
```

## Installation

Python 3.10 or a compatible environment is recommended. The project
dependencies are listed in `requirements.txt`.

``` bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>

python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

``` powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

``` bash
source .venv/bin/activate
```

Install dependencies:

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Project

### Run the end-to-end analytical workflow

``` bash
python main.py
```

This generates a synthetic dataset, fits the Bayesian model, performs
the candidate-price search, and creates the posterior, trace, and
optimization visualizations.

### Launch the interactive Dash dashboard

``` bash
python dashboard.py
```

Open the local address printed by Dash in your browser. The dashboard
builds the dataset and fits the model when it starts, so initial loading
can take time depending on the machine and sampling configuration.

### Export an executive HTML report

``` bash
python visualizations.py
```

The export script builds the analytical outputs and writes
`RAIBS_Executive_Report.html` in the working directory.
`export_report.py` is an additional HTML-report export workflow.

## Technology Stack

-   **Python** --- project implementation and analytical orchestration
-   **NumPy & Pandas** --- numerical computation and data preparation
-   **PyMC** --- Bayesian model specification and posterior sampling
-   **ArviZ** --- Bayesian inference diagnostics and posterior summaries
-   **SciPy** --- scientific-computing dependency
-   **Plotly & Dash** --- interactive visualizations and dashboard
    interface
-   **Matplotlib & Kaleido** --- static visualization and figure-export
    dependencies
-   **Jupyter Notebook** --- exploratory analysis

## Interpretation, Validation & Further Development

This repository is a demonstration of an analytical workflow, not a
production-ready pricing engine. Before applying the approach to a live
business decision, further work should include:

-   Replacing synthetic observations with appropriately governed,
    validated commercial data.
-   Fixing random seeds and recording data/model versions for
    reproducibility.
-   Reviewing MCMC convergence and sampling diagnostics, including trace
    plots, effective sample sizes, and (`\hat{R}`{=tex}).
-   Assessing posterior predictive performance and out-of-sample
    accuracy.
-   Evaluating model assumptions, residual behaviour, possible
    nonlinearities, and product/retailer heterogeneity.
-   Extending the optimization simulation to account consistently for
    promotion and competitor-price covariates.
-   Enforcing realistic price bounds, business constraints, and
    operational considerations.
-   Testing sensitivity to priors, model specification, and uncertainty
    assumptions.

These improvements are important before interpreting model outputs as
decision-grade pricing guidance.

## RAIBS LLC

**RAIBS LLC --- High-Performance Data-Driven Consulting**

This project illustrates RAIBS LLC's approach to combining quantitative
methods, statistical modelling, financial and commercial analytics, and
interactive decision-support systems to investigate business problems
under uncertainty.

**Focus areas:** Bayesian modelling · Pricing analytics · Demand
estimation · Revenue optimization · Monte Carlo simulation · Business
intelligence · Decision support

------------------------------------------------------------------------

*Project documentation reflects the code and artifacts contained in this
repository archive. Some notebooks and exported reports may represent
earlier development iterations.*
