# Data-Cleaning-and-Visualization-
Work on raw data to clean, process and visualize insights

Title
Customer Sales Data Cleaning and Visualization Using Python

Objective
The objective of this project was to clean a raw sales dataset, handle missing values and duplicate records, and create meaningful visualizations to understand business trends.

Tools Used
Python
Pandas
Matplotlib
Seaborn
Jupyter Notebook

Dataset Description
The dataset contained customer purchase information including:
Customer ID
Age
Gender
Product Category
Purchase Amount
Purchase Date
City

Steps Performed

1. Data Loading
Imported the dataset using Pandas and checked its structure.

import pandas as pd
df = pd.read_csv("sales_data.csv")
df.head()

2. Handling Missing Values
Filled missing ages with the average age.
Removed records with missing purchase amounts.

df['Age'].fillna(df['Age'].mean(), inplace=True)
df.dropna(subset=['Purchase_Amount'], inplace=True)

3. Removing Duplicates
   
   df.drop_duplicates(inplace=True)

5. Detecting Outliers
Used box plots and the IQR method to identify unusual purchase amounts.

6. Data Visualization
   
Sales by Product Category
sns.countplot(x='Product_Category', data=df)

Purchase Amount Distribution
sns.histplot(df['Purchase_Amount'])

Monthly Sales Trend
df.groupby('Purchase_Month')['Purchase_Amount'].sum().plot()

Findings
Electronics products generated the highest sales.
Most customers spent between ₹1,000 and ₹5,000.
Sales increased during festive months.

Conclusion
This project improved my understanding of data preprocessing techniques such as handling missing values, removing duplicates, and visualizing patterns using Python libraries. The visualizations helped in identifying important business insights from raw data.
