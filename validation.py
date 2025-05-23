from pathlib import Path
import json
import pandas as pd

# files we expect to see in every func/ folder
REQUIRED_FUNCS = ["bold.nii", "desc-confounds_regressors.tsv"]
REQUIRED_JSON_KEYS = ["RepetitionTime"]


def _check_subject(sub_dir: Path) -> list[dict]:
    """
    Inspect a single subject folder for:
      1) missing func/ directory
      2) missing required files - confounds ect
      3) missing RepetitionTime in JSON file
    Returns a list of {subject, session, file, problem}.
    """
    issues: list[dict] = []

    for sess in sub_dir.glob("ses-*"):
        func_dir = sess / "func"
        if not func_dir.exists():
            issues.append({
                "subject": sub_dir.name,
                "session": sess.name,
                "file": "func dir",
                "problem": "missing"
            })
            continue

        # 1) required files
        for req in REQUIRED_FUNCS:
            if not any(func_dir.glob(f"*{req}*")):
                issues.append({
                    "subject": sub_dir.name,
                    "session": sess.name,
                    "file": req,
                    "problem": "missing"
                })

        # 2) look for TR in each bold JSON
        for nii in func_dir.glob("*bold.nii*"):
            json_path = nii.with_suffix(".json")
            if json_path.exists():
                with open(json_path, "r") as f:
                    meta = json.load(f)
                if "RepetitionTime" not in meta:
                    issues.append({
                        "subject": sub_dir.name,
                        "session": sess.name,
                        "file": json_path.name,
                        "problem": "no TR"
                    })
            else:
                issues.append({
                    "subject": sub_dir.name,
                    "session": sess.name,
                    "file": json_path.name,
                    "problem": "missing"
                })

    return issues


def validate_cohort(cohort_path: Path) -> pd.DataFrame:
    """
    Validate every sub-*/ses-* under the given cohort_path.
    Returns a DataFrame of all issues.
    """
    all_issues: list[dict] = []
    for sub in cohort_path.glob("sub-*"):
        all_issues.extend(_check_subject(sub))
    return pd.DataFrame(all_issues)
