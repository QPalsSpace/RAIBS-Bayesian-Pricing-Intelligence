import numpy as np
import pandas as pd


def monte_carlo_revenue_simulation(
        trace,
        candidate_price,
        n_samples=5000
):

    alpha = (
        trace.posterior["alpha"]
        .values
        .flatten()
    )

    beta = (
        trace.posterior["beta_price"]
        .values
        .flatten()
    )

    idx = np.random.choice(
        len(alpha),
        n_samples,
        replace=True
    )

    alpha = alpha[idx]
    beta = beta[idx]

    demand = (
        alpha
        +
        beta * candidate_price
    )

    revenue = (
        candidate_price
        *
        demand
    )

    return revenue