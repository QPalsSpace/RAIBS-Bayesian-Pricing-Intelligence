import numpy as np
import pandas as pd


def generate_synthetic_retail_data(
        n_rows=4000,
        #seed=42
):

    #np.random.seed(seed)

    retailers = [
        "Walmart",
        "Carrefour",
        "Jumbo",
        "Disco",
        "Coto"
    ]

    products = [
        "Nescafe Gold",
        "KitKat",
        "Nesquik",
        "Dog Chow"
    ]

    df = pd.DataFrame()

    df["retailer"] = np.random.choice(
        retailers,
        n_rows
    )

    df["product"] = np.random.choice(
        products,
        n_rows
    )

    df["price"] = np.random.uniform(
        4,
        8,
        n_rows
    )

    df["promotion"] = np.random.binomial(
        1,
        0.30,
        n_rows
    )

    """
    df["competitor_price"] = (
        df["price"]
        +
        np.random.normal(
            0,
            0.40,
            n_rows
        )
    )
    """ 
    
    df["competitor_price"] = np.random.uniform(
    2.5,
    11.5,
    n_rows
    )
    
    
    demand_noise = np.random.normal(
        0,
        20,
        n_rows
    )

    df["units_sold"] = (
        350
        -
        40 * df["price"]
        +
        30 * df["promotion"]
        +
        15 * df["competitor_price"]
        +
        demand_noise
    )

    df["revenue"] = (
        df["price"]
        *
        df["units_sold"]
    )


    df["price_gap"] = (
    df["price"]
    -
    df["competitor_price"]
    )
    return df


def save_dataset(
        df,
        path="outputs/data/pricing_data.csv"
):

    df.to_csv(
        path,
        index=False
    )

    print(
        f"\nDataset saved -> {path}"
    )