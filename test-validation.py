from pathlib import Path
from validation import validate_cohort

from pathlib import Path
from validation import validate_cohort

def test_empty_sample():
    sample_path = Path(__file__).parent.parent / "sample_data"
    df = validate_cohort(sample_path)
    assert df.empty
