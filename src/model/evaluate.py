import numpy as np
import polars as pl
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error,
    r2_score,
    explained_variance_score
)


def evaluate(name, y_pred, y_true):
    df = {
        "Model": name,
        "MSE": round(mean_squared_error(y_true, y_pred), 4),
        "MAE": round(mean_absolute_error(y_true, y_pred), 4),
        "MAPE": round(mean_absolute_percentage_error(y_true, y_pred), 4),
        "R2": round(r2_score(y_true, y_pred), 4),
        "Exp Var": round(explained_variance_score(y_true, y_pred), 4)
    }
    return pl.DataFrame(df)


if __name__ == "__main__":
    y_pred = np.array([1, 2, 3, 4, 5])
    y_true = np.array([1.1, 2.2, 3.3, 4.2, 5])
    print(evaluate("OK", y_pred, y_true))
