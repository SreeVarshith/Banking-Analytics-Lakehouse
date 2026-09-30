# Screenshots — Amazon S3 Tables

This directory should contain screenshots of the Amazon S3 Tables configuration
used as the Silver/Gold analytics layer of the Banking Analytics Lakehouse.

## Required Screenshots

| Filename | Description | Status |
|---|---|---|
| `s3tables-bucket-overview.png` | S3 Table Bucket: `banking-lakehouse-<suffix>` | `[SCREENSHOT REQUIRED]` |
| `s3tables-namespace-analytics-db.png` | `analytics_db` namespace inside the Table Bucket | `[SCREENSHOT REQUIRED]` |
| `s3tables-enriched-transactions-table.png` | `enriched_transactions` Iceberg table details | `[SCREENSHOT REQUIRED]` |
| `s3tables-table-schema.png` | Table schema (columns and types) | `[SCREENSHOT REQUIRED]` |
| `s3tables-automatic-compaction.png` | Maintenance tab — Automatic Compaction enabled | `[REQUIRED VERIFICATION]` |
| `s3tables-snapshots.png` | Iceberg table snapshots / history | `[SCREENSHOT REQUIRED]` |

## How to Capture

1. Open the **Amazon S3** console
2. In the left sidebar, click **S3 Tables**
3. Select your Table Bucket: `banking-lakehouse-<suffix>`
4. Navigate to the `analytics_db` namespace
5. Open the `enriched_transactions` table
6. Capture: overview, schema, and the **Maintenance** tab (Automatic Compaction)

> ⚠️ **Important:** The Automatic Compaction screenshot is a required verification
> for the capstone deliverable. Without this screenshot, the compaction check
> remains `[REQUIRED VERIFICATION — RESULT NOT PROVIDED]` in the implementation status.
