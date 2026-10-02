from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


# Make the generated dataset reproducible
rng = np.random.default_rng(42)

NUM_PACKAGES = 10_000

PROVIDERS = ["Amazon", "Temu", "AliExpress"]

ORIGIN_COUNTRIES = {
    "Amazon": ["USA", "Mexico"],
    "Temu": ["China", "USA"],
    "AliExpress": ["China", "USA"],
}

PROVINCES = [
    "San José",
    "Alajuela",
    "Heredia",
    "Cartago",
    "Guanacaste",
    "Puntarenas",
    "Limón",
]

SHIPPING_METHODS = ["Standard", "Express", "Economy"]

STATUSES = [
    "Delivered",
    "In Transit",
    "Delayed",
    "Returned",
    "Cancelled",
]


# Probability of each province receiving a package
PROVINCE_PROBABILITIES = [
    0.30,  # San José
    0.18,  # Alajuela
    0.15,  # Heredia
    0.12,  # Cartago
    0.09,  # Guanacaste
    0.08,  # Puntarenas
    0.08,  # Limón
]

# Provider-specific characteristics
PROVIDER_PROBABILITIES = [0.36, 0.34, 0.30]

PROVIDER_WEIGHT_MEAN = {
    "Amazon": 9.5,
    "Temu": 7.5,
    "AliExpress": 11.0,
}

PROVIDER_COST_FACTOR = {
    "Amazon": 1.10,
    "Temu": 0.90,
    "AliExpress": 1.00,
}

PROVIDER_DELIVERY_ADJUSTMENT = {
    "Amazon": -0.5,
    "Temu": 0.7,
    "AliExpress": 0.2,
}

PROVIDER_SHIPPING_PROBABILITIES = {
    "Amazon": [0.40, 0.40, 0.20],
    "Temu": [0.25, 0.15, 0.60],
    "AliExpress": [0.40, 0.20, 0.40],
}

PROVINCE_DELIVERY_DAYS = {
    "San José": 6.5,
    "Alajuela": 6.8,
    "Heredia": 6.6,
    "Cartago": 7.2,
    "Puntarenas": 8.0,
    "Guanacaste": 8.5,
    "Limón": 8.4,
}


def random_date(start_date, end_date):
    """Generate a random date between two dates."""
    days_between = (end_date - start_date).days

    return start_date + timedelta(
        days=int(rng.integers(0, days_between + 1))
    )


def generate_package(package_number):
    """Generate a single package record."""

    provider = rng.choice(
        PROVIDERS,
        p=PROVIDER_PROBABILITIES,
    )

    order_date = random_date(
        datetime(2026, 1, 1),
        datetime(2026, 9, 30),
    )

    shipping_delay = int(
        rng.integers(1, 6)
    )

    ship_date = order_date + timedelta(
        days=shipping_delay
    )

    # Provider-specific weight
    weight_kg = round(
        float(
            np.clip(
                rng.normal(
                    PROVIDER_WEIGHT_MEAN[provider],
                    3.0,
                ),
                0.1,
                30,
            )
        ),
        2,
    )

    # Provider-specific shipping method distribution
    shipping_method = rng.choice(
        SHIPPING_METHODS,
        p=PROVIDER_SHIPPING_PROBABILITIES[provider],
    )

    # Province
    destination_province = rng.choice(
        PROVINCES,
        p=PROVINCE_PROBABILITIES,
    )

    # Delivery time based on province, provider and method
    method_adjustment = {
        "Express": -1.2,
        "Standard": 0,
        "Economy": 0.7,
    }

    delivery_days = (
        PROVINCE_DELIVERY_DAYS[destination_province]
        + PROVIDER_DELIVERY_ADJUSTMENT[provider]
        + method_adjustment[shipping_method]
        + float(rng.normal(0, 0.8))
    )

    delivery_days = max(
        2,
        round(delivery_days),
    )

    estimated_delivery_date = (
        ship_date
        + timedelta(days=delivery_days)
    )

    status = rng.choice(
        STATUSES,
        p=[0.80, 0.08, 0.06, 0.04, 0.02],
    )

    actual_delivery_date = None

    if status in ["Delivered", "Delayed"]:
        actual_delay = int(
            rng.integers(-2, 6)
        )

        actual_delivery_date = (
            estimated_delivery_date
            + timedelta(days=actual_delay)
        )

    # Shipping cost
    base_cost = 5 + (weight_kg * 1.8)

    if shipping_method == "Express":
        base_cost *= 1.5
    elif shipping_method == "Economy":
        base_cost *= 0.8

    base_cost *= PROVIDER_COST_FACTOR[provider]

    shipping_cost = round(
        base_cost,
        2,
    )

    delivery_attempts = rng.choice(
        [1, 2, 3],
        p=[0.85, 0.12, 0.03],
    )

    damaged = bool(
        rng.choice(
            [False, True],
            p=[0.97, 0.03],
        )
    )

    return {
        "package_id": f"PKG-{package_number:05d}",
        "provider": provider,
        "origin_country": rng.choice(
            ORIGIN_COUNTRIES[provider]
        ),
        "destination_province": destination_province,
        "order_date": order_date.date(),
        "ship_date": ship_date.date(),
        "estimated_delivery_date": (
            estimated_delivery_date.date()
        ),
        "actual_delivery_date": (
            actual_delivery_date.date()
            if actual_delivery_date
            else None
        ),
        "weight_kg": weight_kg,
        "shipping_cost_usd": shipping_cost,
        "shipping_method": shipping_method,
        "status": status,
        "delivery_attempts": delivery_attempts,
        "damaged": damaged,
    }


def main():
    packages = [
        generate_package(i)
        for i in range(1, NUM_PACKAGES + 1)
    ]

    df = pd.DataFrame(packages)

    output_path = Path("data/raw/packages.csv")
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Dataset generated successfully: {output_path}"
    )
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":
    main()
