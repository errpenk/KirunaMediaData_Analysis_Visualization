
import argparse
from reply_pipeline import load_data, run_pipeline, save_data, print_report


def parse_args():
    parser = argparse.ArgumentParser(description="Kiruna reply filter")
    parser.add_argument("--input",  default="kiruna_raw_data.xlsx",          help="Input Excel file")
    parser.add_argument("--sheet",  default="reply data",                    help="Sheet name")
    parser.add_argument("--output", default="kiruna_reply_data_cleaned.xlsx", help="Output Excel file")
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print("  Kiruna Reply Data Cleaning Workflow")
    print("=" * 60)

    print("\n[1/4] Loading data")
    df = load_data(args.input, sheet_name=args.sheet)

    print("\n[2/4] Running pipeline")
    df_annotated, df_deleted = run_pipeline(df)

    print("\n[3/4] Report")
    print_report(df, df_annotated, df_deleted)

    print("\n[4/4] Saving results")
    save_data(df_annotated, df_deleted, args.output)

    print("\nDone")


if __name__ == "__main__":
    main()
