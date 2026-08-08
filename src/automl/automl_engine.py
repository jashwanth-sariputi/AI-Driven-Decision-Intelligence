from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor
)

from sklearn.tree import (
    DecisionTreeClassifier,
    DecisionTreeRegressor
)

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression
)

from sklearn.metrics import (
    accuracy_score,
    r2_score
)

from pandas.api.types import (
    is_numeric_dtype
)


class AutoMLEngine:

    def __init__(self):

        self.problem_type = None
        self.best_model = None

    def compare_models(
        self,
        X_train,
        X_test,
        y_train,
        y_test
    ):

        results = {}

        # ---------------------------------------
        # Detect Problem Type
        # ---------------------------------------

        if (
            not is_numeric_dtype(y_train)
            or y_train.nunique() <= 20
        ):

            self.problem_type = "classification"

            models = {
                "Random Forest":
                    RandomForestClassifier(
                        n_estimators=100,
                        n_jobs=-1,
                        random_state=42
                    ),
                "Decision Tree":
                    DecisionTreeClassifier(
                        random_state=42
                    ),
                "Logistic Regression":
                    LogisticRegression(
                        max_iter=1000
                    ),
                "Gradient Boosting":
                    GradientBoostingClassifier(
                        n_estimators=50,
                        random_state=42
                    )
            }
        else:

            self.problem_type = "regression"

            models = {

                "Random Forest":
                    RandomForestRegressor(
                        random_state=42
                    ),

                "Decision Tree":
                    DecisionTreeRegressor(
                        random_state=42
                    ),

                "Linear Regression":
                    LinearRegression(),

                "Gradient Boosting":
                    GradientBoostingRegressor(
                        random_state=42
                    )

            }

        # ---------------------------------------
        # Train Models
        # ---------------------------------------

        best_score = -999

        for name, model in models.items():

            model.fit(
                X_train,
                y_train
            )

            prediction = model.predict(
                X_test
            )

            if self.problem_type == "classification":

                score = accuracy_score(
                    y_test,
                    prediction
                ) * 100

            else:

                score = r2_score(
                    y_test,
                    prediction
                ) * 100

            score = round(score, 2)

            results[name] = score

            if score > best_score:

                best_score = score

                self.best_model = model

        return results

    # ---------------------------------------
    # Feature Importance
    # ---------------------------------------

       # ---------------------------------------
    # Feature Importance
    # ---------------------------------------

    def feature_importance(
        self,
        feature_names
    ):

        if self.best_model is None:
            return None

        if hasattr(
            self.best_model,
            "feature_importances_"
        ):

            importance = self.best_model.feature_importances_

            return dict(
                zip(
                    feature_names,
                    importance
                )
            )

        return None