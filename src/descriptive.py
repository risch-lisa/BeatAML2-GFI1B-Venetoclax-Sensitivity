import pandas as pd


def create_sample_overview(data: pd.DataFrame, patient_col: str = "dbgap_subject_id",
                           sample_col: str = "dbgap_rnaseq_sample",) -> pd.DataFrame:
    """Summarize the number of rows, samples, and patients"""
    return pd.DataFrame(
        {
            "metric": [
                "Zeilen",
                "n Samples",
                "n Patienten",
            ],
            "value": [
                len(data),
                data[sample_col].nunique(),
                data[patient_col].nunique(),
            ],
        }
    )

def create_missing_values_table(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Summarize missing values and their percentages"""
    missing = data[columns].isna().sum()

    return pd.DataFrame(
        {
            "missing n": missing,
            "missing percent": (missing / len(data) * 100).round(1),
        }
    ).sort_values("missing n", ascending=False)

def create_numeric_summary(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Calculate descriptive statistics for numeric variables."""
    numeric = data[columns].apply(pd.to_numeric, errors="coerce")

    summary = numeric.describe().T
    summary["median"] = numeric.median()
    summary["IQR"] = (
        numeric.quantile(0.75) - numeric.quantile(0.25)
    )

    return summary

def create_categorical_summary(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Calculate counts and percentages for a categorical variable"""
    counts = data[column].value_counts(dropna=False)

    return pd.DataFrame(
        {
            "n": counts,
            "percent": (counts / len(data) * 100).round(1),
        }
    )