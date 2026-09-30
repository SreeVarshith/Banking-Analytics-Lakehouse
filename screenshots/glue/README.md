# Screenshots — AWS Glue

This directory should contain screenshots of the AWS Glue configuration
used as the ETL engine of the Banking Analytics Lakehouse.

## Required Screenshots

| Filename | Description | Status |
|---|---|---|
| `glue-job-overview.png` | Glue ETL job overview (name, status, config) | `[SCREENSHOT REQUIRED]` |
| `glue-job-parameters.png` | Job parameters (esp. `--datalake-formats iceberg`) | `[SCREENSHOT REQUIRED]` |
| `glue-job-run-success.png` | Successful job run (green status, duration, records) | `[SCREENSHOT REQUIRED]` |
| `glue-job-script.png` | Script editor showing the PySpark ETL code | `[SCREENSHOT REQUIRED]` |
| `glue-workflow-overview.png` | Glue Workflow DAG (Start trigger → ETL job) | `[SCREENSHOT REQUIRED]` |
| `glue-workflow-run.png` | Successful workflow run | `[SCREENSHOT REQUIRED]` |
| `glue-data-catalog-database.png` | Glue Data Catalog showing `analytics_db` database | `[SCREENSHOT REQUIRED]` |
| `glue-data-catalog-table.png` | `enriched_transactions` table in Glue Catalog | `[SCREENSHOT REQUIRED]` |
| `glue-eventbridge-trigger.png` | EventBridge rule triggering Glue Workflow | `[SCREENSHOT REQUIRED]` |
| `glue-sns-notification.png` | SNS email notification (success or failure) | `[SCREENSHOT REQUIRED]` |

## How to Capture

1. Open **AWS Glue** console → ETL Jobs → `banking-lakehouse-etl`
2. Capture job overview, parameters, and a successful run
3. Navigate to **Workflows** → capture workflow DAG and run history
4. Navigate to **Data Catalog → Databases → analytics_db** → capture table metadata
5. Open **Amazon EventBridge** → capture the S3 trigger rule
6. Open **Amazon SNS** → capture the topic and subscription confirmation
