# Screenshots — Amazon Athena

This directory should contain screenshots of Amazon Athena query results
that validate the Banking Analytics Lakehouse pipeline output.

## Required Screenshots

| Filename | Description | Status |
|---|---|---|
| `athena-workgroup-config.png` | Athena workgroup and results bucket config | `[SCREENSHOT REQUIRED]` |
| `athena-count-query.png` | Test 1: `SELECT count(*)` — data integrity result | `[SCREENSHOT REQUIRED]` |
| `athena-top3-customers.png` | Test 2: Top 3 customers by credit volume | `[SCREENSHOT REQUIRED]` |
| `athena-fraud-analysis.png` | Test 3: Fraud flag distribution | `[SCREENSHOT REQUIRED]` |
| `athena-catalog-view.png` | Athena Data source: `s3tablescatalog` → `analytics_db` | `[SCREENSHOT REQUIRED]` |

## Validation Queries

### Test 1 — Count

```sql
SELECT count(*)
FROM "s3tablescatalog"."analytics_db"."enriched_transactions";
```

### Test 2 — Top 3 Customers

```sql
SELECT name,
       sum(amount) AS total_volume
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
WHERE tx_type = 'Credit'
GROUP BY name
ORDER BY total_volume DESC
LIMIT 3;
```

### Test 3 — Fraud Distribution

```sql
SELECT fraud_flag, count(*) AS transaction_count
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
GROUP BY fraud_flag;
```

## How to Capture

1. Open **Amazon Athena** console
2. Set Data source: `s3tablescatalog` | Database: `analytics_db`
3. Run each query from `sql/athena/validation_queries.sql`
4. Screenshot the query editor AND the results pane for each
5. Save using the filenames in the table above

> ⚠️ These screenshots are key deliverables for the capstone project.
> Without them, the Athena validation section status remains:
> `[RESULT NOT PROVIDED IN SUPPLIED ARTIFACTS]`
