# Data Generation — Banking Analytics Lakehouse

## Implementation Status: ✅ IMPLEMENTED / PROVIDED

The synthetic data generator is a core deliverable of this POC. It is refactored
from the original `Bank_Analytics_Project.ipynb` notebook into a standalone,
importable Python module.

---

## Purpose

The generator creates three synthetic banking datasets that simulate:
- A small bank with 20 customers
- Each customer has one bank account
- 100 banking transactions distributed across those accounts

The data is fully synthetic — no real customer or financial data is used.

---

## Source

| Artifact | Status |
|---|---|
| `Bank_Analytics_Project.ipynb` | ✅ Original notebook (provided) |
| `src/data_generation/generate_banking_data.py` | ✅ Refactored script |
| `data/sample/*.csv` | ✅ Generated output files (provided) |

> **Note:** The original notebook contained a hardcoded Windows filesystem path
> (`C:/Users/sreevarshith/Documents/AWS/Bank_Datasets/`). This path has been
> removed from the public repository. The script now uses a clean relative
> output path (`data/sample/`) by default.

---

## Script Location

```
src/data_generation/generate_banking_data.py
```

---

## Usage

### Basic (default: 100 transactions → data/sample/)

```bash
python src/data_generation/generate_banking_data.py
```

### Custom record count

```bash
python src/data_generation/generate_banking_data.py --records 500
```

### Custom output directory

```bash
python src/data_generation/generate_banking_data.py --output /tmp/banking_data
```

### Programmatic use

```python
from src.data_generation.generate_banking_data import generate_banking_data

generate_banking_data(num_records=100, output_dir="data/sample")
```

---

## Generated Datasets

### `customers.csv` — 20 rows

```
customer_id, name, country
CUST_001, User_1, USA
CUST_002, User_2, USA
CUST_003, User_3, India
...
CUST_020, User_20, Germany
```

**Generation logic:**
- `customer_id`: Zero-padded sequential IDs `CUST_001`…`CUST_020`
- `name`: Synthetic names `User_1`…`User_20`
- `country`: Randomly selected from `["USA", "UK", "India", "Germany"]`

---

### `accounts.csv` — 20 rows

```
account_id, customer_id, account_type
ACC_001, CUST_001, Savings
ACC_002, CUST_002, Savings
ACC_003, CUST_003, Current
...
```

**Generation logic:**
- `account_id`: Zero-padded sequential IDs `ACC_001`…`ACC_020`
- `customer_id`: Direct 1:1 mapping to customers (same ordinal)
- `account_type`: Randomly selected from `["Savings", "Current"]`

---

### `transactions.csv` — 100 rows

```
tx_id, account_id, amount, tx_type, timestamp
TX_82357, ACC_010, 4148.73, Debit, 2026-09-12 00:00:00
TX_35203, ACC_003, 238.66, Credit, 2026-09-06 00:00:00
...
```

**Generation logic:**
- `tx_id`: `TX_` prefix + random 5-digit number
- `account_id`: Randomly selected from the 20 account IDs
- `amount`: Random float between `10.00` and `5000.00`, rounded to 2 decimal places
- `tx_type`: Randomly selected from `["Credit", "Debit"]`
- `timestamp`: Random datetime within the previous 30 days from generation time

---

## Data Quality (Based on Inspection of Supplied Dataset)

| Property | customers | accounts | transactions |
|---|---|---|---|
| Row count | 20 | 20 | 100 |
| Null values | 0 | 0 | 0 |
| Duplicate rows | 0 | 0 | 0 |
| FK integrity | — | ✅ All customer_ids valid | ✅ All account_ids valid |
| Amount range | — | — | 10.00–5000.00 |

---

## Dependencies

```
pandas>=2.0.0
```

No AWS credentials or internet access required for data generation.

---

## Relationship to Notebook

The original `Bank_Analytics_Project.ipynb` contains the same generation logic
embedded in a Jupyter cell with a hardcoded local Windows path.

The refactored script:
- Removes the personal local path
- Adds CLI argument parsing (`--records`, `--output`)
- Adds docstrings and comments
- Is importable as a Python module
- Writes to a clean relative path by default

The original notebook is preserved at `notebooks/Bank_Analytics_Project.ipynb`
for reference.
