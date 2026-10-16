import pandas as pd
from pathlib import Path
from typing import Tuple


def read_txt_file(filename: str) -> pd.DataFrame:
    return pd.read_csv(Path("data") / filename, sep="\t")

def read_excel(filename: str) -> pd.DataFrame:
    return pd.read_excel(Path("data") / filename, sheet_name=0)

def data_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns summary of dtype, n and percent missing and n unique values for each column in df.
    :param df:
    :return: summary
    """
    summary = pd.DataFrame({
        "dtype": df.dtypes,
        "n missing": df.isna().sum(),
        "p% missing": (df.isna().mean() * 100).round(2),
        "n unique": df.nunique(dropna=True)
    }).T
    return summary

def id_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns summary of n patients and n RNA seq in df.
    :param df:
    :return: summary
    """
    summary = pd.DataFrame({
        "n Patienten": [len(df.dbgap_subject_id.unique())],
        "n RNA Seq": [len(df.dbgap_rnaseq_sample.unique())],
    }, index=["Anzahl"]).T
    return summary


def get_sample_summary(sample_df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns summary of n samples, n patients and n RNA seq in sample-df with named index to be used for merge summary
    collection.
    :param sample_df:
    :return:
    """
    return pd.DataFrame({"n Samples": [len(sample_df)],
                         "n Patienten": [sample_df["dbgap_subject_id"].nunique()],
                         "n RNA Seq": [sample_df["dbgap_rnaseq_sample"].nunique()]}, index=["Sample-IDs"])

def merge_data(df_left: pd.DataFrame, df_right: pd.DataFrame, merge_ids: list[str], merge_summary: pd.DataFrame,
               name: str, inner: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """

    :param df_left:
    :param df_right:
    :param merge_ids: IDs to merge dfs on
    :param merge_summary: df containing columns 'n Samples', 'n Patienten', 'n RNA Seq' for collecting merge info
    :param name: name given to index of new row in merge_summary
    :param inner: type of merge operation, True if inner, False if left
    :return: merge summary
    """
    df_merged = pd.merge(df_left, df_right, how="inner" if inner else "left", on=merge_ids)

    summary = {"n Samples": len(df_merged),
               "n Patienten": df_merged["dbgap_subject_id"].nunique(),
               "n RNA Seq": df_merged["dbgap_rnaseq_sample"].nunique()}

    merge_summary = pd.concat([merge_summary, pd.DataFrame(summary, index=[name])])

    return df_merged, merge_summary

