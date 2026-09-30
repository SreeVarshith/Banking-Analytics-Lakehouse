"""
Banking Analytics Lakehouse — Synthetic Data Generator
=======================================================
Generates synthetic banking datasets for the Banking Analytics Lakehouse POC.

Outputs three CSV files to data/sample/ (relative to the project root):
  - customers.csv   : 20 customer records
  - accounts.csv    : 20 account records
  - transactions.csv: 100 transaction records

Usage:
    python src/data_generation/generate_banking_data.py
    python src/data_generation/generate_banking_data.py --records 200 --output data/sample

Implementation Status: [IMPLEMENTED / PROVIDED]
Origin: Refactored from Bank_Analytics_Project.ipynb
Personal filesystem paths removed; relative output path used.
"""

import os
import random
import argparse
from datetime import datetime, timedelta

import pandas as pd


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def generate_banking_data(num_records: int = 100, output_dir: str = "data/sample") -> None:
    """
    Generate synthetic banking datasets and write them to output_dir.

    Parameters
    ----------
    num_records : int
        Number of transaction records to generate (default: 100).
    output_dir : str
        Directory path (relative or absolute) where CSV files are written.
    """
    os.makedirs(output_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # CUSTOMERS  (20 records)
    # ------------------------------------------------------------------
    num_customers = 20
    cust_ids = [f"CUST_{str(i).zfill(3)}" for i in range(1, num_customers + 1)]

    customers = pd.DataFrame({
        "customer_id": cust_ids,
        "name":        [f"User_{i}" for i in range(1, num_customers + 1)],
        "country":     [random.choice(["USA", "UK", "India", "Germany"])
                        for _ in range(num_customers)],
    })

    # ------------------------------------------------------------------
    # ACCOUNTS  (20 records — one per customer)
    # ------------------------------------------------------------------
    acc_ids = [f"ACC_{str(i).zfill(3)}" for i in range(1, num_customers + 1)]

    accounts = pd.DataFrame({
        "account_id":   acc_ids,
        "customer_id":  cust_ids,
        "account_type": [random.choice(["Savings", "Current"])
                         for _ in range(num_customers)],
    })

    # ------------------------------------------------------------------
    # TRANSACTIONS  (num_records records)
    # ------------------------------------------------------------------
    base_date = datetime.now()
    transactions_list = []

    for _ in range(num_records):
        transactions_list.append({
            "tx_id":      f"TX_{random.randint(10000, 99999)}",
            "account_id": random.choice(acc_ids),
            "amount":     round(random.uniform(10.0, 5000.0), 2),
            "tx_type":    random.choice(["Credit", "Debit"]),
            "timestamp":  (base_date - timedelta(days=random.randint(0, 30)))
                          .strftime("%Y-%m-%d %H:%M:%S"),
        })

    transactions = pd.DataFrame(transactions_list)

    # ------------------------------------------------------------------
    # Write CSVs
    # ------------------------------------------------------------------
    customers_path    = os.path.join(output_dir, "customers.csv")
    accounts_path     = os.path.join(output_dir, "accounts.csv")
    transactions_path = os.path.join(output_dir, "transactions.csv")

    customers.to_csv(customers_path, index=False)
    accounts.to_csv(accounts_path, index=False)
    transactions.to_csv(transactions_path, index=False)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f"[generate_banking_data] Output directory : {os.path.abspath(output_dir)}")
    print(f"[generate_banking_data] customers.csv    : {len(customers)} rows")
    print(f"[generate_banking_data] accounts.csv     : {len(accounts)} rows")
    print(f"[generate_banking_data] transactions.csv : {len(transactions)} rows")
    print("[generate_banking_data] Done.")


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic banking datasets for the Banking Analytics Lakehouse POC."
    )
    parser.add_argument(
        "--records",
        type=int,
        default=100,
        help="Number of transaction records to generate (default: 100).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/sample",
        help="Output directory for generated CSV files (default: data/sample).",
    )
    args = parser.parse_args()
    generate_banking_data(num_records=args.records, output_dir=args.output)


if __name__ == "__main__":
    main()
