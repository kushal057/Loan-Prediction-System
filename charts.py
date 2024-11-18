import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def map_feature_names_to_original(coefficients, original_columns):
    original_feature_names = []
    for feature in coefficients.index:
        mapped = False
        for col in original_columns:
            if feature.startswith(col + '_'):
                original_feature_names.append(col)
                mapped = True
                break
        if not mapped:
            original_feature_names.append(feature)
    coefficients['Original_Feature'] = original_feature_names
    return coefficients

def generate_top_features_chart(model, X, original_columns):
    coefficients = pd.DataFrame(model.coef_.flatten(), X.columns, columns=['Coefficient'])
    coefficients = coefficients.sort_values(by='Coefficient', ascending=False)
    coefficients = map_feature_names_to_original(coefficients, original_columns)
    top_features = coefficients.head(3)

    plt.figure(figsize=(8, 6))
    sns.barplot(x=top_features['Original_Feature'], y=top_features['Coefficient'], palette='coolwarm')
    plt.title('Top 3 Features Impacting Loan Status')
    plt.xlabel('Feature')
    plt.ylabel('Coefficient Value')

    # Save the figure to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')
    return img_b64

def generate_income_vs_loan_amount_chart(df):
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Loan_Status_Y', y='Total_Income', data=df, palette='coolwarm')
    plt.title('Loan Approval by Total Income')
    plt.xlabel('Loan Approval Status')
    plt.ylabel('Total Income')

    # Save the figure to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')
    return img_b64

def generate_married_status_vs_loan_status_chart(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Married_Yes', hue='Loan_Status_Y', data=df, palette='coolwarm')
    plt.title('Loan Approval by Marital Status')
    plt.xlabel('Marital Status (Married = 1)')
    plt.ylabel('Loan Approval Count')

    # Save the figure to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')
    return img_b64

def generate_credit_history_chart(df):
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Credit_History', y='Loan_Status_Y', data=df, palette='coolwarm')
    plt.title('Loan Approval by Credit History')
    plt.xlabel('Credit History')
    plt.ylabel('Loan Approval Rate')

    # Save the figure to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')
    return img_b64

def generate_employment_status_vs_loan_status_chart(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Self_Employed_Unknown', hue='Loan_Status_Y', data=df, palette='coolwarm')
    plt.title('Loan Approval by Employment Status')
    plt.xlabel('Employment Status (Self-Employed = 1)')
    plt.ylabel('Loan Approval Count')

    # Save the figure to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')
    return img_b64
