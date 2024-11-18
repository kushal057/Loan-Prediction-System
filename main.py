import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Load dataset
data_path = "data/train.csv"
df = pd.read_csv(data_path)

# Feature Engineering
df.fillna(df.median(numeric_only=True), inplace=True)
df['Self_Employed'] = df['Self_Employed'].fillna('Unknown')
df['Loan_Amount_Term'] = df['Loan_Amount_Term'] / 12
df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
df = pd.get_dummies(df, drop_first=True)

# Data Preprocessing
df = df.drop(columns=[col for col in df.columns if 'Loan_ID' in col])
X = df.drop('Loan_Status_Y', axis=1)
y = df['Loan_Status_Y']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model Building
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)


def predict_loan_status(user_data, model, scaler, df):
    user_df = pd.DataFrame([user_data])
    user_df = pd.get_dummies(user_df, drop_first=True)
    missing_cols = set(df.columns) - set(user_df.columns)
    missing_data = pd.DataFrame({col: [0] for col in missing_cols})
    user_df = pd.concat([user_df, missing_data], axis=1)
    user_df = user_df[X.columns]
    user_scaled = scaler.transform(user_df)
    loan_status = model.predict(user_scaled)[0]
    return loan_status