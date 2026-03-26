
import pandas as pd
from pathlib import Path


def load_input(path: str) -> pd.DataFrame: # csv and xlsx
    ext = Path(path).suffix.lower()
    if ext == ".csv":
        for enc in ("utf-8", "utf-8-sig", "gbk", "latin-1"):
            try:
                return pd.read_csv(path, encoding=enc)
            except UnicodeDecodeError:
                continue
        raise ValueError("Unable to read CSV file. Please specify the encoding manually.")
    elif ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Please use CSV or XLSX.")
