import argparse
from pipeline import load_data, run_pipeline, save_data, print_report


def parse_args():
    parser = argparse.ArgumentParser(description="Kiruna post filter")
    parser.add_argument("--input",  default="kiruna_posts.xlsx",  help="Input Excel file")
    parser.add_argument("--sheet",  default="post data",          help="Sheet name")
    parser.add_argument("--col",    default="Title/Description",  help="Content column name")
    parser.add_argument(
        "--output-class1",  default="kiruna_class1_direct.xlsx",
        help="Output file for Classification 1 (directly related)",
    )
    parser.add_argument(
        "--output-class2",  default="kiruna_class2_indirect.xlsx",
        help="Output file for Classification 2 (indirectly related)",
    )
    parser.add_argument(
        "--output-deleted", default="kiruna_deleted.xlsx",
        help="Output file for deleted posts (with reason)",
    )
    parser.add_argument(
        "--output-combined", default="kiruna_posts_cleaned.xlsx",
        help="Output file combining class 1 + class 2",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print("  Kiruna Post Filter")
    print("=" * 60)

    print(f"\n[1/4] Loading data …")
    df = load_data(args.input, sheet_name=args.sheet)

    print(f"\n[2/4] Classifying posts …")
    df_class1, df_class2, df_deleted = run_pipeline(df, content_col=args.col)

    print(f"\n[3/4] Report")
    print_report(df, df_class1, df_class2, df_deleted)

    print(f"\n[4/4] Saving results …")
    save_data(df_class1,  args.output_class1)
    save_data(df_class2,  args.output_class2)
    save_data(df_deleted, args.output_deleted)

    import pandas as pd
    df_combined = pd.concat([df_class1, df_class2], ignore_index=True)
    save_data(df_combined, args.output_combined)

    print("\nDone ✓")


if __name__ == "__main__":
    main()
