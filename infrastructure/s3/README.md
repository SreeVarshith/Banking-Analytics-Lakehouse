# Infrastructure — Amazon S3 Raw Bucket

## Purpose

The Amazon S3 Standard bucket serves as the **Bronze / Raw Landing Zone** for
the Banking Analytics Lakehouse. It stores the raw CSV files before they are
processed by the AWS Glue ETL job.

## Implementation Status: 📄 DOCUMENTED IN PROJECT REPORT

The bucket is described in the project report. No independent screenshot or
AWS CLI export was supplied as a separate artifact.

> **[SCREENSHOT REQUIRED]** S3 raw bucket console view  
> Suggested path: `screenshots/s3/s3-raw-bucket.png`

---

## Configuration

| Setting | Value |
|---|---|
| Bucket name | `banking-raw-data-<your-suffix>` |
| Bucket type | General purpose (Standard S3) |
| Region | `us-east-1` (recommended — required for S3 Tables) |
| Versioning | Optional |
| Public access | ✅ Block all public access |

---

## Folder Structure

```
banking-raw-data-<suffix>/
├── customers/
│   └── customers.csv
├── accounts/
│   └── accounts.csv
├── transactions/
│   └── transactions.csv
├── scripts/
│   └── banking_lakehouse_etl.py     ← Glue job script
└── athena-results/                  ← Athena query output location
```

---

## Console Setup Steps

1. Open **Amazon S3** console
2. Click **Create bucket**
3. Set **Bucket name**: `banking-raw-data-<your-suffix>`
4. Choose **AWS Region**: `us-east-1`
5. Under **Block Public Access**: ensure all options are checked
6. Click **Create bucket**
7. Create the folder structure above
8. Upload the CSVs from `data/sample/`

---

## Upload CSVs Using AWS CLI

```bash
aws s3 cp data/sample/customers.csv    s3://banking-raw-data-<suffix>/customers/
aws s3 cp data/sample/accounts.csv     s3://banking-raw-data-<suffix>/accounts/
aws s3 cp data/sample/transactions.csv s3://banking-raw-data-<suffix>/transactions/
aws s3 cp src/glue/banking_lakehouse_etl.py s3://banking-raw-data-<suffix>/scripts/
```

---

## IAM Permissions Required

The Glue job IAM role needs read access to this bucket:

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:ListBucket"],
  "Resource": [
    "arn:aws:s3:::banking-raw-data-<suffix>",
    "arn:aws:s3:::banking-raw-data-<suffix>/*"
  ]
}
```
