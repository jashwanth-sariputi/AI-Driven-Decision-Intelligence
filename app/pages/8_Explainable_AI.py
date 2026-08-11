import streamlit as st
import os
import sys
import pickle
import traceback
from datetime import datetime
import pandas as pd
import numpy as np

# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Explainable AI | Nex Decision AI",
    page_icon="🔎",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "username" not in st.session_state:
    st.session_state.username = "Guest"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

if "login_time" not in st.session_state:
    st.session_state.login_time = datetime.now()


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at top left,
            #142c50 0%,
            #071322 38%,
            #050d18 100%
        );

    color: #ffffff;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ============================================================
   PAGE TITLE
   ============================================================ */

.page-title {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 5px;
    letter-spacing: -1px;
}

.page-subtitle {
    font-size: 18px;
    color: #8fbaf0;
    margin-bottom: 28px;
}


/* ============================================================
   USER CARD
   ============================================================ */

.user-card {
    width: 100%;
    box-sizing: border-box;

    background:
        linear-gradient(
            135deg,
            #102d55,
            #153c70
        );

    border: 1px solid #285b91;
    border-radius: 16px;

    padding: 20px 24px;

    margin-bottom: 28px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.22);
}

.user-name {
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 6px;
}

.user-detail {
    font-size: 14px;
    color: #a9c8ec;
}


/* ============================================================
   SECTION TITLE
   ============================================================ */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #ffffff;
    margin-top: 22px;
    margin-bottom: 8px;
}

.section-description {
    font-size: 15px;
    color: #8fbaf0;
    margin-bottom: 15px;
}


/* ============================================================
   MODEL SELECTOR
   ============================================================ */

div[data-baseweb="select"] > div {
    background: #202532 !important;
    border: 1px solid #315d91 !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] * {
    color: #ffffff !important;
}


/* ============================================================
   MODEL INFORMATION CARD
   ============================================================ */

.model-info-card {

    width: 96%;
    margin: 24px auto 30px auto;

    background:
        linear-gradient(
            145deg,
            #102d55,
            #173e73
        );

    border: 1px solid #2b6299;

    border-radius: 17px;

    padding: 22px 26px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.25);

    box-sizing: border-box;
}


/* Smaller title */

.model-info-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 18px;
}


/* Wider grid */

.model-info-grid {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 14px;

    width: 100%;
}


/* Individual information item */

.model-info-item {

    background: rgba(255,255,255,0.055);

    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 11px;

    padding: 14px 15px;

    min-height: 78px;

    box-sizing: border-box;
}


/* Smaller labels */

.model-info-label {

    font-size: 12px;

    color: #8fbaf0;

    margin-bottom: 6px;

    font-weight: 500;
}


/* Smaller values */

.model-info-value {

    font-size: 15px;

    color: #ffffff;

    font-weight: 650;

    word-break: break-word;
}


/* ============================================================
   EXPLAINABILITY CARD
   ============================================================ */

.explain-card {

    width: 96%;

    margin: 20px auto;

    background:
        linear-gradient(
            145deg,
            #0e274b,
            #123764
        );

    border: 1px solid #285d94;

    border-radius: 17px;

    padding: 24px;

    box-sizing: border-box;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

.metric-grid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 15px;

    margin-top: 18px;
}

.metric-card {

    background: rgba(255,255,255,0.055);

    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 12px;

    padding: 18px;

    text-align: center;
}

.metric-label {

    font-size: 12px;

    color: #8fbaf0;

    margin-bottom: 7px;
}

.metric-value {

    font-size: 24px;

    font-weight: 750;

    color: #ffffff;
}


/* ============================================================
   INFO BOX
   ============================================================ */

.info-box {

    background: rgba(40, 103, 164, 0.18);

    border: 1px solid #285d94;

    border-radius: 12px;

    padding: 16px 18px;

    margin-top: 18px;

    color: #b9d4f3;

    font-size: 14px;

    line-height: 1.6;
}


/* ============================================================
   SUCCESS / WARNING / ERROR
   ============================================================ */

