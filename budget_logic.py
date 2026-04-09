import requests
import os
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")


def calculate_budget(income):
    """
    Apply 50-30-20 budgeting rule.
    """

    needs = income * 0.5
    wants = income * 0.3
    savings = income * 0.2

    return {
        "Needs": round(needs, 2),
        "Wants": round(wants, 2),
        "Savings": round(savings, 2)
    }


def analyze_expenses(expenses):
    """
    Analyze total expenses.
    """

    if not expenses:
        return "No expenses recorded yet."

    total = sum([exp[1] for exp in expenses])

    if total > 20000:
        return "Your spending is high. Try reducing unnecessary expenses."

    elif total > 10000:
        return "Your spending is moderate. Keep tracking regularly."

    else:
        return "Good job managing expenses!"


def convert_currency(amount, from_currency="INR", to_currency="USD"):
    """
    Convert currency using ExchangeRate API.
    """

    try:

        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"

        response = requests.get(url)

        data = response.json()

        if data["result"] == "success":

            converted_amount = data["conversion_result"]

            return round(converted_amount, 2)

        else:
            return "Conversion failed."

    except Exception as e:

        return f"Error: {str(e)}"