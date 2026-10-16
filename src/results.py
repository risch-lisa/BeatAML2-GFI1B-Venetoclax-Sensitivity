import pandas as pd


def extract_regression_results(model):
    """Extract regression results from model"""
    results = pd.DataFrame({
        "term": model.params.index,
        "coefficient": model.params,
        "r_squared": model.rsquared,
        "std_error": model.bse,
        "p_value": model.pvalues,
        "ci_lower": model.conf_int()[0],
        "ci_upper": model.conf_int()[1],
    })

    return results[results["term"] != "Intercept"].reset_index(drop=True)

def create_results_table(models: dict):
    """Create results table with regression results from models in dict and add their name in the first column"""
    results = list()
    for name, model in models.items():
        result_df = extract_regression_results(model)
        result_df.insert(0, "model", name)
        results.append(result_df)

    return pd.concat(results)