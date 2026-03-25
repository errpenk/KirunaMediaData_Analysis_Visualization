
# Entry point for Kiruna reply data cleaning

import argparse
import pandas as pd
from reply_pipeline import load_data, run_pipeline, save_data, print_report


def parse_args():
    parser = argparse.ArgumentParser(description="Kiruna reply filter")
    parser.add_argument("--input",          default="kiruna_replies.xlsx",         help="Input Excel file")
    parser.add_argument("--sheet",          default="reply data",                  help="Sheet name")
    parser.add_argument("--col",            default="Title/Description",           help="Content column name")
    parser.add_argument("--output-kept",    default="kiruna_replies_kept.xlsx",    help="Output file for kept replies")
    parser.add_argument("--output-deleted", default="kiruna_replies_deleted.xlsx", help="Output file for deleted replies")
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print("  Kiruna Reply Filter")
    print("=" * 60)

    print("\n[1/4] Loading data")
    df = load_data(args.input, sheet_name=args.sheet)

    print("\n[2/4] Classifying replies")
    df_kept, df_deleted = run_pipeline(df, content_col=args.col)

    print("\n[3/4] Report")
    print_report(df, df_kept, df_deleted)

    print("\n[4/4] Saving results")
    save_data(df_kept,    args.output_kept)
    save_data(df_deleted, args.output_deleted)

    print("\nDone")


if __name__ == "__main__":
    main()
