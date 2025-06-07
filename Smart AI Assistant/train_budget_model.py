# train_budget_model.py

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# 1. Load data
df = pd.read_csv('budget_data.csv')
# Convert month to numeric feature: 0,1,...,11
df['mnum'] = np.arange(len(df))

models = {}
for cat in ['Electronics','Groceries','Fashion','Other']:
    X = df[['mnum']]
    y = df[cat]
    lr = LinearRegression()
    lr.fit(X, y)
    models[cat] = lr
    print(f"{cat} model coef:. intercept:", lr.intercept_, "slope:", lr.coef_[0])

# 2. Save dictionary of models
joblib.dump(models, 'budget_models.pkl')
print("Saved budget_models.pkl")
