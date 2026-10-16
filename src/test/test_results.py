import statsmodels.api as sm
import pandas as pd

from src.results import extract_regression_results, create_results_table


def test_extract_regression_results():
    X = pd.DataFrame({"GFI1B": [1, 2, 3, 4, 5]})
    X = sm.add_constant(X)
    y = pd.Series([10, 9, 8, 7, 6])

    model = sm.OLS(y, X).fit()
    results = extract_regression_results(model)

    assert "Intercept" not in results["term"].values
    assert "GFI1B" in results["term"].values
    assert {
        "coefficient", "std_error", "p_value",
        "ci_lower", "ci_upper", "r_squared"
    }.issubset(results.columns)


def test_create_results_table():
    X = sm.add_constant(pd.DataFrame({"GFI1B": [1, 2, 3, 4, 5]}))
    y = pd.Series([10, 9, 8, 7, 6])
    model = sm.OLS(y, X).fit()

    results = create_results_table({
        "unadjusted": model,
        "adjusted": model,
    })

    assert set(results["model"]) == {"unadjusted", "adjusted"}
    assert len(results) == 4
    assert set(results["term"]) == {"GFI1B", "const"}
    assert (results.groupby("model").size() == 2).all()
