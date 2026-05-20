"""
IIT-Standard House Price Prediction Model Trainer
-------------------------------------------------
This script:
1. Loads and cleans raw housing data.
2. Builds a preprocessing + ML pipeline.
3. Trains a RandomForestRegressor model.
4. Evaluates performance using RMSE, MAE, and R².
5. Saves the trained model to artifacts/ for Django integration.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import numpy as np
import os

# ------------------------------------------------------------
# 1️⃣ LOAD DATA
# ------------------------------------------------------------
data_path = "predictor/ml/house_data.csv"
data = pd.read_csv("C:\\Users\\saiteja\\OneDrive\\Documents\\all excel files\\house.csv")

print("✅ Data loaded successfully!")
print("Columns:", data.columns.tolist())
print("Rows:", len(data))

# ------------------------------------------------------------
# 2️⃣ CLEAN AND PREPROCESS DATA
# ------------------------------------------------------------

# Drop rows with missing values
data = data.dropna()

# Convert 'total_sqft' values like '1200-1500' → mean(1200,1500)
def handle_sqft(x):
    try:
        if '-' in str(x):
            vals = x.split('-')
            return (float(vals[0]) + float(vals[1])) / 2
        return float(x)
    except:
        return None

data['total_sqft'] = data['total_sqft'].apply(handle_sqft)
data = data.dropna(subset=['total_sqft'])

# Define feature and target columns
X = data.drop("price", axis=1)
y = data["price"]

# Define categorical and numerical columns
categorical = ['area_type', 'availability', 'location', 'size']
numerical = ['total_sqft', 'bath']

# ------------------------------------------------------------
# 3️⃣ BUILD PIPELINE
# ------------------------------------------------------------

# Preprocessor handles both types of features
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical),
    ('cat', OneHotEncoder(handle_unknown="ignore"), categorical)
])

# Complete pipeline = preprocessing + model
model = Pipeline([
    ('pre', preprocessor),
    ('rf', RandomForestRegressor(n_estimators=100, random_state=42))
])

# ------------------------------------------------------------
# 4️⃣ TRAIN / TEST SPLIT
# ------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------------------------------------------
# 5️⃣ MODEL TRAINING
# ------------------------------------------------------------
print("🚀 Training model...")
model.fit(X_train, y_train)
print("✅ Model training complete!")

# ------------------------------------------------------------
# 6️⃣ MODEL EVALUATION
# ------------------------------------------------------------
y_pred = model.predict(X_test)

# RMSE = Root Mean Squared Error
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# MAE = Mean Absolute Error
mae = mean_absolute_error(y_test, y_pred)

# R² = Coefficient of Determination
r2 = r2_score(y_test, y_pred)

print("\n📊 Model Evaluation Results:")
print("--------------------------------------")
print("Model prediction",y_pred)
print(f"RMSE (Root Mean Squared Error): {rmse:.2f}")
print(f"MAE  (Mean Absolute Error):     {mae:.2f}")
print(f"R² Score (Goodness of fit):     {r2:.3f}")
print("--------------------------------------")

# ------------------------------------------------------------
# 7️⃣ SAVE TRAINED MODEL
# ------------------------------------------------------------
os.makedirs("predictor/ml/artifacts", exist_ok=True)
joblib.dump(model, "predictor/ml/artifacts/house_price_model.joblib")
print("✅ Model saved successfully at: predictor/ml/artifacts/house_price_model.joblib")
