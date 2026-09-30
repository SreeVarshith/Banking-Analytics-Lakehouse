# Infrastructure — Amazon S3 Tables

## Purpose

Amazon S3 Tables is the **Silver / Gold Analytics Layer** of the Banking
Analytics Lakehouse. It provides managed Apache Iceberg storage for the
`enriched_transactions` table written by the Glue ETL job.

## Implementation Status: 📄 DOCUMENTED IN PROJECT REPORT

The S3 Table Bucket and namespace are described in the project report.

> **[SCREENSHOT REQUIRED]** S3 Table Bucket console view  
> **[SCREENSHOT REQUIRED]** analytics_db namespace  
> **[SCREENSHOT REQUIRED]** enriched_transactions Iceberg table  
> **[SCREENSHOT REQUIRED]** Automatic Compaction setting

---

## Configuration

### Table Bucket

| Setting | Value |
|---|---|
| Bucket name | `banking-lakehouse-<your-suffix>` |
| Bucket type | **S3 Table Bucket** (NOT a standard S3 bucket) |
| Region | `us-east-1` |

> ⚠️ S3 Table Buckets are a distinct resource type from standard S3 buckets.
> They are created via **S3 → S3 Tables** in the console, not via the standard
> S3 bucket creation flow.

---

### Namespace

| Setting | Value |
|---|---|
| Namespace name | `analytics_db` |
| Equivalent to | A database/schema in traditional warehouses |

---

### Iceberg Table

The `enriched_transactions` table is created automatically by the Glue ETL job.

| Setting | Value |
|---|---|
| Table name | `enriched_transactions` |
| Catalog identifier | `s3tablescatalog` |
| Full path | `s3tablescatalog.analytics_db.enriched_transactions` |
| Format | Apache Iceberg v2 |
| Storage format | Parquet |

---

## Console Setup Steps

1. Open **Amazon S3** console
2. Click **S3 Tables** in the left sidebar
3. Click **Create table bucket**
4. Set name: `banking-lakehouse-<your-suffix>`
5. Choose region: `us-east-1`
6. After creation, open the bucket
7. Click **Create namespace** → name: `analytics_db`
8. The `enriched_transactions` table will be created automatically when the Glue job runs

---

## Automatic Compaction

> **[REQUIRED VERIFICATION — RESULT NOT PROVIDED]**
>
> After the ETL job completes, verify that Automatic Compaction is enabled:
>
> S3 Tables Console → Table Bucket → `analytics_db` → `enriched_transactions`
> → **Maintenance** tab → confirm **Automatic Compaction: ON**

Automatic Compaction merges small Parquet files created by incremental writes
into larger, more query-efficient files. This is essential for production-scale
Iceberg table performance.

---

## IAM Permissions Required

```json
{
  "Effect": "Allow",
  "Action": [
    "s3tables:CreateTableBucket",
    "s3tables:CreateNamespace",
    "s3tables:CreateTable",
    "s3tables:PutTableData",
    "s3tables:GetTableData"
  ],
  "Resource": "*"
}
```

The Glue job IAM role must also have `AmazonS3FullAccess` or equivalent for
the S3 Table Bucket.

---

## Difference: Standard S3 vs S3 Tables

| Feature | Standard S3 | Amazon S3 Tables |
|---|---|---|
| Purpose | General object storage | Managed Iceberg storage |
| ACID transactions | ❌ | ✅ |
| Automatic Compaction | ❌ | ✅ |
| Schema evolution | Manual | ✅ Native |
| Time travel | ❌ | ✅ Native |
| Glue Catalog integration | Optional (crawler) | ✅ Built-in |
