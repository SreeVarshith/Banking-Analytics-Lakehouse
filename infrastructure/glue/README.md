# Infrastructure — AWS Glue

## Purpose

AWS Glue provides the **PySpark ETL engine** for the Banking Analytics Lakehouse.
It reads raw CSVs from S3, joins and transforms them, and writes the enriched
Iceberg table to Amazon S3 Tables.

## Implementation Status: 📄 DOCUMENTED IN PROJECT REPORT

> **[SCREENSHOT REQUIRED]** Glue job configuration  
> **[SCREENSHOT REQUIRED]** Successful Glue job run  
> **[SCREENSHOT REQUIRED]** Glue Workflow configuration

---

## Glue Job Configuration

| Setting | Value |
|---|---|
| Job name | `banking-lakehouse-etl` |
| Type | Spark |
| Glue version | Glue 4.0 |
| Language | Python (PySpark) |
| Worker type | G.1X |
| Number of workers | 2 |
| Script location | `s3://banking-raw-data-<suffix>/scripts/banking_lakehouse_etl.py` |
| Temp directory | `s3://banking-raw-data-<suffix>/glue-temp/` |

---

## Required Job Parameters

| Parameter | Value |
|---|---|
| `--datalake-formats` | `iceberg` |
| `--conf` | `spark.sql.catalog.s3tablescatalog=org.apache.iceberg.spark.SparkCatalog` |
| `--conf` | `spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions` |

---

## IAM Role

The Glue job requires an IAM role with:

- `AWSGlueServiceRole` (managed policy)
- Read access to S3 raw bucket
- Write access to S3 Table Bucket
- `glue:*` permissions for catalog updates
- `s3tables:*` permissions

---

## Glue Workflow

The specification describes a **Glue Workflow** for automated orchestration:

```
Start Trigger
    │
    ▼
banking-lakehouse-etl (Glue Job)
    │
    ▼
Gold Aggregation Job (optional)
```

### Console Setup Steps

1. Open **AWS Glue** console
2. Navigate to **Workflows**
3. Click **Add workflow** → name: `banking-lakehouse-workflow`
4. Add trigger → **On demand** or **Schedule**
5. Add the ETL job as a node
6. Connect optional Gold aggregation job

---

## Glue Data Catalog

The Glue ETL job registers the `enriched_transactions` Iceberg table in the
Glue Data Catalog automatically via the Iceberg catalog configuration.

This enables Athena to discover and query the table without a separate Crawler.

---

## Console Setup Steps — Glue Job

1. Open **AWS Glue** console
2. Navigate to **ETL Jobs**
3. Click **Create job** → **Script editor**
4. Upload `src/glue/banking_lakehouse_etl.py`
5. Configure settings (see table above)
6. Add Iceberg job parameters
7. Attach IAM role
8. Click **Save** and **Run**
