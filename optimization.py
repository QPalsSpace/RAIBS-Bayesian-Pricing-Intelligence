import numpy as np
import pandas as pd

from monte_carlo import (
    monte_carlo_revenue_simulation
)


def find_optimal_price(trace):

    prices = np.linspace(
        3,
        10,
        100
    )

    expected_revenues = []

    for p in prices:

        revenue_samples = (
            monte_carlo_revenue_simulation(
                trace,
                p
            )
        )

        expected_revenues.append(
            revenue_samples.mean()
        )

    idx = np.argmax(
        expected_revenues
    )

    result = {

        "optimal_price":
            prices[idx],

        "expected_revenue":
            expected_revenues[idx]
    }

    optimization_df = pd.DataFrame({

        "price":
            prices,

        "expected_revenue":
            expected_revenues
    })

    return result, optimization_df