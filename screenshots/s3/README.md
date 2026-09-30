# Screenshots — Amazon S3

This directory should contain screenshots of the Amazon S3 raw bucket
used as the Bronze/landing layer of the Banking Analytics Lakehouse.

## Required Screenshots

| Filename | Description | Status |
|---|---|---|
| `s3-raw-bucket-overview.png` | S3 raw bucket overview (name, region, properties) | `[SCREENSHOT REQUIRED]` |
| `s3-raw-bucket-folders.png` | Folder structure: /customers, /accounts, /transactions, /scripts | `[SCREENSHOT REQUIRED]` |
| `s3-customers-upload.png` | customers.csv uploaded to /customers/ | `[SCREENSHOT REQUIRED]` |
| `s3-accounts-upload.png` | accounts.csv uploaded to /accounts/ | `[SCREENSHOT REQUIRED]` |
| `s3-transactions-upload.png` | transactions.csv uploaded to /transactions/ | `[SCREENSHOT REQUIRED]` |
| `s3-scripts-upload.png` | banking_lakehouse_etl.py in /scripts/ | `[SCREENSHOT REQUIRED]` |

## How to Capture

1. Open the **Amazon S3** console
2. Navigate to your raw bucket: `banking-raw-data-<suffix>`
3. Capture each view listed above
4. Save screenshots using the filenames in the table above
5. Place them in this directory: `screenshots/s3/`
