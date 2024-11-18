from flask import Flask, request, jsonify
from main import model, scaler, df, predict_loan_status
import charts

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    # Get user data from the request
    user_data = request.json

    # Predict loan status
    loan_status = predict_loan_status(user_data, model, scaler, df)
    status = 'Approved' if loan_status == 1 else 'Rejected'
    message = "Your loan application seems likely to be approved." if loan_status == 1 else "Your loan application will most likely be rejected."

    # Generate charts and get base64-encoded images
    top_features_chart = charts.generate_top_features_chart(model, df.drop('Loan_Status_Y', axis=1),
                                                            ['Gender', 'Married', 'Education', 'Self_Employed',
                                                             'Property_Area', 'Credit_History'])
    income_vs_loan_chart = charts.generate_income_vs_loan_amount_chart(df)
    married_vs_loan_chart = charts.generate_married_status_vs_loan_status_chart(df)
    credit_history_chart = charts.generate_credit_history_chart(df)
    employment_status_chart = charts.generate_employment_status_vs_loan_status_chart(df)

    # Prepare response data
    response = {
        'loan_status': status,
        'message': f"{message}",
        'charts': {
            'Top Contributing Features': top_features_chart,
            'Income vs Loan Amount': income_vs_loan_chart,
            'Married to Loan Repayment Measure': married_vs_loan_chart,
            'Credit History to Loan': credit_history_chart,
            'Employment factor': employment_status_chart
        }
    }

    # Return the response as JSON with charts
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
