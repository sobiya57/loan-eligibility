import pandas as pd
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    StratifiedKFold,
    GridSearchCV,
)
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    roc_curve,
)
from sklearn.ensemble import RandomForestClassifier
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import shap
from utils import (
    TRAIN_PATH,
    MODEL_PATH,
    EDA_REPORT_PATH,
    MODEL_REPORT_PATH,
    METRICS_REPORT_PATH,
    FEATURE_IMPORTANCE_PATH,
    FEATURE_IMPORTANCE_IMAGE_PATH,
    CONFUSION_MATRIX_PATH,
    ROC_CURVE_PATH,
    CROSS_VALIDATION_REPORT_PATH,
    SHAP_SUMMARY_PATH,
    SHAP_BAR_PATH,
)

from eda import generate_eda_report

# 1) Load data
df = pd.read_csv(TRAIN_PATH)
df.columns = [c.strip() for c in df.columns]

# Generate EDA report
generate_eda_report(df, EDA_REPORT_PATH)
print(f"EDA report saved to {EDA_REPORT_PATH}")

TARGET = "Loan_Status"

# Map target Y/N -> 1/0 if needed
if df[TARGET].dtype == object:
    df[TARGET] = df[TARGET].astype(str).str.strip().map({"Y": 1, "N": 0})

categorical = ["Gender","Married","Dependents","Education","Self_Employed","Property_Area"]
numeric = ["ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History"]

X = df[categorical + numeric]
y = df[TARGET].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2) Preprocess
cat_tf = Pipeline(steps=[
    ("imp", SimpleImputer(strategy="most_frequent")),
    ("ohe", OneHotEncoder(handle_unknown="ignore"))
])
num_tf = Pipeline(steps=[
    ("imp", SimpleImputer(strategy="median")),
])

preprocess = ColumnTransformer(
    transformers=[
        ("cat", cat_tf, categorical),
        ("num", num_tf, numeric),
    ],
    remainder="drop",
)

# 3) Model
clf = RandomForestClassifier(
    random_state=42,
    n_jobs=-1,
)

pipe = Pipeline(
    steps=[
        ("prep", preprocess),
        ("model", clf),
    ]
)

# Grid Search Parameters
param_grid = {
    "model__n_estimators": [100, 200, 300],
    "model__max_depth": [None, 5, 10, 20],
    "model__min_samples_split": [2, 5],
    "model__min_samples_leaf": [1, 2],
}

grid = GridSearchCV(
    estimator=pipe,
    param_grid=param_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=1,
)

pipe = grid

# 4) Train
pipe.fit(X_train, y_train)

print("\nBest Parameters:")
print(pipe.best_params_)

print("\nBest Cross Validation Accuracy:")
print(pipe.best_score_)

# 5) Evaluate
best_model = pipe.best_estimator_

y_pred = best_model.predict(X_test)
y_prob = best_model.predict_proba(X_test)[:, 1]
print(classification_report(y_test, y_pred))
try:
    print("ROC AUC:", roc_auc_score(y_test, y_prob))
except Exception:
    pass

# Generate Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap="Blues")

plt.title("Loan Eligibility - Confusion Matrix")
plt.tight_layout()

plt.savefig(CONFUSION_MATRIX_PATH)
plt.close()

print(f"Confusion Matrix saved to {CONFUSION_MATRIX_PATH}")

# Generate ROC Curve

fpr, tpr, _ = roc_curve(y_test, y_prob)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f"AUC = {roc_auc_score(y_test, y_prob):.3f}")
plt.plot([0, 1], [0, 1], linestyle="--")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Loan Eligibility - ROC Curve")
plt.legend()

plt.tight_layout()
plt.savefig(ROC_CURVE_PATH)
plt.close()

print(f"ROC Curve saved to {ROC_CURVE_PATH}")

# Generate Feature Importance Report

feature_names = best_model.named_steps["prep"].get_feature_names_out()
importances = best_model.named_steps["model"].feature_importances_

importance_df = (
    pd.DataFrame(
        {
            "Feature": feature_names,
            "Importance": importances,
        }
    )
    .sort_values("Importance", ascending=False)
)

importance_df.to_csv(FEATURE_IMPORTANCE_PATH, index=False)

print(f"Feature importance saved to {FEATURE_IMPORTANCE_PATH}")

# Generate Feature Importance Chart

top_features = importance_df.head(15)

plt.figure(figsize=(10, 6))

plt.barh(
    top_features["Feature"][::-1],
    top_features["Importance"][::-1]
)

plt.xlabel("Importance")
plt.ylabel("Features")
plt.title("Top 15 Feature Importances")

plt.tight_layout()

plt.savefig(FEATURE_IMPORTANCE_IMAGE_PATH)

plt.close()

print(
    f"Feature Importance Chart saved to {FEATURE_IMPORTANCE_IMAGE_PATH}"
)

# Cross Validation

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)

cv_scores = cross_val_score(
    pipe,
    X,
    y,
    cv=cv,
    scoring="accuracy",
)

print("\nCross Validation Scores:")
print(cv_scores)

print(f"Mean Accuracy: {cv_scores.mean():.4f}")
print(f"Std Accuracy : {cv_scores.std():.4f}")

with open(CROSS_VALIDATION_REPORT_PATH, "w") as f:
    f.write("5-Fold Cross Validation\n")
    f.write("=" * 40 + "\n\n")

    for i, score in enumerate(cv_scores, start=1):
        f.write(f"Fold {i}: {score:.4f}\n")

    f.write("\n")
    f.write(f"Mean Accuracy : {cv_scores.mean():.4f}\n")
    f.write(f"Std Accuracy  : {cv_scores.std():.4f}\n")

print(f"Cross Validation report saved to {CROSS_VALIDATION_REPORT_PATH}")

# ==========================
# SHAP Explainability
# ==========================

# Get transformed test data
X_test_transformed = best_model.named_steps["prep"].transform(X_test)

# Get feature names after preprocessing
feature_names = best_model.named_steps["prep"].get_feature_names_out()

# Get trained Random Forest model
rf_model = best_model.named_steps["model"]

# Create SHAP explainer
explainer = shap.TreeExplainer(rf_model)

# Calculate SHAP values
shap_values = explainer.shap_values(X_test_transformed)

# Handle SHAP output for binary classification
if isinstance(shap_values, list):
    shap_values = shap_values[1]
elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
    shap_values = shap_values[:, :, 1]
    
# SHAP Summary Plot
plt.figure(figsize=(14, 8))

shap.summary_plot(
    shap_values,
    X_test_transformed,
    feature_names=feature_names,
    show=False,
    max_display=15
)

plt.title("SHAP Summary Plot", fontsize=16, pad=15)
plt.xlabel("SHAP interaction value", fontsize=12)
plt.tight_layout()

plt.savefig(
    SHAP_SUMMARY_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"SHAP Summary Plot saved to {SHAP_SUMMARY_PATH}")


# SHAP Feature Importance
plt.figure(figsize=(14, 8))

shap.summary_plot(
    shap_values,
    X_test_transformed,
    feature_names=feature_names,
    plot_type="bar",
    show=False,
    max_display=15
)

plt.title("SHAP Feature Importance", fontsize=16, pad=15)
plt.xlabel("Mean |SHAP value|", fontsize=12)
plt.tight_layout()

plt.savefig(
    SHAP_BAR_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"SHAP Bar Plot saved to {SHAP_BAR_PATH}")

# 6) Save
joblib.dump(best_model, MODEL_PATH)
print(f"Saved trained pipeline to {MODEL_PATH}")
