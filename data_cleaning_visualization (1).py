"""
Project 1: Data Cleaning & Visualization Project
--------------------------------------------------
Goal   : Work on a raw dataset to clean, process, and visualize insights.
Tools  : Pandas, Matplotlib, Seaborn
Output : A cleaned CSV file + a dashboard image (PNG) with key visual insights.

NOTE: A synthetic "raw" employee sales dataset is generated below so the
script runs anywhere without needing an external file. To use your own
data, simply replace the `generate_raw_dataset()` call with
`pd.read_csv("your_file.csv")`.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_raw_dataset(n=300):
    regions = ["North", "South", "East", "West"]
    df = pd.DataFrame({
        "EmployeeID": range(1, n + 1),
        "Region": np.random.choice(regions, n),
        "Age": np.random.randint(21, 60, n).astype(float),
        "ExperienceYears": np.random.randint(0, 35, n).astype(float),
        "MonthlySales": np.random.normal(50000, 15000, n).round(2),
        "CustomerRating": np.random.uniform(1, 5, n).round(2),
    })

    missing_idx = np.random.choice(df.index, size=int(0.08 * n), replace=False)
    df.loc[missing_idx, "Age"] = np.nan
    missing_idx2 = np.random.choice(df.index, size=int(0.06 * n), replace=False)
    df.loc[missing_idx2, "MonthlySales"] = np.nan

    outlier_idx = np.random.choice(df.index, size=6, replace=False)
    df.loc[outlier_idx, "MonthlySales"] = df.loc[outlier_idx, "MonthlySales"] * 5

    df = pd.concat([df, df.iloc[:10]], ignore_index=True)
    return df


def inspect_data(df, label):
    print(f"\n--- {label} ---")
    print("Shape:", df.shape)
    print("Missing values per column:\n", df.isnull().sum())
    print("Duplicate rows:", df.duplicated().sum())


def clean_data(df):
    df = df.drop_duplicates().reset_index(drop=True)

    for col in ["Age", "MonthlySales"]:
        df[col] = df[col].fillna(df[col].median())

    def cap_outliers(series):
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        return series.clip(lower, upper)

    df["MonthlySales"] = cap_outliers(df["MonthlySales"])
    df["Age"] = df["Age"].round(0).astype(int)
    return df


def build_dashboard(raw_df, clean_df):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle("Data Cleaning & Visualization Dashboard", fontsize=16, fontweight="bold")

    sns.heatmap(raw_df.isnull(), cbar=False, cmap="Reds", ax=axes[0, 0])
    axes[0, 0].set_title("Missing Values (Raw Data)")

    sns.boxplot(data=raw_df, y="MonthlySales", ax=axes[0, 1], color="salmon")
    sns.boxplot(data=clean_df, y="MonthlySales", ax=axes[0, 1], color="lightgreen",
                width=0.4, fliersize=2)
    axes[0, 1].set_title("MonthlySales: Raw (red) vs Cleaned (green)")

    sns.histplot(clean_df["MonthlySales"], kde=True, color="steelblue", ax=axes[1, 0])
    axes[1, 0].set_title("MonthlySales Distribution (Cleaned)")

    corr = clean_df[["Age", "ExperienceYears", "MonthlySales", "CustomerRating"]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=axes[1, 1])
    axes[1, 1].set_title("Correlation Heatmap (Cleaned)")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path = os.path.join(OUTPUT_DIR, "data_cleaning_dashboard.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"\nDashboard saved to: {path}")


def main():
    raw_df = generate_raw_dataset()
    inspect_data(raw_df, "Raw Dataset")

    clean_df = clean_data(raw_df)
    inspect_data(clean_df, "Cleaned Dataset")

    csv_path = os.path.join(OUTPUT_DIR, "cleaned_dataset.csv")
    clean_df.to_csv(csv_path, index=False)
    print(f"\nCleaned dataset saved to: {csv_path}")

    build_dashboard(raw_df, clean_df)

    print("\nKey Insights:")
    print(f"- Average monthly sales after cleaning: {clean_df['MonthlySales'].mean():.2f}")
    print(f"- Region with most employees: {clean_df['Region'].mode()[0]}")
    print(f"- Correlation between experience and sales: "
          f"{clean_df['ExperienceYears'].corr(clean_df['MonthlySales']):.2f}")


if __name__ == "__main__":
    main()
