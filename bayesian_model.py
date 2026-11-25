import time

import pymc as pm
import arviz as az
import numpy as np


def fit_bayesian_elasticity(df):

    print("\nPreparing Bayesian Model...\n")

    start = time.time()

    price = df["price"].values

    promotion = df["promotion"].values

    sales = df["units_sold"].values

    competitor_price = df["competitor_price"]
    
    
    with pm.Model() as model:

        """
        alpha = pm.Normal(
            "alpha",
            mu=300,
            sigma=100
        )

        beta_price = pm.Normal(
            "beta_price",
            mu=-40,
            sigma=20
        )

        beta_promo = pm.Normal(
            "beta_promo",
            mu=30,
            sigma=20
        )
        """ 
        
        sigma = pm.HalfNormal(
            "sigma",
            sigma=20
        )


        alpha = pm.Normal(
            "alpha",
            mu=300,
            sigma=100
        )

        beta_price = pm.Normal(
            "beta_price",
            mu=-37,
            sigma=20
        )

        beta_promo = pm.Normal(
            "beta_promo",
            mu=20,
            sigma=20
        )

        beta_competitor = pm.Normal(
            "beta_competitor",
            mu=25,
            sigma=20
        )

        mu = (
        alpha
        +
        beta_price * price
        +
        beta_promo * promotion
        +
        beta_competitor * competitor_price
        )

        """
        mu = (
            alpha
            +
            beta_price * price
            +
            beta_promo * promotion
        )
        """ 
        
        pm.Normal(
            "sales",
            mu=mu,
            sigma=sigma,
            observed=sales
        )

        print(
            "\nStarting sampling...\n"
        )

        trace = pm.sample(
            draws=2000,
            tune=1000,
            chains=2,
            cores=2,
            target_accept=0.90,
            return_inferencedata=True
        )

    print(
        "\nSampling completed.\n"
    )

    print(
        f"Elapsed Seconds = {time.time()-start:.2f}"
    )

    summary = az.summary(
        trace,
        round_to=3
    )

    return model, trace, summary