"""
tests/test_data_generation.py
==============================
Recommended automated test suite for the Banking Analytics Lakehouse
data generation module.

IMPLEMENTATION STATUS: [RECOMMENDED — not part of original submitted artifacts]

These tests validate the synthetic data generator's output for:
  - correct record counts
  - expected column schemas
  - valid categorical values
  - null / duplicate checks
  - relationship integrity (FK references)
  - amount range bounds

Usage:
    pip install pytest
    pytest tests/test_data_generation.py -v
"""

import os
import sys
import tempfile
import pytest
import pandas as pd

# ---------------------------------------------------------------------------
# Ensure src is importable
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.data_generation.generate_banking_data import generate_banking_data


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def sample_data(tmp_path_factory):
    """Generate sample data to a temporary directory for all tests."""
    out_dir = str(tmp_path_factory.mktemp("sample"))
    generate_banking_data(num_records=100, output_dir=out_dir)
    return {
        "customers":    pd.read_csv(os.path.join(out_dir, "customers.csv")),
        "accounts":     pd.read_csv(os.path.join(out_dir, "accounts.csv")),
        "transactions": pd.read_csv(os.path.join(out_dir, "transactions.csv")),
    }


# ---------------------------------------------------------------------------
# Record count tests
# ---------------------------------------------------------------------------

class TestRecordCounts:
    def test_customer_count(self, sample_data):
        assert len(sample_data["customers"]) == 20, "Expected 20 customer records"

    def test_account_count(self, sample_data):
        assert len(sample_data["accounts"]) == 20, "Expected 20 account records"

    def test_transaction_count(self, sample_data):
        assert len(sample_data["transactions"]) == 100, "Expected 100 transaction records"


# ---------------------------------------------------------------------------
# Column schema tests
# ---------------------------------------------------------------------------

class TestColumnSchema:
    def test_customer_columns(self, sample_data):
        expected = {"customer_id", "name", "country"}
        assert set(sample_data["customers"].columns) == expected

    def test_account_columns(self, sample_data):
        expected = {"account_id", "customer_id", "account_type"}
        assert set(sample_data["accounts"].columns) == expected

    def test_transaction_columns(self, sample_data):
        expected = {"tx_id", "account_id", "amount", "tx_type", "timestamp"}
        assert set(sample_data["transactions"].columns) == expected


# ---------------------------------------------------------------------------
# Categorical value tests
# ---------------------------------------------------------------------------

class TestCategoricalValues:
    def test_valid_countries(self, sample_data):
        valid = {"USA", "UK", "India", "Germany"}
        actual = set(sample_data["customers"]["country"].unique())
        assert actual.issubset(valid), f"Unexpected countries: {actual - valid}"

    def test_valid_account_types(self, sample_data):
        valid = {"Savings", "Current"}
        actual = set(sample_data["accounts"]["account_type"].unique())
        assert actual.issubset(valid), f"Unexpected account types: {actual - valid}"

    def test_valid_tx_types(self, sample_data):
        valid = {"Credit", "Debit"}
        actual = set(sample_data["transactions"]["tx_type"].unique())
        assert actual.issubset(valid), f"Unexpected tx_type values: {actual - valid}"


# ---------------------------------------------------------------------------
# Null / duplicate tests
# ---------------------------------------------------------------------------

class TestNullsAndDuplicates:
    def test_customers_no_nulls(self, sample_data):
        assert sample_data["customers"].isnull().sum().sum() == 0

    def test_accounts_no_nulls(self, sample_data):
        assert sample_data["accounts"].isnull().sum().sum() == 0

    def test_transactions_no_nulls(self, sample_data):
        assert sample_data["transactions"].isnull().sum().sum() == 0

    def test_customer_ids_unique(self, sample_data):
        ids = sample_data["customers"]["customer_id"]
        assert ids.duplicated().sum() == 0, "Duplicate customer IDs found"

    def test_account_ids_unique(self, sample_data):
        ids = sample_data["accounts"]["account_id"]
        assert ids.duplicated().sum() == 0, "Duplicate account IDs found"


# ---------------------------------------------------------------------------
# Amount range tests
# ---------------------------------------------------------------------------

class TestAmountRange:
    def test_amount_min(self, sample_data):
        assert sample_data["transactions"]["amount"].min() >= 10.0

    def test_amount_max(self, sample_data):
        assert sample_data["transactions"]["amount"].max() <= 5000.0

    def test_amount_positive(self, sample_data):
        assert (sample_data["transactions"]["amount"] > 0).all()


# ---------------------------------------------------------------------------
# Relationship integrity tests
# ---------------------------------------------------------------------------

class TestRelationshipIntegrity:
    def test_account_customer_fk(self, sample_data):
        """All account.customer_id values must exist in customers.customer_id."""
        customer_ids = set(sample_data["customers"]["customer_id"])
        account_cids = set(sample_data["accounts"]["customer_id"])
        assert account_cids.issubset(customer_ids), \
            f"Orphan customer_id in accounts: {account_cids - customer_ids}"

    def test_transaction_account_fk(self, sample_data):
        """All transaction.account_id values must exist in accounts.account_id."""
        account_ids = set(sample_data["accounts"]["account_id"])
        tx_aids     = set(sample_data["transactions"]["account_id"])
        assert tx_aids.issubset(account_ids), \
            f"Orphan account_id in transactions: {tx_aids - account_ids}"


# ---------------------------------------------------------------------------
# Custom record count test
# ---------------------------------------------------------------------------

class TestCustomRecordCount:
    def test_custom_transaction_count(self, tmp_path):
        """Generator should respect the --records argument."""
        generate_banking_data(num_records=50, output_dir=str(tmp_path))
        tx = pd.read_csv(tmp_path / "transactions.csv")
        assert len(tx) == 50, "Custom record count not respected"
