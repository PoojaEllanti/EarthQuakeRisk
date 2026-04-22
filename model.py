import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

def train_model():

    # ---------------- LOAD DATA ----------------
    data = pd.read_csv("earthquake.csv")
    data.columns = data.columns.str.lower()

    # Rename columns if needed
    column_map = {
        "magnitude": "mag",
        "lat": "latitude",
        "lon": "longitude"
    }
    data = data.rename(columns=column_map)

    # Keep required columns
    data = data[['mag', 'depth', 'latitude', 'longitude']].dropna()

    # ---------------- BALANCED LABEL ----------------
    def risk_level(row):
        if row['mag'] >= 6:
            return 2   # High
        elif row['mag'] >= 4:
            return 1   # Medium
        else:
            return 0   # Low

    data['risk'] = data.apply(risk_level, axis=1)

    X = data[['mag', 'depth', 'latitude', 'longitude']]
    y = data['risk']

    # ---------------- SPLIT ----------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ---------------- MODELS ----------------
    models = {
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(),
        "Logistic Regression": LogisticRegression(max_iter=1000)
    }

    best_model = None
    best_acc = 0
    best_name = ""
    results = {}

    # ---------------- TRAIN ----------------
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        results[name] = acc

        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name

    return best_model, best_acc, best_name, results