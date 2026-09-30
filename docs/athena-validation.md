# Athena Validation — Banking Analytics Lakehouse

## Implementation Status: ⚠️ QUERIES PROVIDED — EXECUTION RESULTS NOT PROVIDED

The validation SQL queries are derived from the project specification.
Actual Athena execution results and screenshots are not included in the
supplied project artifacts.

---

## Overview

Amazon Athena provides serverless SQL access to the Iceberg table stored in
Amazon S3 Tables via the AWS Glue Data Catalog.

```
Amazon Athena
    │
    │ SQL query
    ▼
AWS Glue Data Catalog  (metadata)
    │
    ▼
s3tablescatalog.analytics_db.enriched_transactions
    │
    ▼
Apache Iceberg → Amazon S3 Tables (Parquet files)
```

---

## Prerequisites

Before running these queries:

1. The Glue ETL job must have completed successfully
2. The `enriched_transactions` Iceberg table must exist in `analytics_db`
3. Athena must be configured with an S3 results bucket:
   ```
   s3://banking-raw-data-<suffix>/athena-results/
   ```
4. The Athena workgroup must be configured to use the S3 Tables catalog

---

## Test 1 — Data Integrity Validation

**Purpose:** Validates the total record count in the Iceberg table after the
ETL load. Confirms data was written successfully.

```sql
SELECT count(*)
FROM "s3tablescatalog"."analytics_db"."enriched_transactions";
```

**Expected behavior:** Returns the number of non-duplicate, non-null
transactions that passed the ETL cleansing rules.

> **[RESULT NOT PROVIDED]** Actual Athena count query result not included in supplied artifacts.
>
> **[SCREENSHOT REQUIRED]** Athena count query result

---

## Test 2 — Top Customers by Credit Transaction Volume

**Purpose:** Business analytics — identifies the top 3 customers by total
Credit transaction amount.

```sql
SELECT name,
       sum(amount) AS total_volume
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
WHERE tx_type = 'Credit'
GROUP BY name
ORDER BY total_volume DESC
LIMIT 3;
```

> **⚠️ Assignment Note:** The stated business requirement specifies "last 30 days"
> of transactions. However, the validation SQL provided in the project specification
> filters only by `tx_type = 'Credit'` without an explicit timestamp filter.
> A production implementation should explicitly apply the date condition (see Test 2b below).
> This discrepancy is documented here rather than silently corrected.

> **[RESULT NOT PROVIDED]** Actual Athena top-3 query result not included in supplied artifacts.
>
> **[SCREENSHOT REQUIRED]** Athena top-3 customers query result

---

## Test 2b — Improved Version (Recommended)

Same query with explicit 30-day date filter, aligning with the stated
business requirement:

```sql
SELECT name,
       sum(amount) AS total_volume
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
WHERE tx_type = 'Credit'
  AND tx_date >= date_add('day', -30, current_date)
GROUP BY name
ORDER BY total_volume DESC
LIMIT 3;
```

---

## Test 3 — Fraud Transaction Distribution

**Purpose:** Validates the fraud detection logic. Shows the split between
normal (`N`) and suspicious (`Y`) transactions.

```sql
SELECT fraud_flag,
       count(*) AS transaction_count
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
GROUP BY fraud_flag;
```

**Expected:** Transactions with `amount > 4000` are flagged `'Y'`.

> **[RESULT NOT PROVIDED]** Actual Athena fraud query result not included.

---

## SQL Files Location

```
sql/athena/
├── validation_queries.sql    ← Tests 1, 2, 2b, 3
└── business_queries.sql      ← Additional analytics queries
```

---

## How to Run in Athena

1. Open the **Amazon Athena** console
2. Select your **Workgroup**
3. Set the **Data source** to `s3tablescatalog`
4. Set the **Database** to `analytics_db`
5. Paste the query into the query editor
6. Click **Run**
7. View results in the **Results** pane
8. Download as CSV if needed for the project report

---

## Glue Data Catalog

The Athena queries work because the AWS Glue Data Catalog maintains the
metadata (schema, location, partitions) for the Iceberg table written by the
Glue ETL job. Athena resolves `s3tablescatalog.analytics_db.enriched_transactions`
through this catalog without requiring a manual Glue Crawler run.

---

## Screenshots Required

| Screenshot | Location | Status |
|---|---|---|
| Athena count query result | `screenshots/athena/` | [REQUIRED] |
| Athena top-3 query result | `screenshots/athena/` | [REQUIRED] |
| Athena fraud analysis result | `screenshots/athena/` | [REQUIRED] |
| Athena workgroup configuration | `screenshots/athena/` | [REQUIRED] |
