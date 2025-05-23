from pathlib import Path
from validation import validate_cohort

def test_empty_sample(tmp_path: Path):
    sample = Path(__file__).parent.parent / "sample_data"
    cohort = tmp_path / "demo"
    cohort.mkdir()
    for item in sample.rglob("*"):
        dest = cohort / item.relative_to(sample)
        if item.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
        else:
            dest.write_bytes(item.read_bytes())

    df = validate_cohort(cohort)
    assert df.empty
