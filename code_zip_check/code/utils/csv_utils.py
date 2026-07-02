"""
csv_utils.py

Helpers for reading input CSVs and writing the final output.csv.
"""
import pandas as pd


def load_claims(path: str) -> pd.DataFrame:
    """Load claims.csv or sample_claims.csv."""
    raise NotImplementedError


def load_user_history(path: str) -> dict[str, dict]:
    """
    Load user_history.csv and return a dict keyed by user_id
    for O(1) lookup during processing.
    """
    raise NotImplementedError


def load_requirements(path: str) -> list[dict]:
    """Load evidence_requirements.csv as a list of row dicts."""
    raise NotImplementedError


def write_output(rows: list[dict], path: str) -> None:
    """
    Write the list of output row dicts to output.csv
    with columns in the required order.
    """
    raise NotImplementedError
