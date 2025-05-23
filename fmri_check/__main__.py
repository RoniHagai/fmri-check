"""
fmri-check CLI entry‐point – unified support for:
  • Single cohort (positional PATH)
  • Multi‐cohort scanning under a ROOT folder
  • Offline demo (--demo)

  python -m fmri_check .\demo_cohort -o demo_issues.csv

"""
from __future__ import annotations
import argparse
import os
from pathlib import Path
from importlib import resources
import pandas as pd
from validation import validate_cohort


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fmri-check",
        description="Validate one or more fMRIPrep cohorts."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run on built-in sample_data (offline demo; ignores PATH/ROOT)."
    )
    parser.add_argument(
        "--root",
        metavar="ROOT",
        help="Path to a parent folder containing multiple *_fmriprep cohorts."
    )
    parser.add_argument(
        "--md",
        metavar="REPORT.md",
        help="Save issues as a Markdown table."
    )
    parser.add_argument(
        "-o", "--out",
        metavar="REPORT.csv",
        help="Save issues as a CSV file."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to a single cohort folder (omit if using --demo or --root)."
    )

    args = parser.parse_args()
    if not args.demo and not args.root and args.path is None:
        parser.error("You must supply PATH, or --root, or --demo")
    return args


def main() -> None:
    args = parse_args()

    #  which cohort paths to scan
    if args.demo:
        # offline demo data bundled in the package
        cohort_paths = [resources.files("fmri_check") / "sample_data"]
    elif args.root:
        root = Path(args.root).expanduser().resolve()
        cohort_paths = [
            root / d for d in os.listdir(root)
            if d.endswith("_fmriprep") and (root / d).is_dir()
        ]
    else:
        cohort_paths = [Path(args.path).expanduser().resolve()]

    # collect results from all cohorts
    all_dfs: list[pd.DataFrame] = []
    for cohort_path in cohort_paths:
        cohort_name = cohort_path.name
        df = validate_cohort(cohort_path)
        if not df.empty:
            df = df.copy()
            df["cohort"] = cohort_name
        all_dfs.append(df)

    # concatenate into one DataFrame
    full_df = pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

    # summary output
    if full_df.empty:
        print("✅ No issues found!")
    else:
        total = len(full_df)
        print(f"❌ Found {total} issue{'s' if total != 1 else ''} across {len(cohort_paths)} cohort(s).")

    # save or print detailed report
    if not full_df.empty:
        if args.md:
            full_df.to_markdown(args.md, index=False)
            print(f"Markdown report saved to: {args.md}")
        elif args.out:
            full_df.to_csv(args.out, index=False)
            print(f"CSV report saved to: {args.out}")
        else:
            print(full_df.to_string(index=False))


if __name__ == "__main__":
    main()
