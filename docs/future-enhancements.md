# Future Enhancements — Banking Analytics Lakehouse

> All items in this document are **RECOMMENDED** enhancements.  
> None of them were part of the original submitted implementation.

---

## Data Model Enhancements

### 1. Add `email` field to Customers

The capstone specification defines `email` as part of the customers schema.
The current implementation omits it. A future enhancement would add:

```python
"email": [f"user_{i}@example.com" for i in range(1, 21)]
```

This would align the generated dataset with the full specification schema.

### 2. Add `balance` field to Accounts

The capstone specification defines `balance` as part of the accounts schema.
A future enhancement would add a randomly generated starting balance:

```python
"balance": [round(random.uniform(1000.0, 50000.0), 2) for _ in range(20)]
```

---

## ETL Enhancements

### 3. Explicit Timestamp Filter in Business Query

The current Athena business query (Test 2) does not apply an explicit date filter,
despite the stated requirement of "last 30 days." A future enhancement would
enforce:

```sql
AND tx_date >= date_add('day', -30, current_date)
```

This aligns the query with the business requirement.

### 4. Incremental Load (DynamoDB Watermark)

The specification describes a DynamoDB-backed watermark tracking system.
A full implementation would:

- Create a DynamoDB table: `banking_watermark`
- Store the last processed `timestamp` after each ETL run
- On next run, read only records newer than the watermark
- Update the watermark on success

This avoids full dataset reloads and is production-essential for high-volume pipelines.

### 5. Data Quality Framework

Add automated data quality checks in the ETL pipeline:

- Null count checks
- Referential integrity validation
- Amount range validation
- Duplicate detection metrics
- Row count reconciliation (source vs target)

Tools: AWS Glue Data Quality, Deequ, or Great Expectations.

---

## Automation Enhancements

### 6. CI/CD Pipeline

Add GitHub Actions for:

- Running the Python test suite on pull requests
- Linting with `flake8` / `black`
- Type checking with `mypy`

Example `.github/workflows/test.yml`:

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt pytest
      - run: pytest tests/ -v
```

### 7. Infrastructure as Code

Replace the console-based setup with:

- **AWS CloudFormation** or **Terraform** for:
  - S3 raw bucket
  - S3 Table Bucket
  - Glue Job definition
  - Glue Workflow
  - EventBridge rule
  - SNS topic
  - DynamoDB watermark table
  - IAM roles and policies

This makes the environment fully reproducible.

---

## Analytics Enhancements

### 8. Advanced Partitioning

Partition the `enriched_transactions` Iceberg table by `tx_date` to improve
Athena query performance on date-range filters:

```python
df_enriched.writeTo(OUTPUT_TABLE) \
    .partitionedBy("tx_date") \
    .createOrReplace()
```

### 9. Gold Layer Aggregations

Add a Gold layer with pre-aggregated views:

```sql
CREATE TABLE analytics_db.daily_summary AS
SELECT tx_date,
       country,
       account_type,
       tx_type,
       count(*)    AS tx_count,
       sum(amount) AS total_amount
FROM analytics_db.enriched_transactions
GROUP BY tx_date, country, account_type, tx_type;
```

### 10. Real-Time Streaming

Replace batch CSV ingestion with streaming using **Amazon Kinesis Data Streams**
or **Amazon MSK (Kafka)** for near-real-time transaction processing.

---

## Monitoring & Observability

### 11. CloudWatch Dashboards

Add CloudWatch dashboards for:

- Glue job success/failure rate
- ETL job duration trend
- Record count per run

### 12. Machine Learning Fraud Detection

Replace the simple threshold rule (`amount > 4000`) with an ML-based fraud
detection model using **Amazon SageMaker**.

---

## Visualization

### 13. Amazon QuickSight Dashboard

Connect Amazon QuickSight to the Athena data source to build visual dashboards:

- Transaction volume by day/country
- Credit vs Debit trend
- Fraud flag breakdown
- Top customers leaderboard

---

## Summary

| Enhancement | Priority | Effort |
|---|---|---|
| Add `email` and `balance` fields | Medium | Low |
| Timestamp filter in business query | High | Low |
| CI/CD pipeline (GitHub Actions) | High | Medium |
| Infrastructure as Code | High | High |
| Incremental load (DynamoDB) | Medium | Medium |
| Data quality framework | Medium | Medium |
| Partitioning strategy | Medium | Low |
| Gold layer aggregations | Low | Medium |
| Real-time streaming | Low | High |
| ML fraud detection | Low | High |
| QuickSight dashboard | Low | Medium |
