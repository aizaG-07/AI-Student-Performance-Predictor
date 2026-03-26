import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load datasets
df1 = pd.read_csv("StudentPerformanceFactors.csv")
df2 = pd.read_csv("student_performance.csv")

# Align rows
min_len = min(len(df1), len(df2))
df1 = df1.iloc[:min_len]
df2 = df2.iloc[:min_len]

# Combine datasets
df = pd.concat([df1, df2], axis=1)

# Remove duplicate columns
df = df.loc[:, ~df.columns.duplicated()]

# Handle missing values
df.fillna(df.mean(numeric_only=True), inplace=True)

# Create target column
df['pass'] = df['total_score'].apply(lambda x: 1 if x >= 50 else 0)

# Select features
features = [
    'Hours_Studied',
    'Attendance',
    'Sleep_Hours',
    'weekly_self_study_hours',
    'total_score'
]

X = df[features]
y = df['pass']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model trained using merged datasets!")