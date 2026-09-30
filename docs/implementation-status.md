# Implementation Status — Banking Analytics Lakehouse

## Purpose

This document provides an accurate, component-by-component implementation
status for the Banking Analytics Lakehouse POC. It clearly distinguishes
between what was specified in the assignment, what was actually implemented
and evidenced in the supplied artifacts, and what is recommended.

> **Accuracy is more important than appearing complete.**
> This document does not claim completion without evidence.

---

## Status Legend

| Symbol | Status | Meaning |
|---|---|---|
| ✅ | IMPLEMENTED / PROVIDED | Evidence exists in supplied artifacts |
| 📄 | DOCUMENTED IN REPORT | Described/shown in project report (DOCX) |
| ⚠️ | SPECIFIED — ARTIFACT NOT PROVIDED | Required by spec; no independent artifact |
| ❌ | NOT IN SCOPE | Not part of this POC |
| 🔮 | RECOMMENDED | Not specified; recommended for future |

---

## Full Implementation Status Table

| Component | Assignment Requirement | Supplied Evidence | Status |
|---|---|---|---|
| **DATA GENERATION** | | | |
| `customers.csv` (20 rows) | ✅ Required | Python notebook + CSV file | ✅ PROVIDED |
| `accounts.csv` (20 rows) | ✅ Required | Python notebook + CSV file | ✅ PROVIDED |
| `transactions.csv` (100 rows) | ✅ Required | Python notebook + CSV file | ✅ PROVIDED |
| `email` column in customers | Specified in spec | **Not in dataset** | ⚠️ NOT IMPLEMENTED |
| `balance` column in accounts | Specified in spec | **Not in dataset** | ⚠️ NOT IMPLEMENTED |
| **S3 RAW LANDING** | | | |
| S3 raw bucket created | ✅ Required | Mentioned in report | 📄 DOCUMENTED IN REPORT |
| CSVs uploaded to S3 | ✅ Required | Bucket name in report | 📄 DOCUMENTED IN REPORT |
| Folder structure (customers/, accounts/, transactions/) | ✅ Required | Described in report | 📄 DOCUMENTED IN REPORT |
| S3 raw bucket screenshot | ✅ Required for deliverable | **Not supplied** | ⚠️ SCREENSHOT NOT PROVIDED |
| **AWS GLUE ETL** | | | |
| PySpark ETL script | ✅ Required | Script shown in project report | 📄 DOCUMENTED IN REPORT |
| Join: transactions + accounts + customers | ✅ Required | In project report script | 📄 DOCUMENTED IN REPORT |
| Cast amount → Decimal | ✅ Required | In project report script | 📄 DOCUMENTED IN REPORT |
| Cast timestamp → Date | ✅ Required | In project report script | 📄 DOCUMENTED IN REPORT |
| Duplicate removal | ✅ Required | In project report script | 📄 DOCUMENTED IN REPORT |
| Fraud flag derivation (amount > 4000) | ✅ Implemented | In project report script | 📄 DOCUMENTED IN REPORT |
| Glue job deployment screenshot | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| Successful Glue job run screenshot | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| **AWS GLUE WORKFLOW** | | | |
| Glue Workflow created | ✅ Specified | Described in report | 📄 DOCUMENTED IN REPORT |
| Workflow automation (sequential jobs) | ✅ Specified | Described in report | 📄 DOCUMENTED IN REPORT |
| Workflow screenshot | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| **S3 TABLES / ICEBERG** | | | |
| S3 Table Bucket created | ✅ Required | Bucket name in report | 📄 DOCUMENTED IN REPORT |
| `analytics_db` namespace | ✅ Required | Named in Glue script | 📄 DOCUMENTED IN REPORT |
| `enriched_transactions` Iceberg table | ✅ Required | In Glue script | 📄 DOCUMENTED IN REPORT |
| Iceberg format-version 2 | ✅ Required | `.tableProperty("format-version","2")` | 📄 DOCUMENTED IN REPORT |
| S3 Table Bucket screenshot | ✅ Required for deliverable | **Not supplied as standalone** | ⚠️ SCREENSHOT NOT PROVIDED |
| **GLUE DATA CATALOG** | | | |
| Catalog registered by ETL job | ✅ Required | Via `glue_catalog` in script | 📄 DOCUMENTED IN REPORT |
| Glue Catalog screenshot | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| **AMAZON ATHENA** | | | |
| Validation query 1: `count(*)` | ✅ Required | SQL in project report | 📄 DOCUMENTED IN REPORT |
| Validation query 2: Top 3 customers | ✅ Required | SQL in project report | 📄 DOCUMENTED IN REPORT |
| Fraud analysis query | ✅ Implemented | SQL in project report | 📄 DOCUMENTED IN REPORT |
| Timestamp filter in business query | ⚠️ Stated in requirements | **Missing from provided SQL** | ⚠️ DISCREPANCY NOTED |
| Athena result screenshots | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| **AUTOMATION** | | | |
| Amazon EventBridge rule | ✅ Specified | Described in report | 📄 DOCUMENTED IN REPORT |
| EventBridge S3 trigger | ✅ Specified | Described in report | 📄 DOCUMENTED IN REPORT |
| EventBridge screenshot | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| Amazon SNS topic | ✅ Specified | Described in report | 📄 DOCUMENTED IN REPORT |
| SNS email notification | ✅ Specified | Described in report | 📄 DOCUMENTED IN REPORT |
| SNS success/failure screenshot | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| **INCREMENTAL LOAD** | | | |
| DynamoDB watermark tracking | ✅ Specified | Described in report | 📄 DOCUMENTED IN REPORT |
| DynamoDB table screenshot | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| **MAINTENANCE** | | | |
| Automatic Compaction verification | ✅ Required | **Not verified in supplied files** | ⚠️ VERIFICATION NOT PROVIDED |
| **INFRASTRUCTURE** | | | |
| CloudFormation/Terraform template | Spec says: "IaC OR screenshot" | **Not provided** | ⚠️ NOT PROVIDED |
| Infrastructure screenshots (alternative) | ✅ Required | Referenced in report | 📄 DOCUMENTED IN REPORT |
| **TESTING** | | | |
| Automated test suite | ❌ Not required by spec | **Not in original artifacts** | 🔮 RECOMMENDED |
| **REPOSITORY** | | | |
| README | Repository best practice | ✅ Created | ✅ PROVIDED |
| `.gitignore` | Security | ✅ Created | ✅ PROVIDED |
| `SECURITY.md` | Security | ✅ Created | ✅ PROVIDED |
| `.env.example` | Security | ✅ Created | ✅ PROVIDED |
| `requirements.txt` | Reproducibility | ✅ Created | ✅ PROVIDED |
| Data generator script | ✅ Required | ✅ Refactored from notebook | ✅ PROVIDED |
| SQL files | Documentation | ✅ Created | ✅ PROVIDED |
| Infrastructure READMEs | Documentation | ✅ Created | ✅ PROVIDED |

