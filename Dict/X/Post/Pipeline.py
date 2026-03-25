
# Data loading, cleaning, and export

import pandas as pd
from classifier import classify




def load_data(file_path: str, sheet_name: str = "post data") -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(f"Loaded {len(df):,} rows from '{sheet_name}'")
    return df


def save_data(df: pd.DataFrame, file_path: str) -> None:
    df.to_excel(file_path, index=False)
    print(f"Saved {len(df):,} rows → {file_path}")


# cleaning pipeline

def run_pipeline(
    df: pd.DataFrame,
    content_col: str = "Title/Description",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Classify every post and split into three DataFrames.

    Returns
    -------
    df_class1  : Classification 1 (directly related)
    df_class2  : Classification 2 (indirectly related)
    df_deleted : Classification 0 (deleted) with reason column
    """
    labels, reasons = [], []
    for text in df[content_col]:
        label, reason = classify(text)
        labels.append(label)
        reasons.append(reason)

    df = df.copy()
    df["_label"]  = labels
    df["_reason"] = reasons

    # ── secondary noise filter: drop rows ≤ 1 meaningful char ──
    def too_short(text):
        return pd.isna(text) or len(str(text).strip()) <= 1

    df.loc[df[content_col].apply(too_short) & (df["_label"] != 0), "_label"] = 0
    df.loc[df[content_col].apply(too_short) & (df["_reason"] == ""), "_reason"] = "too short"

    # split
    df_class1 = df[df["_label"] == 1].drop(columns=["_label", "_reason"]).reset_index(drop=True)
    df_class2 = df[df["_label"] == 2].drop(columns=["_label", "_reason"]).reset_index(drop=True)
    df_deleted = df[df["_label"] == 0].drop(columns=["_label"]).rename(
        columns={"_reason": "Deletion_Reason"}
    ).reset_index(drop=True)

    return df_class1, df_class2, df_deleted


# reporting

def print_report(df_orig, df_class1, df_class2, df_deleted):
    total = len(df_orig)
    kept = len(df_class1) + len(df_class2)
    print("\n" + "=" * 60)
    print(f"Total posts: {total:>6,}")
    print(f"Classification 1: {len(df_class1):>6,}  ({len(df_class1)/total*100:.1f}%)")
    print(f"Classification 2: {len(df_class2):>6,}  ({len(df_class2)/total*100:.1f}%)")
    print(f"Kept (1 + 2) : {kept:>6,}  ({kept/total*100:.1f}%)")
    print(f"Deleted (0) : {len(df_deleted):>6,}  ({len(df_deleted)/total*100:.1f}%)")
    print("=" * 60)

    print("\nDeletion breakdown")
    print(df_deleted["Deletion_Reason"].value_counts().to_string())
    print()
