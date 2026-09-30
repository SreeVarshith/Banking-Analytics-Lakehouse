-- =============================================================================
-- Athena Business Analytics Queries — Banking Analytics Lakehouse
-- =============================================================================
-- File   : sql/athena/business_queries.sql
-- Purpose: Analytical SQL queries for banking domain insights.
-- Target : Amazon Athena → s3tablescatalog.analytics_db.enriched_transactions
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Q1 — Transaction volume by country
-- -----------------------------------------------------------------------------

SELECT country,
       count(*)        AS total_transactions,
       sum(amount)     AS total_amount,
       avg(amount)     AS avg_amount
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
GROUP BY country
ORDER BY total_amount DESC;


-- -----------------------------------------------------------------------------
-- Q2 — Account type distribution
-- -----------------------------------------------------------------------------

SELECT account_type,
       count(*)    AS accounts_count,
       sum(amount) AS total_volume
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
GROUP BY account_type;


-- -----------------------------------------------------------------------------
-- Q3 — Credit vs Debit split
-- -----------------------------------------------------------------------------

SELECT tx_type,
       count(*)    AS transaction_count,
       sum(amount) AS total_amount,
       min(amount) AS min_amount,
       max(amount) AS max_amount
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
GROUP BY tx_type;


-- -----------------------------------------------------------------------------
-- Q4 — Fraud flagged transactions
-- -----------------------------------------------------------------------------

SELECT tx_id,
       name,
       account_id,
       amount,
       tx_type,
       fraud_flag
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
WHERE fraud_flag = 'Y'
ORDER BY amount DESC;


-- -----------------------------------------------------------------------------
-- Q5 — Daily transaction trend
-- -----------------------------------------------------------------------------

SELECT tx_date,
       count(*)    AS daily_tx_count,
       sum(amount) AS daily_volume
FROM "s3tablescatalog"."analytics_db"."enriched_transactions"
GROUP BY tx_date
ORDER BY tx_date DESC;
