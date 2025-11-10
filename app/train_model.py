import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
import joblib
from utils import TRAIN_PATH, MODEL_PATH

# 1) Load data
df = pd.read_csv(TRAIN_PATH)
df.columns = [c.strip() for c in df.columns]

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
clf = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)

pipe = Pipeline(steps=[("prep", preprocess), ("model", clf)])

# 4) Train
pipe.fit(X_train, y_train)

# 5) Evaluate
y_pred = pipe.predict(X_test)
y_prob = pipe.predict_proba(X_test)[:, 1]
print(classification_report(y_test, y_pred))
try:
    print("ROC AUC:", roc_auc_score(y_test, y_prob))
except Exception:
    pass

# 6) Save
joblib.dump(pipe, MODEL_PATH)
print(f"Saved trained pipeline to {MODEL_PATH}")
