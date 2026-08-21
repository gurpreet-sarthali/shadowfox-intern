import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ------------------------
# 1. Load and inspect data
# ------------------------
path = r'c:\Users\Lenovo\Desktop\my all\code\shadowfox\basic_level\HousingData.csv'
df = pd.read_csv(path)

print('Dataset shape:', df.shape)
print('\nColumn names:')
print(df.columns.tolist())
print('\nData types:')
print(df.dtypes)
print('\nMissing values:')
print(df.isna().sum())
print('\nDuplicate rows:', df.duplicated().sum())
print('\nFirst 5 rows:')
print(df.head())

# Target is MEDV; all other columns are feature candidates.
X = df.drop(columns=['MEDV'])
y = df['MEDV']

# ------------------------
# 2. Basic quality checks
# ------------------------
print('\nSummary statistics:')
print(df.describe().T)

# Fill missing values using median for numerical columns.
median_imputer = SimpleImputer(strategy='median')
X_imputed = pd.DataFrame(median_imputer.fit_transform(X), columns=X.columns)

# ------------------------
# 3. EDA and visuals
# ------------------------
plt.figure(figsize=(10, 5))
sns.histplot(y, bins=20, kde=True)
plt.title('Distribution of House Prices (MEDV)')
plt.xlabel('Median Value of Owner-Occupied Homes ($1000s)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

corr = df.corr(numeric_only=True)
plt.figure(figsize=(14, 10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()

# Scatterplot of strongest known relationships
for col in ['RM', 'LSTAT', 'PTRATIO', 'DIS']:
    plt.figure(figsize=(6, 4))
    sns.scatterplot(x=df[col], y=df['MEDV'])
    plt.title(f'{col} vs MEDV')
    plt.xlabel(col)
    plt.ylabel('MEDV')
    plt.tight_layout()
    plt.show()

# ------------------------
# 4. Train-test split
# ------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42
)

# ------------------------
# 5. Model training + comparison
# ------------------------
models = {
    'Linear Regression': Pipeline([
        ('scaler', StandardScaler()),
        ('model', LinearRegression())
    ]),
    'Decision Tree Regressor': DecisionTreeRegressor(random_state=42),
    'Random Forest Regressor': RandomForestRegressor(random_state=42, n_estimators=300),
    'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=42),
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, preds)

    results.append({
        'Model': name,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
    })

results_df = pd.DataFrame(results).sort_values('R2', ascending=False)
print('\nModel comparison:')
print(results_df.to_string(index=False))

best_model_name = results_df.iloc[0]['Model']
best_model = models[best_model_name]

# ------------------------
# 6. Best model -> actual vs predicted plot
# ------------------------
final_preds = best_model.predict(X_test)

plt.figure(figsize=(7, 7))
sns.scatterplot(x=y_test, y=final_preds)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.title(f'Actual vs Predicted Prices — {best_model_name}')
plt.xlabel('Actual MEDV')
plt.ylabel('Predicted MEDV')
plt.tight_layout()
plt.show()

residuals = y_test - final_preds
plt.figure(figsize=(7, 5))
sns.histplot(residuals, bins=20, kde=True)
plt.title(f'Residual Distribution — {best_model_name}')
plt.xlabel('Residual (Actual - Predicted)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# ------------------------
# 7. Feature importance (if supported)
# ------------------------
if hasattr(best_model, 'feature_importances_'):
    importances = pd.Series(best_model.feature_importances_, index=X.columns)
    top_importances = importances.sort_values(ascending=False).head(10)
    print('\nTop feature importances:')
    print(top_importances)
    plt.figure(figsize=(8, 6))
    top_importances.plot(kind='barh', color='steelblue')
    plt.title('Top 10 Features by Importance')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.show()

# ------------------------
# 8. Final prediction example
# ------------------------
# Example of a new house following the same feature schema as the training data.
new_house = pd.DataFrame([
    {
        'CRIM': 0.2,
        'ZN': 25,
        'INDUS': 7.0,
        'CHAS': 0,
        'NOX': 0.55,
        'RM': 6.2,
        'AGE': 60,
        'DIS': 4.5,
        'RAD': 3,
        'TAX': 220,
        'PTRATIO': 18.0,
        'B': 390,
        'LSTAT': 8.5,
    }
])

new_house_imputed = pd.DataFrame(median_imputer.transform(new_house), columns=new_house.columns)
new_prediction = best_model.predict(new_house_imputed)
print('\nExample prediction for a new house:')
print(new_house)
print(f'Predicted MEDV: {new_prediction[0]:.2f} (in $1000s)')

# ------------------------
# 9. Final conclusion text
# ------------------------
print('\nConclusion:')
print('This workflow loaded the actual HousingData.csv file, checked shape, dtypes, nulls, duplicates, and identified MEDV as the target variable.')
print('We trained multiple regression models and compared their performance using MAE, MSE, RMSE, and R^2. The best-performing model was selected based on the highest R^2 and lowest error metrics.')
print('The strongest price drivers were typically property size (RM), socioeconomic and neighborhood indicators (LSTAT), and accessibility features (DIS), though the exact ranking depends on the selected model.')
