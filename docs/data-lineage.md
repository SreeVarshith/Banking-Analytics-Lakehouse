# Data Lineage — Banking Analytics Lakehouse

## Overview

This document traces the lineage of data from its synthetic generation source
through the AWS pipeline to final analytical consumption.

---

## End-to-End Data Lineage Diagram

```mermaid
flowchart TD
    subgraph GEN["🐍 Python Generator\nsrc/data_generation/generate_banking_data.py"]
        PY1["customers.csv\n20 rows\ncustomer_id, name, country"]
        PY2["accounts.csv\n20 rows\naccount_id, customer_id, account_type"]
        PY3["transactions.csv\n100 rows\ntx_id, account_id, amount, tx_type, timestamp"]
    end

    subgraph BRONZE["☁️ S3 Standard — Bronze / Raw Layer"]
        S3C["s3://banking-raw-data/customers/"]
        S3A["s3://banking-raw-data/accounts/"]
        S3T["s3://banking-raw-data/transactions/"]
    end

    subgraph ETL["⚙️ AWS Glue PySpark — ETL Transformation"]
        J1["Read 3 CSVs"]
        J2["Join: transactions ⟕ accounts ⟕ customers"]
        J3["Deduplicate & filter null/zero amounts"]
        J4["Cast: amount → Decimal(10,2)"]
        J5["Cast: timestamp → Date (tx_date)"]
        J6["Derive: fraud_flag = 'Y' if amount > 4000"]
        J7["Select final columns for enriched_transactions"]
        J1 --> J2 --> J3 --> J4 --> J5 --> J6 --> J7
    end

    subgraph SILVER["🏛️ S3 Tables — Silver/Gold Analytics Layer"]
        ICE["enriched_transactions\nApache Iceberg v2\nanalytics_db"]
    end

    subgraph CATALOG["📚 AWS Glue Data Catalog"]
        META["Schema metadata\nTable partitions\nSnapshot history"]
    end

    subgraph QUERY["🔍 Amazon Athena — Analytics"]
        Q1["Count validation\nSELECT count(*)"]
        Q2["Top customers\nSELECT name, sum(amount)"]
        Q3["Fraud analysis\nSELECT fraud_flag, count(*)"]
    end

    PY1 --> S3C
    PY2 --> S3A
    PY3 --> S3T

    S3C --> J1
    S3A --> J1
    S3T --> J1

    J7 --> ICE
    ICE --> META
    META --> Q1
    META --> Q2
    META --> Q3
```

---

## Column-Level Lineage

### `enriched_transactions` — Column Origins

| Column | Source Table | Source Column | Transformation |
|---|---|---|---|
| `tx_id` | transactions | `tx_id` | None (pass-through) |
| `account_id` | transactions | `account_id` | None (join key) |
| `customer_id` | accounts | `customer_id` | Resolved via join |
| `name` | customers | `name` | Resolved via join |
| `country` | customers | `country` | Resolved via join |
| `account_type` | accounts | `account_type` | Resolved via join |
| `amount` | transactions | `amount` | `cast(Decimal(10,2))` |
| `tx_type` | transactions | `tx_type` | None (pass-through) |
| `tx_date` | transactions | `timestamp` | `to_date(timestamp)` |
| `fraud_flag` | — | — | Derived: `when(amount > 4000, 'Y').otherwise('N')` |

---

## Join Lineage

```
transactions (100 rows)
    │
    │ LEFT JOIN on account_id
    ▼
accounts (20 rows)
    │
    │ LEFT JOIN on customer_id
    ▼
enriched_transactions
(up to 100 rows after dedup/filter)
```

Each transaction gains:
- Account attributes (`account_type`) from the accounts join
- Customer attributes (`name`, `country`) from the customers join

---

## Data Quality Checkpoints

| Stage | Check | Applied By |
|---|---|---|
| Raw generation | No nulls, valid FK refs | Python generator |
| ETL cleansing | `dropDuplicates()` | Glue PySpark |
| ETL cleansing | `filter(amount > 0)` | Glue PySpark |
| ETL type safety | `cast(Decimal(10,2))` | Glue PySpark |
| ETL type safety | `to_date(timestamp)` | Glue PySpark |
| Athena validation | `count(*)` check | Athena SQL |

---

## Lineage Summary Table

| Step | Input | Process | Output | Status |
|---|---|---|---|---|
| 1 | — | Python data generator | 3 CSV files (140 rows total) | ✅ PROVIDED |
| 2 | CSVs | S3 upload | Bronze raw bucket | ⚠️ ARTIFACT NOT PROVIDED |
| 3 | S3 CSVs | Glue ETL (PySpark) | enriched_transactions | ⚠️ ARTIFACT NOT PROVIDED |
| 4 | Iceberg table | Glue Data Catalog | Schema metadata | ⚠️ ARTIFACT NOT PROVIDED |
| 5 | Metadata | Athena SQL | Analytics results | ⚠️ RESULT NOT PROVIDED |
