import os
import multiprocessing

from data_generation import (
    generate_synthetic_retail_data,
    save_dataset
)

from bayesian_model import (
    fit_bayesian_elasticity
)

from optimization import (
    find_optimal_price
)

from visualizations import (
    posterior_plot,
    trace_plot,
    optimization_plot
)

def create_directories():

    folders = [

        "outputs",

        "outputs/data",

        "outputs/figures"

    ]

    for folder in folders:

        os.makedirs(
            folder,
            exist_ok=True
        )


def main():

    create_directories()

    print()

    print(
        "=" * 60
    )

    print(
        "RAIBS BAYESIAN PRICING INTELLIGENCE"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "Generating synthetic dataset..."
    )

    df = generate_synthetic_retail_data()

    save_dataset(df)
    
    print(
        df[
            ["price", "competitor_price"]
        ].corr()
    )
    
    model, trace, summary = (
    fit_bayesian_elasticity(df)
    )

    print(summary)

    result, optimization_df = (
        find_optimal_price(trace)
    )

    print()

    print("OPTIMAL PRICE")

    print(result)

    posterior_plot(trace)

    trace_plot(trace)

    optimization_plot(
        optimization_df
    )
    
    print()

    print(
        "Dataset Shape:"
    )

    print(
        df.shape
    )

    print()

    print(
        "First Records:"
    )

    print(
        df.head()
    )

    print()

    print(
        "Revenue Summary:"
    )

    print(
        df["revenue"].describe()
    )


if __name__ == "__main__":

    multiprocessing.freeze_support()

    main()