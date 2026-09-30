# Bank_Analytics_Project.ipynb (Placeholder)

The original Jupyter Notebook `Bank_Analytics_Project.ipynb` should be placed
in this directory.

## Why This Placeholder Exists

The original notebook was provided as a project artifact but contains:

- A **hardcoded personal Windows filesystem path** that must not be committed
  to a public repository
- Personal directory references (e.g., `C:/Users/sreevarshith/...`)

## How to Add the Notebook

Before committing the notebook to this repository:

1. Open `Bank_Analytics_Project.ipynb` in Jupyter
2. Remove or replace the hardcoded path:
   ```python
   # BEFORE (do not commit):
   output_path = "C:/Users/sreevarshith/Documents/AWS/Bank_Datasets/"
   
   # AFTER (safe for public repo):
   output_path = "data/sample/"
   ```
3. Clear all cell outputs (Kernel → Restart & Clear Output)
4. Save the notebook
5. Place it at: `notebooks/Bank_Analytics_Project.ipynb`

## Refactored Version

The data generation logic has been refactored into a standalone script:

```
src/data_generation/generate_banking_data.py
```

This script:
- Uses a relative output path (`data/sample/` by default)
- Supports CLI arguments (`--records`, `--output`)
- Is importable as a Python module
- Has no personal filesystem paths

The notebook is preserved as a reference artifact showing the original
implementation context.
