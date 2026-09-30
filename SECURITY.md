# Security Policy

## Overview

This repository contains no real credentials, no real customer data, and
no private infrastructure identifiers. All datasets are fully synthetic.

---

## What Must NEVER Be Committed

The following must **never** be committed to this repository:

| Type | Examples |
|---|---|
| AWS Access Keys | `AKIAIOSFODNN7EXAMPLE` |
| AWS Secret Keys | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| AWS Account IDs | `123456789012` |
| IAM Role ARNs | `arn:aws:iam::123456789012:role/MyRole` |
| S3 Bucket names with account suffixes | `banking-raw-data-narendar` |
| Private key files | `*.pem`, `*.key` |
| AWS credential files | `~/.aws/credentials` |
| Environment files | `.env` |
| Personal filesystem paths | `C:/Users/yourname/Documents/...` |
| Real customer data | Any PII |
| Passwords or tokens | Any authentication secret |

---

## What This Repository Contains

✅ Fully synthetic CSV data (no real persons, no real transactions)  
✅ Python scripts using relative paths only  
✅ SQL queries using placeholder table names  
✅ Infrastructure documentation with `<your-suffix>` placeholders  
✅ `.env.example` with placeholder values (no real credentials)  
✅ `.gitignore` blocking sensitive file patterns

---

## Configuration

AWS configuration is managed via environment variables. Copy `.env.example`
to `.env` and populate with your values:

```bash
cp .env.example .env
# Edit .env with your actual values
# NEVER commit .env to version control
```

---

## .gitignore

The `.gitignore` in this repository blocks:

- `.env` files
- `*.pem`, `*.key` certificate/key files
- `credentials` files
- Python cache and virtual environments
- Jupyter notebook checkpoints

---

## Reporting Security Issues

If you discover a security issue or accidentally committed credentials:

1. **Immediately revoke** any exposed AWS keys in the AWS IAM console
2. **Rotate** all potentially exposed credentials
3. Open a GitHub Issue (do not include the credential in the issue)
4. If sensitive data was committed to git history, consider:
   - `git filter-branch` or `git filter-repo` to rewrite history
   - GitHub's [secret scanning](https://docs.github.com/en/code-security/secret-scanning) to detect leaks

---

## Synthetic Data Disclaimer

All data in `data/sample/` is algorithmically generated using Python's `random`
module with no connection to real individuals, real bank accounts, or real
financial transactions. No PII is present.
