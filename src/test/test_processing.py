import pandas as pd

from src.processing import merge_data


def test_merge_data_inner_join():
    left = pd.DataFrame({
        "dbgap_subject_id": ["P1", "P2"],
        "dbgap_rnaseq_sample": ["S1", "S2"],
        "x": [10, 20],
    })
    right = pd.DataFrame({
        "dbgap_subject_id": ["P1"],
        "dbgap_rnaseq_sample": ["S1"],
        "y": [1.5],
    })
    summary = pd.DataFrame(
        columns=["n Samples", "n Patienten", "n RNA Seq"]
    )

    merged, updated_summary = merge_data(
        left, right,
        ["dbgap_subject_id", "dbgap_rnaseq_sample"],
        summary, "Test", inner=True
    )

    assert len(merged) == 1
    assert merged["dbgap_subject_id"].tolist() == ["P1"]
    assert updated_summary.loc["Test", "n Samples"] == 1
    assert updated_summary.loc["Test", "n Patienten"] == 1

