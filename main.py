import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# ==========================
# Setup and Imports
# ==========================
charts_dir = 'charts'
os.makedirs(charts_dir, exist_ok=True)

# Load dataset
data_path = "data/train.csv"
df = pd.read_csv(data_path)

# ==========================
# Feature Engineering
# ==========================
# Fill missing values for simplicity
df.fillna(df.median(numeric_only=True), inplace=True)
df['Self_Employed'] = df['Self_Employed'].fillna('Unknown')

# Convert 'Loan_Amount_Term' to years and create total income feature
df['Loan_Amount_Term'] = df['Loan_Amount_Term'] / 12
df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']

# Encoding categorical variables (One-Hot Encoding)
df = pd.get_dummies(df, drop_first=True)

# ==========================
# Data Preprocessing
# ==========================
# Remove identifier columns such as 'Loan_ID'
df = df.drop(columns=[col for col in df.columns if 'Loan_ID' in col])

# Separate features and target
X = df.drop('Loan_Status_Y', axis=1)
y = df['Loan_Status_Y']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ==========================
# Model Building (Logistic Regression)
# ==========================
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# ==========================
# Map One-Hot Encoded Feature Names Back to Original
# ==========================
def map_feature_names_to_original(coefficients, original_columns):
    """
    Map one-hot encoded feature names back to the original categorical feature names.
    """
    original_feature_names = []
    for feature in coefficients.index:
        # Identify if the feature name is one-hot encoded and map to the original column
        mapped = False
        for col in original_columns:
            if feature.startswith(col + '_'):
                original_feature_names.append(col)
                mapped = True
                break
        if not mapped:
            original_feature_names.append(feature)  # Keep feature name as is if no match
    coefficients['Original_Feature'] = original_feature_names
    return coefficients

# ==========================
# Generate Top 3 Features Impact Chart
# ==========================
def generate_top_features_chart():
    # Get model coefficients
    coefficients = pd.DataFrame(model.coef_.flatten(), X.columns, columns=['Coefficient'])
    coefficients = coefficients.sort_values(by='Coefficient', ascending=False)

    # List of original categorical columns before encoding
    original_columns = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Credit_History']

    # Map one-hot encoded features back to original
    coefficients = map_feature_names_to_original(coefficients, original_columns)

    # Get top 3 features impacting loan status
    top_features = coefficients.head(3)

    # Plot the bar chart for top 3 features
    plt.figure(figsize=(8, 6))
    sns.barplot(x=top_features['Original_Feature'], y=top_features['Coefficient'], palette='coolwarm')
    plt.title('Top 3 Features Impacting Loan Status')
    plt.xlabel('Feature')
    plt.ylabel('Coefficient Value')
    plt.savefig(os.path.join(charts_dir, 'top_3_features_impact.png'))
    plt.show()

# ==========================
# Generate Loan Amount vs Income Chart
# ==========================
def generate_income_vs_loan_amount_chart():
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Loan_Status_Y', y='Total_Income', data=df, palette='coolwarm')
    plt.title('Loan Approval by Total Income')
    plt.xlabel('Loan Approval Status')
    plt.ylabel('Total Income')
    plt.savefig(os.path.join(charts_dir, 'income_vs_loan_amount.png'))
    plt.show()

# ==========================
# Generate Married Status vs Loan Approval Status
# ==========================
def generate_married_status_vs_loan_status_chart():
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Married_Yes', hue='Loan_Status_Y', data=df, palette='coolwarm')
    plt.title('Loan Approval by Marital Status')
    plt.xlabel('Marital Status (Married = 1)')
    plt.ylabel('Loan Approval Count')
    plt.savefig(os.path.join(charts_dir, 'married_status_vs_loan_status.png'))
    plt.show()

# ==========================
# Generate Credit History vs Loan Approval Status Chart
# ==========================
def generate_credit_history_chart():
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Credit_History', y='Loan_Status_Y', data=df, palette='coolwarm')
    plt.title('Loan Approval by Credit History')
    plt.xlabel('Credit History')
    plt.ylabel('Loan Approval Rate')
    plt.savefig(os.path.join(charts_dir, 'credit_history_impact.png'))
    plt.show()

# ==========================
# Generate Employment Status vs Loan Approval Chart
# ==========================
def generate_employment_status_vs_loan_status_chart():
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Self_Employed_Unknown', hue='Loan_Status_Y', data=df, palette='coolwarm')
    plt.title('Loan Approval by Employment Status')
    plt.xlabel('Employment Status (Self-Employed = 1)')
    plt.ylabel('Loan Approval Count')
    plt.savefig(os.path.join(charts_dir, 'employment_status_vs_loan_status.png'))
    plt.show()

# ==========================
# User Input Prediction Function
# ==========================
def predict_loan_status(user_data, model, scaler, df):
    # Create a DataFrame from user input
    user_df = pd.DataFrame([user_data])

    # One-hot encode the user input data
    user_df = pd.get_dummies(user_df, drop_first=True)

    # Ensure the user data matches the feature columns of the training set
    missing_cols = set(df.columns) - set(user_df.columns)
    missing_data = pd.DataFrame({col: [0] for col in missing_cols})
    user_df = pd.concat([user_df, missing_data], axis=1)

    # Reorder the columns to match the training set
    user_df = user_df[X.columns]

    # Scale the user input data
    user_scaled = scaler.transform(user_df)

    # Predict loan status
    loan_status = model.predict(user_scaled)[0]

    return loan_status

# ==========================
# Example User Data for Prediction (example input)
# ==========================
user_data = {
    'Gender_Male': 1,
    'Married_Yes': 1,
    'Education_Graduate': 1,
    'Self_Employed_Unknown': 0,
    'Property_Area_Semiurban': 1,
    'Loan_Amount_Term': 10,
    'Total_Income': 6000,
    'ApplicantIncome': 4000,
    'CoapplicantIncome': 2000,
    'LoanAmount': 150
}

# Get loan status prediction
loan_status = predict_loan_status(user_data, model, scaler, df)
print(f"Loan Prediction: {'Approved' if loan_status == 1 else 'Rejected'}")

# Generate and display relevant charts
generate_top_features_chart()  # Top 3 features impact chart
generate_income_vs_loan_amount_chart()  # Income vs Loan Amount chart
generate_married_status_vs_loan_status_chart()  # Married Status vs Loan Approval chart
generate_credit_history_chart()  # Credit History vs Loan Approval chart
generate_employment_status_vs_loan_status_chart()  # Employment Status vs Loan Approval chart
