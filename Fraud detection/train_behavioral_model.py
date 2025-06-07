import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
import joblib

def main():
    # 1. Load the synthetic dataset
    df = pd.read_csv('behavioral_biometrics_dataset.csv')
    print(f"Loaded dataset with {len(df)} rows")

    # 2. Split into features and label
    X = df.drop(columns=['label'])
    y = df['label']

    # 3. Train/test split (80/20 stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples")

    # 4. Instantiate & train RandomForest
    clf = RandomForestClassifier(
        n_estimators=100,   # number of trees in the forest
        max_depth=10,       # maximum depth per tree
        random_state=42,    # for reproducible results
        n_jobs=-1           # use all CPU cores
    )
    clf.fit(X_train, y_train)
    print("Model training complete")

    # 5. Evaluate on the test set
    y_proba = clf.predict_proba(X_test)[:, 1]  # probability of class “1” (fraud)
    auc = roc_auc_score(y_test, y_proba)
    print(f"Test ROC AUC: {auc:.3f}")

    # Optional: classification report at default threshold 0.5
    y_pred = (y_proba >= 0.5).astype(int)
    print("Classification Report (threshold=0.5):")
    print(classification_report(y_test, y_pred))

    # 6. Save the trained model
    model_path = 'keystroke_fraud_model.pkl'
    joblib.dump(clf, model_path)
    print(f"Trained model saved to {model_path}")

if __name__ == '__main__':
    main()
