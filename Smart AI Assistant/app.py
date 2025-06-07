from flask import Flask, request, jsonify, send_from_directory
import joblib, json, numpy as np
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

# Load regression models per category
models = joblib.load('budget_models.pkl')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/budget/status', methods=['POST'])
def budget_status():
    data = request.get_json()
    budgets    = data.get('budgets', {})      # {category: budget}
    cart_items = data.get('cartItems', [])     # [{category, amount}, ...]

    # Sum cart amounts by category
    cart_sum = {}
    for ci in cart_items:
        cart_sum[ci['category']] = cart_sum.get(ci['category'], 0) + ci['amount']

    status = []
    for cat, cart_amt in cart_sum.items():
        model = models.get(cat)
        pred_spend = float(model.predict(np.array([[12]]))[0])
        spent_so_far = pred_spend  # month-end forecast from historical
        user_budget = budgets.get(cat, 0)
        forecast_over = (spent_so_far + cart_amt) - user_budget
        status.append({
            'category': cat,
            'currentCart': cart_amt,
            'spentSoFar': round(spent_so_far),
            'budget': user_budget,
            'forecastOver': round(forecast_over)
        })

    # Example partner-card offer
    card_offer = {
        'bank': 'Bank X Platinum',
        'discount': '10%',
        'maxOff': 2000,
        'applyUrl': 'https://apply.bankx.com/platinum'
    }

    return jsonify({'status': status, 'cardOffer': card_offer})

if __name__ == '__main__':
    app.run(debug=True)
