from pathlib import Path
import json
import pandas as pd

REQUIRED_FUNCS = ["bold.nii", "desc-confounds_regressors.tsv"]
REQUIRED_JSON_KEYS = ["RepetitionTime"]

def _check_subject(sub_dir: Path) -> list[dict]:
    """Return list of issue-dicts for a single subject."""
    issues = []

    for sess in sub_dir.glob("ses-*"):
        func_dir = sess / "func"
        if not func_dir.exists():
            issues.append({"subject": sub_dir.name, "session": sess.name,
                           "file": "func dir", "problem": "missing"})
            continue
        # 1.look for NIfTI+TSV files
        for req in REQUIRED_FUNCS:
            if not any(func_dir.glob(f"*{req}*")):
                issues.append({"subject": sub_dir.name, "session": sess.name,
                               "file": req, "problem": "missing"})
        # 2.look for TR JSON
        for nii in func_dir.glob("*bold.nii*"):
            json_path = nii.with_suffix(".json")
            if json_path.exists():
                with open(json_path) as f:
                    meta = json.load(f)
                if "RepetitionTime" not in meta:
                    issues.append({"subject": sub_dir.name, "session": sess.name,
                                   "file": json_path.name, "problem": "no TR"})
            else:
                issues.append({"subject": sub_dir.name, "session": sess.name,
                               "file": json_path.name, "problem": "missing"})

    return issues

def validate_cohort(cohort_path: Path) -> pd.DataFrame:
    all_issues = []
    for sub in cohort_path.glob("sub-*"):
        all_issues.extend(_check_subject(sub))
    return pd.DataFrame(all_issues)
