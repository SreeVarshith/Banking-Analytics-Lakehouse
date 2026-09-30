# Infrastructure — Amazon Athena

## Purpose

Amazon Athena provides **serverless SQL analytics** over the Iceberg table
stored in Amazon S3 Tables. It is the final validation and analytics layer
of the Banking Analytics Lakehouse.

## Implementation Status: 📄 DOCUMENTED IN PROJECT REPORT

> **[SCREENSHOT REQUIRED]** Athena workgroup configuration  
> **[SCREENSHOT REQUIRED]** Athena count(*) validation result  
> **[SCREENSHOT REQUIRED]** Athena top-3 customers result  
> **[SCREENSHOT REQUIRED]** Athena fraud analysis result

---

## Configuration

| Setting | Value |
|---|---|
| Catalog | `s3tablescatalog` |
| Database | `analytics_db` |
| Table | `enriched_transactions` |
| Query results bucket | `s3://banking-raw-data-<suffix>/athena-results/` |
| Region | `us-east-1` |

---

## Workgroup Setup

1. Open **Amazon Athena** console
2. Navigate to **Workgroups**
3. Create or use the **primary** workgroup
4. Set query results location: `s3://banking-raw-data-<suffix>/athena-results/`

---

## Running Validation Queries

1. In Athena query editor:
   - **Data source:** `s3tablescatalog`
   - **Database:** `analytics_db`
2. Paste queries from `sql/athena/validation_queries.sql`
3. Click **Run**

### Query 1 — Count Validation

```sql
SELECT count(*)
FROM "s3tablescatalog"."analytics_db"."enriched_transactions";
```

### Query 2 — Top Customers by Credit Volume

```sql
SELECT name,
       sum(amount) AS total_volume
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
WHERE tx_type = 'Credit'
GROUP BY name
ORDER BY total_volume DESC
LIMIT 3;
```

### Query 3 — Fraud Distribution

```sql
SELECT fraud_flag, count(*) AS transaction_count
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
GROUP BY fraud_flag;
```

---

## Athena Pricing Note

Athena charges per query based on data scanned (~\$5 per TB).
Iceberg columnar Parquet format and partitioning minimize scanned data and cost.

---

## Full SQL Reference

See:

- `sql/athena/validation_queries.sql` — validation tests
- `sql/athena/business_queries.sql` — additional analytics
