# fmri-check
repo: https://github.com/RoniHagai/fmri-check.git

Lightweight **CLI tool** for quick sanity-checks on *fMRIPrep* cohorts:
flags missing NIfTIs, confounds TSVs, and absent **RepetitionTime** in JSON files.

## ✨ Features
- Walks every `sub-*/ses-*` folder and applies configurable rules  
- Outputs **Markdown** or **CSV** report (`--md | -o`)  



```bash
# clone & install
git clone https://github.com/RoniHagai/fmri-check.git
cd fmri-check
pip install -e .

# run on your cohort
python -m fmri_check /path/to/ayelet_fmriprep -o issues.csv

# offline demo
python -m fmri_check --demo --md demo.md


fmri-check/
├─ fmri_check/          # Python package
│  ├─ validator.py
│  ├─ sample_data/…     # built-in demo cohort
│  └─ __main__.py       # CLI entry-point
├─ tests/               # pytest tests
├─ .github/workflows/   # CI definition (pytest on push)
└─ README.md            # you are here

