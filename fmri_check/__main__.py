"""
Entry-point for the fmri-check CLI:
    python -m fmri_check <PATH> [options]

Examples
--------
# הרצה על תקייה אמיתית ושמירת דו"ח CSV
python -m fmri_check K:\ayelet_fmriprep -o issues.csv

# דמו אופליין על sample_data בתוך החבילה, ושמירת דו"ח Markdown
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

    # דגל דמו – מריץ על נתוני הדוגמה המובנים בחבילה
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run validation on the built-in sample_data (ignore PATH)."
    )

    # שמירת דו״ח Markdown
    parser.add_argument(
        "--md",
        metavar="REPORT.md",
        help="Save issues as a Markdown table."
    )

    # שמירת דו״ח CSV (שם-קיצור אופציונלי נשמר מהגרסה הראשונה)
    parser.add_argument(
        "-o", "--out",
        metavar="REPORT.csv",
        help="Save issues as a CSV file."
    )

    # נתיב התקייה – נהיה אופציונלי (nargs='?') כי אפשר להשתמש ב---demo
    parser.add_argument(
        "path",
        nargs="?",
        help="Path to a cohort folder (omit if you use --demo)."
    )

    args = parser.parse_args()

    # ולידציה ידנית: חייבים או PATH או --demo
    if not args.demo and args.path is None:
        parser.error("You must supply PATH or use --demo")

    return args


def main() -> None:
    args = parse_args()

    # קובעים את הנתיב לבדיקה
    if args.demo:
        cohort_path = resources.files("fmri_check") / "sample_data"
    else:
        cohort_path = Path(args.path).expanduser().resolve()

    # הרצת הבדיקות
    issues_df = validate_cohort(cohort_path)

    # תוצאות
    if issues_df.empty:
        print("✅ No issues found!")
    else:
        print(f"❌ Found {len(issues_df)} issues.")

        # סדר עדיפויות: Markdown > CSV > הדפסה למסך
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
