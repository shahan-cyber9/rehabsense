"""Session persistence for saving metrics to local storage."""

import pandas as pd
from datetime import datetime
from pathlib import Path


def save_session(record, path="data/sessions.csv"):
    """Saves a dictionary of session metrics to a CSV file."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    record["timestamp"] = datetime.now().isoformat(timespec="seconds")
    df = pd.DataFrame([record])

    if file_path.exists():
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)