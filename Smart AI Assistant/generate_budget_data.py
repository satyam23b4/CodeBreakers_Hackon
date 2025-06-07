# generate_budget_data.py

import pandas as pd
import numpy as np

np.random.seed(0)
months = pd.date_range(start='2024-01-01', periods=12, freq='MS').strftime('%Y-%m')
data = {'month': months}
for cat, base in [('Electronics', 8000), ('Groceries', 5000), ('Fashion', 3000), ('Other', 2000)]:
    # Linear trend + seasonal + noise
    trend = np.linspace(base * 0.8, base * 1.2, len(months))
    seasonal = 300 * np.sin(np.linspace(0, 2 * np.pi, len(months)))
    noise = np.random.normal(0, 200, len(months))
    data[cat] = trend + seasonal + noise

df = pd.DataFrame(data)
df.to_csv('budget_data.csv', index=False)
print("budget_data.csv created:")
print(df.head())
