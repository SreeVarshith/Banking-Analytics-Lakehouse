# Data Flow Diagram — Banking Analytics Lakehouse

## End-to-End Data Flow

```mermaid
flowchart LR
    subgraph GEN["🐍 Python\nGenerator"]
        PY["generate_banking_data.py"]
    end

    subgraph RAW["📁 Raw Files\ndata/sample/"]
        F1["customers.csv\n20 rows"]
        F2["accounts.csv\n20 rows"]
        F3["transactions.csv\n100 rows"]
    end

    subgraph S3B["☁️ S3 Standard\nBronze Layer"]
        S3["banking-raw-data\nbucket"]
    end

    subgraph GLUE["⚙️ AWS Glue\nPySpark"]
        J["banking_lakehouse_etl.py\n\n① Read CSVs\n② Join 3 tables\n③ Deduplicate\n④ Cast types\n⑤ Fraud flag"]
    end

    subgraph S3T["🏛️ S3 Tables\nSilver/Gold Layer"]
        ICE["analytics_db\n.enriched_transactions\n(Iceberg v2)"]
    end

    subgraph CAT["📚 Glue\nData Catalog"]
        META["Schema\nMetadata"]
    end

    subgraph ATH["🔍 Amazon\nAthena"]
        SQL["SQL Queries\nValidation\n+ Analytics"]
    end

    PY --> F1 & F2 & F3
    F1 & F2 & F3 -->|aws s3 cp| S3
    S3 -->|EventBridge\ntrigger| J
    J -->|writeTo\nIceberg| ICE
    ICE -->|auto-register| META
    META -->|catalog\nlookup| SQL
```

---

## Record-Level Flow

```mermaid
flowchart TD
    subgraph SOURCE["Source Records"]
        C20["20 customers\nCUST_001…CUST_020"]
        A20["20 accounts\nACC_001…ACC_020"]
        T100["100 transactions\nTX_NNNNN"]
    end

    subgraph JOIN["Glue ETL Join"]
        J1["transactions\n(100 rows)"]
        J2["+ accounts\n(add account_type,\ncustomer_id)"]
        J3["+ customers\n(add name, country)"]
        J4["= enriched\n(≤100 rows after\ndedup + filter)"]
        J1 --> J2 --> J3 --> J4
    end

    subgraph DERIVE["Derived Fields"]
        D1["amount\n→ Decimal(10,2)"]
        D2["timestamp\n→ tx_date (Date)"]
        D3["fraud_flag\namount > 4000 → 'Y'"]
    end

    subgraph OUT["Output Table"]
        E["enriched_transactions\ntx_id | account_id | customer_id\nname | country | account_type\namount | tx_type | tx_date\nfraud_flag"]
    end

    C20 --> J3
    A20 --> J2
    T100 --> J1
    J4 --> D1 & D2 & D3
    D1 & D2 & D3 --> E
```

---

## FK Relationship Flow

```
customers.customer_id  (PK, 20 values)
    │
    │ referenced by
    ▼
accounts.customer_id   (FK → 20 unique values)
accounts.account_id    (PK, 20 values: ACC_001…ACC_020)
    │
    │ referenced by
    ▼
transactions.account_id  (FK → random 20 values, 100 rows total)
```
