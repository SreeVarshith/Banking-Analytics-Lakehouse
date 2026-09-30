# Amazon S3 Tables & Apache Iceberg

## Implementation Status: ⚠️ SPECIFIED IN POC — ARTIFACT NOT PROVIDED

The S3 Tables configuration is fully specified in the project architecture.
This document explains the design, configuration, and why S3 Tables are used.

> **Artifact Note:** No S3 Table Bucket console screenshot or API output was
> included in the supplied project files. The documentation below is based on
> the project specification and AWS documentation.

---

## What is Amazon S3 Tables?

Amazon S3 Tables is a purpose-built, managed storage layer for Apache Iceberg
tables. It is **distinct from a standard S3 bucket** containing manually
managed Parquet files.

| Feature | Standard S3 Bucket | Amazon S3 Tables |
|---|---|---|
| Storage type | General object storage | Managed Iceberg storage |
| Table format | Manual (you manage Parquet) | Iceberg v2 (managed) |
| ACID transactions | ❌ No | ✅ Yes |
| Compaction | Manual | ✅ Automatic |
| Schema evolution | Manual | ✅ Native Iceberg |
| Time travel | ❌ No | ✅ Native Iceberg |
| Glue Catalog integration | Optional | ✅ Built-in |
| Athena access | Via crawler | ✅ Direct (via catalog) |

---

## Why S3 Tables for This Project?

The Banking Analytics Lakehouse requires:

1. **ACID-compliant writes** from Glue PySpark (concurrent safe)
2. **Schema evolution** as the enriched_transactions table grows
3. **Time travel** to query historical snapshots
4. **Automatic compaction** to maintain query performance over time
5. **Managed metadata** without manually running Glue crawlers

Amazon S3 Tables with Apache Iceberg provides all of these out of the box.

---

## S3 Tables Configuration

### Table Bucket

A **Table Bucket** is the top-level S3 Tables resource. It is separate from
a regular S3 bucket and is managed by the S3 Tables service.

```
Bucket Name: banking-lakehouse-<your-suffix>
Type: S3 Table Bucket (not a standard S3 bucket)
```

> **[SCREENSHOT REQUIRED]** S3 Table Bucket console view

---

### Namespace

Within the Table Bucket, a **namespace** (equivalent to a database) organizes tables:

```
Namespace: analytics_db
```

> **[SCREENSHOT REQUIRED]** analytics_db namespace in S3 Tables console

---

### Iceberg Table

The ETL job creates the following Iceberg table within the namespace:

```
Table: enriched_transactions
Full path: s3tablescatalog.analytics_db.enriched_transactions
Format: Apache Iceberg v2
```

> **[SCREENSHOT REQUIRED]** enriched_transactions table in S3 Tables console

---

## Apache Iceberg

This project uses **Apache Iceberg** — NOT Delta Lake.

Iceberg is an open table format for large analytic datasets. Key features used:

| Feature | How Used |
|---|---|
| Format version 2 | `.tableProperty("format-version", "2")` in Glue ETL |
| createOrReplace | Idempotent write from Glue |
| Parquet data files | Underlying storage format |
| Metadata JSON | Snapshot and schema tracking |
| ACID commits | Glue PySpark write |

### Iceberg vs Delta Lake (for context)

This project uses **Apache Iceberg** as specified by the assignment.
Delta Lake (Databricks) is a different format and is not part of this project.

---

## Catalog Integration

S3 Tables integrates with **AWS Glue Data Catalog** so that Amazon Athena can
query the Iceberg table using standard SQL:

```sql
SELECT * FROM "s3tablescatalog"."analytics_db"."enriched_transactions";
```

The catalog identifier `s3tablescatalog` is the default catalog name for
S3 Tables integration with Athena.

---

## Automatic Compaction

**Automatic Compaction** is a key operational benefit of S3 Tables.

### Why Compaction Matters

As the Glue ETL job writes to the Iceberg table over time, many small Parquet
data files accumulate. Without compaction:

- Athena queries slow down (more S3 API calls per query)
- Metadata files grow excessively
- Storage costs increase

Automatic Compaction in S3 Tables:

- Merges small files into larger, more efficient files
- Runs without manual intervention
- Maintains optimal query performance

### Verification

> **[REQUIRED VERIFICATION — RESULT NOT PROVIDED]**
>
> The project specification requires verifying that **Automatic Compaction** is
> enabled in the S3 Tables console. No screenshot or verification result was
> included in the supplied artifacts.
>
> **To verify:** Navigate to the S3 Tables console → Table Bucket →
> enriched_transactions → Maintenance → confirm Automatic Compaction is ON.

> **[SCREENSHOT REQUIRED]** Automatic Compaction enabled in S3 Tables console

---

## Console Setup Guide

Since no IaC template is provided, the S3 Tables infrastructure is configured
through the AWS Console:

1. Open **Amazon S3** console
2. Navigate to **S3 Tables** (left sidebar)
3. Click **Create table bucket**
4. Set bucket name: `banking-lakehouse-<your-suffix>`
5. Click **Create namespace** → name: `analytics_db`
6. The `enriched_transactions` table is created automatically by the Glue ETL job
7. After ETL runs, verify the table appears in the console
8. Check **Maintenance** settings — confirm **Automatic Compaction** is enabled

---

## Related Documentation

- [ETL Pipeline](etl-pipeline.md) — how data is written to S3 Tables
- [Athena Validation](athena-validation.md) — how to query the Iceberg table
- [Architecture](architecture.md) — where S3 Tables fits in the overall design
