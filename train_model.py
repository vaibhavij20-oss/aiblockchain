import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight

# Load dataset
df = pd.read_csv("data/ctdc_dataset.csv", sep=";", low_memory=False)

# Create Risk label
df["Risk"] = (
    (df["isForcedLabour"] == 1) |
    (df["isSexualExploit"] == 1)
).astype(int)

# Selected features
features = [
    "gender",
    "ageBroad",
    "citizenship",
    "meansOfControlDebtBondage",
    "meansOfControlThreats",
    "meansOfControlPsychologicalAbuse",
    "meansOfControlPhysicalAbuse",
    "meansOfControlSexualAbuse",
    "meansOfControlWithholdsDocuments",
    "meansOfControlRestrictsMovement",
    "meansOfControlExcessiveWorkingHours",
    "recruiterRelationFriend",
    "recruiterRelationFamily",
    "recruiterRelationOther"
]

X = df[features].copy()
y = df["Risk"]

# Handle missing values
X["gender"] = X["gender"].fillna("Unknown")
X["ageBroad"] = X["ageBroad"].fillna("Unknown")
X["citizenship"] = X["citizenship"].fillna("Unknown")
X = X.fillna(0)

# One-hot encode
X = pd.get_dummies(X, drop_first=True)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Handle imbalance
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y_train),
    y=y_train
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight=dict(zip(np.unique(y_train), class_weights))
)

model.fit(X_train, y_train)

print("Model Performance:")
print(classification_report(y_test, model.predict(X_test)))

# Save model and feature columns
joblib.dump(model, "model.pkl")
joblib.dump(X.columns.tolist(), "feature_columns.pkl")

print("Model and features saved successfully!")
