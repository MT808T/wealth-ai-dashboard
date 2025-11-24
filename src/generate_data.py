from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd


def generate_synthetic_portfolio(
    n_clients: int = 1289,
    seed: int = 42,
    region: Literal["europe", "global"] = "europe",
) -> pd.DataFrame:
    """
    Generate a synthetic wealth management client portfolio.

    The data is purely fictional and intended for analytics and dashboard demos.
    """
    rng = np.random.default_rng(seed)

    if region == "europe":
        countries = ["CH", "DE", "FR", "IT", "UK", "LU"]
    else:
        countries = ["CH", "US", "HK", "SG", "AE", "UK"]

    client_ids = [f"C{i:04d}" for i in range(1, n_clients + 1)]

    df = pd.DataFrame(
        {
            "client_id": client_ids,
            "country": rng.choice(countries, size=n_clients),
            "aum_chf": rng.uniform(150_000, 8_000_000, size=n_clients).round(0),
            "return_ytd": rng.normal(0.045, 0.07, size=n_clients).round(4),
            "volatility": rng.uniform(0.04, 0.32, size=n_clients).round(4),
            "sharpe_ratio": rng.normal(0.9, 0.35, size=n_clients).round(2),
            "segment": rng.choice(
                ["HNW", "UHNW", "Affluent"],
                size=n_clients,
                p=[0.5, 0.2, 0.3],
            ),
            "advisor_id": rng.integers(1, 15, size=n_clients),
        }
    )

    allocation = pd.DataFrame(
        {
            "asset_equity": rng.uniform(0.15, 0.85, size=n_clients),
            "asset_bonds": rng.uniform(0.05, 0.6, size=n_clients),
            "asset_fx": rng.uniform(0.0, 0.25, size=n_clients),
            "asset_alts": rng.uniform(0.0, 0.25, size=n_clients),
        }
    )
    total = allocation.sum(axis=1)
    allocation = (allocation.T / total).T.round(3)

    df = pd.concat([df, allocation], axis=1)
    return df
