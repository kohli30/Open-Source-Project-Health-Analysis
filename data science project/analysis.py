import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("github_cleaned_dataset.csv")

# Convert target variable to numeric
le = LabelEncoder()
df["Activity_Status"] = le.fit_transform(df["Activity_Status"])  # Active=1, Declining=0

# Select features
features = [
    "Monthly_Commit_Velocity",
    "Total_Contributors",
    "Active_Contributors_Last_30_Days",
    "Issue_Resolution_Rate",
    "PR_Merge_Rate",
    "Contributor_Churn_Rate"
]

X = df[features]
y = df["Activity_Status"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, y_pred)

plt.figure()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Declining", "Active"],
            yticklabels=["Declining", "Active"])

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()



feature_importance = pd.DataFrame({
    "Feature": features,
    "Coefficient": model.coef_[0]
})

feature_importance = feature_importance.sort_values(by="Coefficient", ascending=False)

plt.figure()
sns.barplot(x="Coefficient", y="Feature", data=feature_importance)
plt.title("Feature Importance (Logistic Regression)")
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df_clean = pd.read_csv("github_cleaned_dataset.csv")

print("Dataset Shape:", df_clean.shape)
print(df_clean.head())

plt.figure()
sns.histplot(df_clean["Monthly_Commit_Velocity"])
plt.title("Distribution of Monthly Commit Velocity")
plt.xlabel("Monthly Commit Velocity")
plt.ylabel("Frequency")
plt.show()

plt.figure()
sns.boxplot(x="Activity_Status", y="Contributor_Churn_Rate", data=df_clean)
plt.title("Contributor Churn Rate by Activity Status")
plt.show()

plt.figure(figsize=(10,8))
sns.heatmap(df_clean.corr(numeric_only=True), cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
