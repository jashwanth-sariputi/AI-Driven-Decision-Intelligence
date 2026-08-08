from sklearn.linear_model import LinearRegression
import numpy as np


class ForecastEngine:

    def forecast(
        self,
        dataframe,
        target_column,
        periods=30
    ):

        data = dataframe.copy()

        data = data.dropna(subset=[target_column])

        y = data[target_column].values

        X = np.arange(len(y)).reshape(-1, 1)

        model = LinearRegression()

        model.fit(X, y)

        future_x = np.arange(
            len(y),
            len(y) + periods
        ).reshape(-1, 1)

        future_prediction = model.predict(future_x)

        return future_prediction