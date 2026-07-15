import pandas as pd
import pickle
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# FIXED FEATURE FUNCTION (IMPORTANT)
def extract_features(password):
    return [
        len(password),
        len(re.findall(r"\d", password)),
        len(re.findall(r"[A-Z]", password)),
        len(re.findall(r"[a-z]", password)),
        len(re.findall(r"[^a-zA-Z0-9]", password)),
    ]

# Load dataset
data = pd.read_csv("passwords.csv")

X = data["password"].apply(extract_features).tolist()
y = data["strength"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# Evaluation
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained & saved")