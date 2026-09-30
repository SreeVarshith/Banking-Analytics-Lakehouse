"""
banking_lakehouse_etl.py — AWS Glue PySpark ETL Job
====================================================

IMPLEMENTATION STATUS: [SPECIFIED IN POC / REFERENCE IMPLEMENTATION]

This file is a REFERENCE IMPLEMENTATION derived from the project specification
and the Glue ETL script documented in the project report.

It is NOT identical to a Glue job that was independently verified as deployed.
The original author's Glue script (as documented in the capstone report) used
glue_catalog with a standard S3 bucket + Iceberg.

This version follows the S3 Tables-based approach specified in the POC
architecture using s3tablescatalog.

To use in AWS Glue:
  - Upload this file to your Glue scripts S3 location.
  - Ensure --datalake-formats iceberg is added to Glue job parameters.
  - Update RAW_BUCKET and TABLE_BUCKET to your actual bucket names.
  - Attach an IAM role with S3, Glue, and S3 Tables permissions.

References:
  - AWS Glue Iceberg docs: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-iceberg.html
  - Amazon S3 Tables: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html
"""

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import when, col, to_date
from pyspark.sql.types import DecimalType

# ---------------------------------------------------------------------------
# Job Initialization
# ---------------------------------------------------------------------------

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc   = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job   = Job(glueContext)
job.init(args["JOB_NAME"], args)

# ---------------------------------------------------------------------------
# Configuration — update these to match your AWS environment
# ---------------------------------------------------------------------------

RAW_BUCKET    = "s3://banking-raw-data-<your-suffix>"
TABLE_BUCKET  = "s3://banking-lakehouse-<your-suffix>"
CATALOG       = "s3tablescatalog"
DATABASE      = "analytics_db"
OUTPUT_TABLE  = f"{CATALOG}.{DATABASE}.enriched_transactions"

# ---------------------------------------------------------------------------
# EXTRACT — Read raw CSVs from S3 landing zone (Bronze layer)
# ---------------------------------------------------------------------------

customers = (
    spark.read
    .option("header", "true")
    .csv(f"{RAW_BUCKET}/customers/")
)

accounts = (
    spark.read
    .option("header", "true")
    .csv(f"{RAW_BUCKET}/accounts/")
)

transactions = (
    spark.read
    .option("header", "true")
    .csv(f"{RAW_BUCKET}/transactions/")
)

# ---------------------------------------------------------------------------
# TRANSFORM — Join, cleanse, cast, enrich (Silver/Gold layer)
# ---------------------------------------------------------------------------

# 1. Join transactions → accounts → customers
df = (
    transactions
    .join(accounts,   "account_id")
    .join(customers,  "customer_id")
)

# 2. Remove duplicates
df = df.dropDuplicates()

# 3. Remove null/zero amounts
df = df.filter(col("amount").isNotNull() & (col("amount") > 0))

# 4. Cast amount to Decimal(10,2)
df = df.withColumn("amount", col("amount").cast(DecimalType(10, 2)))

# 5. Cast timestamp to Date
df = df.withColumn("tx_date", to_date(col("timestamp"), "yyyy-MM-dd HH:mm:ss"))

# 6. Fraud detection flag (transactions > $4,000 marked suspicious)
#    NOTE: This was part of the original implementation documented in the
#    project report. The threshold of 4000 matches the specification.
df = df.withColumn(
    "fraud_flag",
    when(col("amount") > 4000, "Y").otherwise("N")
)

# Select final columns for enriched_transactions
df_enriched = df.select(
    "tx_id",
    "account_id",
    "customer_id",
    "name",
    "country",
    "account_type",
    "amount",
    "tx_type",
    "tx_date",
    "fraud_flag",
)

# ---------------------------------------------------------------------------
# LOAD — Write to Amazon S3 Tables (Apache Iceberg)
# ---------------------------------------------------------------------------

(
    df_enriched
    .writeTo(OUTPUT_TABLE)
    .tableProperty("format-version", "2")
    .tableProperty("location", f"{TABLE_BUCKET}/enriched_transactions/")
    .createOrReplace()
)

print(f"[ETL] Enriched transactions written to: {OUTPUT_TABLE}")
print(f"[ETL] Record count: {df_enriched.count()}")

job.commit()
