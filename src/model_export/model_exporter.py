import joblib
import os


class ModelExporter:

    def export(

        self,

        model,

        model_name,

        feature_names=None,

        target_column=None,

        problem_type=None

    ):

        os.makedirs("saved_models", exist_ok=True)

        filename = f"saved_models/{model_name}.pkl"

        package = {

            "model": model,

            "feature_names": feature_names,

            "target_column": target_column,

            "problem_type": problem_type

        }

        joblib.dump(package, filename)

        return filename