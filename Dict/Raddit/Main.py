# Main processing flow: Read → Classify → Report → Save

import pandas as pd
from classifier import classify_post
from config import INPUT_FILE, OUTPUT_FILE, SHEET_NAME, TITLE_COL, BODY_COL


# Load

def load_data(file_path: str, sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    print(f"Load Finished：{len(df)} records")
    return df


# Classifier

def run_classification(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the classifier for each record.
    If BODY_COL exists, combine the title and body for evaluation;
    If it does not exist, use only the title.
    """
    has_body = BODY_COL is not None and BODY_COL in df.columns

    if has_body:
        print(f"Text column detected '{BODY_COL}'，The title and body will be combined and categorized.")
        results = df.apply(
            lambda row: classify_post(row[TITLE_COL], row[BODY_COL]),
            axis=1
        )
    else:
        print(f"No main text column was detected; only '{TITLE_COL}' was used for categorization.")
        results = df[TITLE_COL].apply(lambda t: classify_post(t))

    df['Cleaned_Category'] = [r[0] for r in results]
    df['Classification_Reason'] = [r[1] for r in results]
    df['Confidence'] = [r[2] for r in results]

    # Keep indicator: Both category 1 and 2 are retained.
    df['Keep'] = df['Cleaned_Category'].isin([1, 2])

    print("Finshed")
    return df


# Statistical report

def generate_report(df: pd.DataFrame) -> dict:
    total = len(df)
    direct = (df['Cleaned_Category'] == 1).sum()
    indirect = (df['Cleaned_Category'] == 2).sum()
    unrelated = (df['Cleaned_Category'] == 0).sum()
    to_keep = df['Keep'].sum()
    to_delete = (~df['Keep']).sum()

    return {
        'total': total,
        'direct': direct,
        'indirect': indirect,
        'unrelated': unrelated,
        'to_keep': to_keep,
        'to_delete': to_delete,
        'direct_pct': direct / total * 100,
        'indirect_pct': indirect / total * 100,
        'unrelated_pct': unrelated / total * 100,
        'avg_confidence': df['Confidence'].mean(),
    }


def print_report(report: dict):
    print("\n" + "=" * 60)
    print("KIRUNA POST DATA CLEANING REPORT")
    print("=" * 60)
    print(f"Total: {report['total']}")
    print(f"\nResult：")
    print(f"1 - Directly related: {report['direct']:>5}  ({report['direct_pct']:.1f}%)")
    print(f"2 - Indirectly related: {report['indirect']:>5}  ({report['indirect_pct']:.1f}%)")
    print(f"0 - Unrelated: {report['unrelated']:>5}  ({report['unrelated_pct']:.1f}%)")
    print(f"\nRecommended operation：")
    print(f"Save(1+2): {report['to_keep']}")
    print(f"Del(0): {report['to_delete']}")
    print(f"\nAverage confidence level: {report['avg_confidence']:.2f}")
    print("=" * 60)


# Save

def save_results(df: pd.DataFrame, output_path: str):
    """
    Save 2 sheets:
    'All Posts': Full data (including category columns)
    'Kept Posts': Only retain data from categories 1 & 2 for direct use in subsequent analysis
    """
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='All Posts', index=False)
        df[df['Keep']].to_excel(writer, sheet_name='Kept Posts', index=False)

    print(f"\nSaved to：{output_path}")
    print(f"Sheet'All Posts': {len(df)} (total)")
    print(f"Sheet'Kept Posts': {df['Keep'].sum()} (only category 1 & 2）")


# Run
if __name__ == '__main__':
    print("=" * 60)
    print("  Kiruna Post Data Cleaning — Running")
    print("=" * 60 + "\n")

    df = load_data(INPUT_FILE, SHEET_NAME)
    df = run_classification(df)
    report = generate_report(df)
    print_report(report)
    save_results(df, OUTPUT_FILE)

    print("\nFinish")
