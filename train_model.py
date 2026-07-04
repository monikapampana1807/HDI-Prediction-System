import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Load cleaned dataset
df = pd.read_csv("dataset/clean_hdi.csv")


# Features
X = df[
    [
        'Life_Expectancy',
        'Expected_Schooling',
        'Mean_Schooling',
        'GNI_Per_Capita'
    ]
]


# Target
y = df['HDI_Category']


# Encode labels
encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42
)


# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Test
prediction = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    prediction
)


print("Model trained successfully!")
print("Accuracy:", accuracy)


# Save model
joblib.dump(
    model,
    "model/hdi_model.pkl"
)


# Save encoder
joblib.dump(
    encoder,
    "model/label_encoder.pkl"
)


print("\nModel saved inside model folder")