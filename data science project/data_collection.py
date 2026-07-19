import requests
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns


TOKEN = "[Enter YOUR API]"

headers = {
    "Authorization": f"token {TOKEN}"
}

repos_data = []
page = 1

while len(repos_data) < 200:
    url = f"https://api.github.com/search/repositories?q=stars:>500&sort=stars&page={page}&per_page=50"
    response = requests.get(url, headers=headers).json()

    for repo in response["items"]:
        repos_data.append({
            "Repository_Name": repo["full_name"],
            "Primary_Language": repo["language"],
            "Stars_Count": repo["stargazers_count"],
            "Forks_Count": repo["forks_count"],
            "Open_Issues": repo["open_issues_count"],
            "Repository_Age_Months": (
                (pd.Timestamp.utcnow() - pd.to_datetime(repo["created_at"])).days // 30

            ),
            "Days_Since_Last_Update": (
               (pd.Timestamp.utcnow() - pd.to_datetime(repo["pushed_at"])).days

            )
        })

    page += 1
    time.sleep(2)

df = pd.DataFrame(repos_data)
df.to_csv("real_github_repositories.csv", index=False)

print("Collected Repositories:", df.shape)

import numpy as np

expanded_data = []

for _, row in df.iterrows():
    for month in range(6):  # 6 months per repository
        expanded_data.append({
            "Repository_Name": row["Repository_Name"],
            "Primary_Language": row["Primary_Language"],
            "Stars_Count": row["Stars_Count"],
            "Forks_Count": row["Forks_Count"],
            "Open_Issues": row["Open_Issues"],
            "Repository_Age_Months": row["Repository_Age_Months"],
            "Days_Since_Last_Update": row["Days_Since_Last_Update"],
            "Activity_Month": month + 1,
            "Monthly_Commit_Velocity": np.random.randint(5, 200),
            "Total_Contributors": np.random.randint(5, 300),
            "Active_Contributors_Last_30_Days": np.random.randint(1, 100),
            "Total_Issues": np.random.randint(50, 5000),
            "Issue_Resolution_Rate": np.random.uniform(0.4, 0.95),
            "Total_Pull_Requests": np.random.randint(50, 4000),
            "PR_Merge_Rate": np.random.uniform(0.5, 0.98),
            "Release_Frequency": np.random.randint(0, 12),
            "Contributor_Churn_Rate": np.random.uniform(0.05, 0.5),
            "Activity_Status": np.random.choice(["Active", "Declining"])
        })

df_expanded = pd.DataFrame(expanded_data)

df_expanded.to_csv("github_expanded_dataset.csv", index=False)

print("Expanded Dataset Shape:", df_expanded.shape)

df_clean = df_expanded[
    (df_expanded["Total_Contributors"] >= 10) &
    (df_expanded["Monthly_Commit_Velocity"] >= 10)
]

df_clean.to_csv("github_cleaned_dataset.csv", index=False)

print("Cleaned Dataset Shape:", df_clean.shape)

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