---

## Source vs Implementation Notes

### Note 1 — Missing `email` column

The capstone specification defines `email` as a column in the Customers dataset.
The actual generated dataset does not include this column. The data generator
and sample CSVs reflect the actual implementation.

### Note 2 — Missing `balance` column

The capstone specification defines `balance` as a column in the Accounts dataset.
The actual generated dataset does not include this column.

### Note 3 — Timestamp filter in business query

The stated business requirement for Test 2 refers to "last 30 days."
The validation SQL provided in the project report filters only by `tx_type = 'Credit'`
without an explicit timestamp condition. This discrepancy is documented;
an improved query with the date filter is provided in `sql/athena/validation_queries.sql`.

### Note 4 — Glue ETL deployment evidence

The project report contains the full Glue PySpark script and describes the
Glue job configuration. However, the only file supplied as an artifact is
the project report DOCX — no separate `.py` script file or Glue job
export/screenshot was independently supplied. The script in `src/glue/`
is a reference implementation.

### Note 5 — S3 Tables and Athena results

Screenshots of the S3 Table Bucket, Athena query results, and the
Automatic Compaction setting are referenced in the project report but were
not provided as separate image files in the supplied artifacts.

---

## Artifact Inventory

| Artifact | Type | Status |
|---|---|---|
| `Bank_Analytics_Project.ipynb` | Jupyter Notebook | ✅ Supplied by user |
| `Bank_Datasets.zip` (customers, accounts, transactions CSV) | Dataset archive | ✅ Supplied by user |
| `media_1790759881725.docx` (project report) | Project report DOCX | ✅ Supplied by user |
| Standalone Glue `.py` script | Code file | ⚠️ Not independently supplied |
| S3 / S3 Tables / Glue / Athena screenshots | Image files | ⚠️ Not independently supplied |
| CloudFormation / Terraform template | IaC | ⚠️ Not supplied |