div[data-testid="stAlert"] {
    border-radius: 10px;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton > button {

    border-radius: 9px;

    border: 1px solid #3477c1;

    background: #2563eb;

    color: white;

    font-weight: 650;
}

.stButton > button:hover {

    background: #1d4ed8;

    border-color: #4c8ed8;
}


/* ============================================================
   RESPONSIVE
   ============================================================ */

@media (max-width: 900px) {

    .model-info-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

    .metric-grid {
        grid-template-columns:
            1fr;
    }

}

@media (max-width: 600px) {

    .model-info-grid {
        grid-template-columns:
            1fr;
    }

    .page-title {
        font-size: 32px;
    }

}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def render_html(html):
    """
    Render HTML safely without Streamlit interpreting
    the indented HTML as a code block.
    """
    import textwrap

    clean_html = textwrap.dedent(html).strip()

    st.markdown(
        clean_html,
        unsafe_allow_html=True
    )


def find_model_directory():
    """
    Look for common model directories.
    """

    possible_directories = [

        os.path.join(PROJECT_ROOT, "models"),

        os.path.join(PROJECT_ROOT, "model"),

        os.path.join(PROJECT_ROOT, "app", "models"),

        os.path.join(PROJECT_ROOT, "data", "models"),

    ]

    for directory in possible_directories:

        if os.path.exists(directory):

            return directory

    return None


def get_model_files():
    """
    Find available pickle/joblib models.
    """

    files = []

    model_directory = find_model_directory()

    if model_directory:

        for filename in os.listdir(model_directory):

            if filename.lower().endswith(
                (".pkl", ".pickle", ".joblib")
            ):

                files.append(
                    os.path.join(
                        model_directory,
                        filename
                    )
                )

    # Also check project root
    for root, dirs, filenames in os.walk(PROJECT_ROOT):

        # Avoid scanning virtual environment
        dirs[:] = [
            d for d in dirs
            if d not in [
                ".venv",
                "venv",
                "__pycache__",
                ".git"
            ]
        ]

        for filename in filenames:

            if filename.lower().endswith(
                (".pkl", ".pickle", ".joblib")
            ):

                path = os.path.join(
                    root,
                    filename
                )

                if path not in files:

                    files.append(path)

    return files


def load_model(path):
    """
    Load pickle/joblib model.
    """

    try:

        if path.lower().endswith(".joblib"):

            import joblib

            return joblib.load(path)

        with open(path, "rb") as file:

            return pickle.load(file)

    except Exception:

        return None


def get_model_name(model):
    """
    Determine model algorithm.
    """

    if model is None:

        return "Unknown"

    # Pipeline
    if hasattr(model, "steps"):

        try:

            final_model = model.steps[-1][1]

            return type(final_model).__name__

        except Exception:

            pass

    return type(model).__name__


def get_problem_type(model):
    """
    Estimate problem type from model.
    """

    if model is None:

        return "Unknown"

    name = type(model).__name__.lower()

    if hasattr(model, "steps"):

        try:

            name = type(
                model.steps[-1][1]
            ).__name__.lower()

        except Exception:

            pass

    classification_words = [
        "classifier",
        "classification",
        "logistic"
    ]

    regression_words = [
        "regressor",
        "regression",
        "linearregression",
        "randomforestregressor",
        "decisiontreeregressor",
        "gradientboostingregressor"
    ]

    if any(
        word in name
        for word in classification_words
    ):

        return "Classification"

    if any(
        word in name
        for word in regression_words
    ):

        return "Regression"

    return "Unknown"


def get_feature_count(model):

    if model is None:

        return "Unknown"

    if hasattr(model, "n_features_in_"):

        return str(
            model.n_features_in_
        )

    if hasattr(model, "feature_names_in_"):

        return str(
            len(model.feature_names_in_)
        )

    if hasattr(model, "steps"):

        try:

            final_model = model.steps[-1][1]

            if hasattr(
                final_model,
                "n_features_in_"
            ):

                return str(
                    final_model.n_features_in_
                )

        except Exception:

            pass

    return "Unknown"


def get_target_column(model):

    """
    Try to obtain target column information.
    """

    possible_attributes = [
        "target_column",
        "target",
        "target_name",
        "y_name"
    ]

    for attribute in possible_attributes:

        if hasattr(model, attribute):

            value = getattr(
                model,
                attribute
            )

            if value:

                return str(value)

    return "Unknown"


# ============================================================
# PAGE HEADER
# ============================================================

render_html(
    """
    <div class="page-title">
        🔎 Explainable AI
    </div>

    <div class="page-subtitle">
        Understand how your machine learning model makes predictions.
    </div>
    """
)


# ============================================================
# USER INFORMATION
# ============================================================




# ============================================================
# MODEL SELECTION
# ============================================================

render_html(
    """
    <div class="section-title">
        🤖 Select Model
    </div>

    <div class="section-description">
        Choose a trained model to understand its predictions.
    </div>
    """
)


model_files = get_model_files()


if not model_files:

    st.warning(
        "No trained models were found."
    )

    st.info(
        "Train a model first from the AutoML or Prediction section."
    )

    st.stop()


model_names = [
    os.path.basename(path)
    for path in model_files
]


selected_name = st.selectbox(
    "Choose a trained model",
    model_names
)


selected_path = model_files[
    model_names.index(selected_name)
]


model = load_model(
    selected_path
)


# ============================================================
# MODEL INFORMATION
# ============================================================

model_name = get_model_name(model)

problem_type = get_problem_type(model)

feature_count = get_feature_count(model)

target_column = get_target_column(model)



# ============================================================
# EXPLAINABILITY DASHBOARD
# ============================================================

render_html(
    """
    <div class="section-title">
        📈 Explainability Dashboard
    </div>

    <div class="section-description">
        SHAP-based explanations help identify which features
        influence model predictions.
    </div>
    """
)


# ============================================================
# FIND DATASET
# ============================================================

dataset = None

possible_dataset_directories = [

    os.path.join(PROJECT_ROOT, "data"),

    os.path.join(PROJECT_ROOT, "datasets"),

    os.path.join(PROJECT_ROOT, "uploads"),

    os.path.join(PROJECT_ROOT, "app", "data"),

]


dataset_files = []

for directory in possible_dataset_directories:

    if os.path.exists(directory):

        for filename in os.listdir(directory):

            if filename.lower().endswith(
                (".csv", ".xlsx", ".xls")
            ):

                dataset_files.append(
                    os.path.join(
                        directory,
                        filename
                    )
                )


if dataset_files:

    dataset_path = st.selectbox(
        "Dataset",
        dataset_files,
        format_func=lambda x: os.path.basename(x)
    )

    try:

        if dataset_path.lower().endswith(".csv"):

            dataset = pd.read_csv(
                dataset_path
            )

        else:

            dataset = pd.read_excel(
                dataset_path
            )

    except Exception:

        dataset = None


# ============================================================
# DATASET SUMMARY
# ============================================================

if dataset is not None:

    numeric_features = len(
        dataset.select_dtypes(
            include=np.number
        ).columns
    )

    categorical_features = len(
        dataset.select_dtypes(
            exclude=np.number
        ).columns
    )

    rows = len(dataset)


    render_html(
        f"""
        <div class="explain-card">

            <div class="model-info-title">
                📊 Dataset Information
            </div>

            <div class="metric-grid">

                <div class="metric-card">

                    <div class="metric-label">
                        Dataset Rows
                    </div>

                    <div class="metric-value">
                        {rows:,}
                    </div>

                </div>


                <div class="metric-card">

                    <div class="metric-label">
                        Numeric Features
                    </div>

                    <div class="metric-value">
                        {numeric_features}
                    </div>

                </div>


                <div class="metric-card">

                    <div class="metric-label">
                        Categorical Features
                    </div>

                    <div class="metric-value">
                        {categorical_features}
                    </div>

                </div>

            </div>

        </div>
        """
    )


# ============================================================
# SHAP EXPLANATION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🧠 Feature Explanation
    </div>

    <div class="section-description">
        Generate SHAP explanations for the selected model.
    </div>
    """,
    unsafe_allow_html=True
)


if model is None:

    st.error(
        "The selected model could not be loaded."
    )

    st.info(
        "Please select another trained model."
    )

    st.stop()


if dataset is None:

    st.info(
        "Upload or select a compatible dataset to generate explanations."
    )

    st.stop()


# ============================================================
# PREPARE DATA
# ============================================================

X = dataset.copy()


# Remove obvious target columns when possible

if target_column != "Unknown":

    if target_column in X.columns:

        X = X.drop(
            columns=[target_column]
        )


# ============================================================
# SHAP BUTTON
# ============================================================

if st.button(
    "🔍 Generate SHAP Explanation",
    type="primary"
):

    try:

        import shap

        # ----------------------------------------------------
        # Try model pipeline first
        # ----------------------------------------------------

        prediction_model = model

        transformed_X = X

        feature_names = list(
            X.columns
        )


        # ----------------------------------------------------
        # If model is a Pipeline
        # ----------------------------------------------------

        if hasattr(model, "named_steps"):

            try:

                preprocessing_steps = model.steps[:-1]

                final_model = model.steps[-1][1]

                transformed_X = X

                for _, step in preprocessing_steps:

                    transformed_X = step.transform(
                        transformed_X
                    )

                prediction_model = final_model

                if hasattr(
                    transformed_X,
                    "toarray"
                ):

                    transformed_X = transformed_X.toarray()

                transformed_X = np.asarray(
                    transformed_X
                )

            except Exception:

                transformed_X = X


        # ----------------------------------------------------
        # If categorical data remains
        # ----------------------------------------------------

        if isinstance(
            transformed_X,
            pd.DataFrame
        ):

            non_numeric = transformed_X.select_dtypes(
                exclude=np.number
            ).columns

            if len(non_numeric) > 0:

                st.warning(
                    "This model expects encoded numerical features. "
                    "The saved model does not contain compatible preprocessing "
                    "for the selected dataset."
                )

                st.info(
                    "Please select the dataset that was used when training this model."
                )

                st.stop()


        # ----------------------------------------------------
        # Convert to numpy
        # ----------------------------------------------------

        transformed_X = np.asarray(
            transformed_X
        )


        # ----------------------------------------------------
        # Limit rows for performance
        # ----------------------------------------------------

        if len(transformed_X) > 500:

            transformed_X = transformed_X[:500]

            st.info(
                "Using the first 500 rows for SHAP analysis "
                "to keep the dashboard responsive."
            )


        # ----------------------------------------------------
        # Tree models
        # ----------------------------------------------------

        tree_model_names = [

            "DecisionTreeRegressor",

            "DecisionTreeClassifier",

            "RandomForestRegressor",

            "RandomForestClassifier",

            "ExtraTreesRegressor",

            "ExtraTreesClassifier",

            "GradientBoostingRegressor",

            "GradientBoostingClassifier",

            "XGBRegressor",

            "XGBClassifier"

        ]


        if type(prediction_model).__name__ in tree_model_names:

            explainer = shap.TreeExplainer(
                prediction_model
            )

            shap_values = explainer.shap_values(
                transformed_X,
                check_additivity=False
            )


            # ------------------------------------------------
            # Classification output handling
            # ------------------------------------------------

            if isinstance(
                shap_values,
                list
            ):

                shap_array = np.asarray(
                    shap_values[-1]
                )

            else:

                shap_array = np.asarray(
                    shap_values
                )


            # ------------------------------------------------
            # SHAP summary
            # ------------------------------------------------

            st.success(
                "SHAP explanation generated successfully."
            )


            st.subheader(
                "📊 Feature Importance"
            )


            # If dimensions match
            if (
                shap_array.ndim == 2
                and shap_array.shape[1]
                == transformed_X.shape[1]
            ):

                importance = np.abs(
                    shap_array
                ).mean(
                    axis=0
                )

                names = feature_names

                if len(names) != len(importance):

                    names = [
                        f"Feature {i+1}"
                        for i in range(
                            len(importance)
                        )
                    ]

                importance_df = pd.DataFrame(
                    {
                        "Feature": names,
                        "Mean |SHAP|": importance
                    }
                ).sort_values(
                    "Mean |SHAP|",
                    ascending=False
                )


                st.dataframe(
                    importance_df,
                    use_container_width=True,
                    hide_index=True
                )


                st.bar_chart(
                    importance_df.set_index(
                        "Feature"
                    ).head(15)
                )


            else:

                st.info(
                    "The model was explained successfully, "
                    "but feature names could not be matched automatically."
                )


        else:

            st.warning(
                f"SHAP TreeExplainer is not supported for "
                f"{type(prediction_model).__name__}."
            )

            st.info(
                "For this model type, use a tree-based model such as "
                "Random Forest or Decision Tree for SHAP analysis."
            )


    except ValueError as e:

        # Friendly handling of the exact error
        error_text = str(e)

        if "could not convert string to float" in error_text:

            st.error(
                "The selected dataset contains text/categorical values "
                "that this trained model cannot process directly."
            )

            st.info(
                "Please select the dataset used during model training, "
                "or retrain the model with preprocessing such as "
                "OneHotEncoder."
            )

        else:

            st.error(
                "The SHAP explanation could not be generated."
            )

            st.info(
                "Please check that the selected model and dataset are compatible."
            )


    except Exception:

        # NEVER show complete traceback to normal users
        st.error(
            "We couldn't generate the explanation for this model."
        )

        st.info(
            "Try another trained model or use the dataset that was used "
            "to train this model."
        )