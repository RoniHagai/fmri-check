"""
Entry-point for the fmri-check CLI:


Examples
--------
real data:
python -m fmri_check K:\ayelet_fmriprep -o issues.csv

demo data:
python -m fmri_check --demo --md report.md
"""
from __future__ import annotations
import argparse
from pathlib import Path
from importlib import resources

from validation import validate_cohort


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="fmri-check",
        description="Validate an fMRIPrep cohort directory."
    )

    # demo flag
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run validation on the built-in sample_data (ignore PATH)."
    )

    # save Markdown
    parser.add_argument(
        "--md",
        metavar="REPORT.md",
        help="Save issues as a Markdown table."
    )

    # save CSV
    parser.add_argument(
        "-o", "--out",
        metavar="REPORT.csv",
        help="Save issues as a CSV file."
    )

    #
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to a cohort folder (omit if you use --demo)."
    )

    args = parser.parse_args()

    #
    if not args.demo and args.path is None:
        parser.error("You must supply PATH or use --demo")

    return args


def main() -> None:
    args = parse_args()

    # set path for check
    if args.demo:
        cohort_path = resources.files("fmri_check") / "sample_data"
    else:
        cohort_path = Path(args.path).expanduser().resolve()

    # check
    issues_df = validate_cohort(cohort_path)

    # results
    if issues_df.empty:
        print("✅ No issues found!")
    else:
        print(f"❌ Found {len(issues_df)} issues.")


        if args.md:
            issues_df.to_markdown(args.md, index=False)
            print(f"Markdown report saved to: {args.md}")
        elif args.out:
            issues_df.to_csv(args.out, index=False)
            print(f"CSV report saved to: {args.out}")
        else:
            print(issues_df.to_string(index=False))


if __name__ == "__main__":
    main()
