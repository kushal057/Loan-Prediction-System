import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ensure 'charts' directory exists
charts_dir = 'charts'
os.makedirs(charts_dir, exist_ok=True)

# Load dataset
data_path = "data/train.csv"
df = pd.read_csv(data_path)

# Basic overview
print(df.info())  # Check data types and missing values
print(df.describe())  # Summary statistics for numerical columns
print(df.head())  # First few rows

# Missing values heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.savefig(os.path.join(charts_dir, 'missing_values_heatmap.png'))
plt.show()
plt.close()

# Example handling: Fill missing values with median (for simplicity)
df.fillna(df.median(numeric_only=True), inplace=True)

# Loan Status Distribution
plt.figure(figsize=(8, 6))
sns.countplot(x='Loan_Status', data=df, color='skyblue')  # Use `color` instead of `palette`
plt.title('Loan Status Distribution')
plt.savefig(os.path.join(charts_dir, 'loan_status_distribution.png'))
plt.show()
plt.close()

# Bar plots for categorical features vs Loan Status
categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']

for col in categorical_cols:
    plt.figure(figsize=(8, 6))
    sns.countplot(x=col, hue='Loan_Status', data=df)
    plt.title(f'{col} vs Loan Status')
    plt.savefig(os.path.join(charts_dir, f'{col}_vs_Loan_Status.png'))
    plt.show()
    plt.close()

# Histograms for numerical features
numerical_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']

for col in numerical_cols:
    plt.figure(figsize=(8, 6))
    sns.histplot(df[col], kde=True, bins=30, color='blue')
    plt.title(f'{col} Distribution')
    plt.savefig(os.path.join(charts_dir, f'{col}_distribution.png'))
    plt.show()
    plt.close()

# Boxplots for Loan Status vs Numerical Features
for col in numerical_cols:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Loan_Status', y=col, data=df)
    plt.title(f'{col} vs Loan Status')
    plt.savefig(os.path.join(charts_dir, f'{col}_vs_Loan_Status.png'))
    plt.show()
    plt.close()

# Correlation Heatmap
# Drop non-numeric columns
numeric_df = df.select_dtypes(include=['number'])

plt.figure(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap')
plt.savefig(os.path.join(charts_dir, 'correlation_heatmap.png'))
plt.show()
plt.close()
