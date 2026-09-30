-- =============================================================================
-- Athena Validation Queries — Banking Analytics Lakehouse
-- =============================================================================
-- File   : sql/athena/validation_queries.sql
-- Purpose: SQL queries to validate the enriched_transactions Iceberg table
--          after the Glue ETL job completes.
--
-- Target : Amazon Athena (using Glue Data Catalog or S3 Tables catalog)
-- Table  : s3tablescatalog.analytics_db.enriched_transactions
--
-- Implementation Status:
--   Queries are derived from the official POC specification.
--   Actual Athena execution results: [RESULT NOT PROVIDED IN ARTIFACTS]
-- =============================================================================


-- -----------------------------------------------------------------------------
-- TEST 1 — Data Integrity Validation
-- Validates total record count in the Iceberg table after ETL load.
-- Expected: Should match the number of non-duplicate, non-null transactions
--           processed from the raw CSVs.
-- -----------------------------------------------------------------------------

SELECT count(*)
FROM "s3tablescatalog"."analytics_db"."enriched_transactions";


-- -----------------------------------------------------------------------------
-- TEST 2 — Top Customers by Credit Transaction Volume
-- Business requirement: identify top 3 customers by total credit amount.
--
-- ASSIGNMENT NOTE: The stated business requirement refers to "last 30 days"
-- of transactions. However, the validation SQL provided in the project
-- specification filters only by tx_type = 'Credit' without an explicit
-- timestamp filter. A production implementation should apply the date
-- condition shown below (see TEST 2b).
-- -----------------------------------------------------------------------------

SELECT name,
       sum(amount) AS total_volume
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
WHERE tx_type = 'Credit'
GROUP BY name
ORDER BY total_volume DESC
LIMIT 3;


-- -----------------------------------------------------------------------------
-- TEST 2b — Improved Version (Recommended)
-- Same as TEST 2 but with explicit 30-day timestamp filter applied.
-- This version aligns with the stated "last 30 days" business requirement.
-- -----------------------------------------------------------------------------

SELECT name,
       sum(amount) AS total_volume
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
WHERE tx_type = 'Credit'
  AND tx_date >= date_add('day', -30, current_date)
GROUP BY name
ORDER BY total_volume DESC
LIMIT 3;


-- -----------------------------------------------------------------------------
-- TEST 3 — Fraud Transaction Distribution
-- Count of transactions flagged as suspicious (amount > $4,000)
-- vs normal transactions.
-- -----------------------------------------------------------------------------

SELECT fraud_flag,
       count(*) AS transaction_count
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
GROUP BY fraud_flag;
