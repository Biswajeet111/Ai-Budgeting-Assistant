import requests
import os
from dotenv import load_dotenv

# Load environment variables (like API keys) from a .env file
load_dotenv()

# Fetch the Exchange Rate API key from environment variables
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")


def calculate_budget(income):
    """
    Applies the popular 50-30-20 budgeting rule to a given income.
    - 50% for Needs (Rent, Bills, Food)
    - 30% for Wants (Entertainment, Shopping)
    - 20% for Savings or Debt Repayment
    
    Args:
        income (float): Total monthly income.
        
    Returns:
        dict: A dictionary containing the calculated amounts for Needs, Wants, and Savings.
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
    Analyzes the total expenses and provides a brief summary/advice.
    
    Args:
        expenses (list): A list of expense records (tuples).
        
    Returns:
        str: A message indicating the financial health based on total spending.
    """
    if not expenses:
        return "No expenses recorded yet. Start by adding some to see your analysis!"

    # Sum up the amount column (index 1 in the tuple)
    total = sum([exp[1] for exp in expenses])

    if total > 20000:
        return f"Warning: Your total spending is ₹{total:.2f}. This is quite high. Consider reviewing your 'Wants' category."
    elif total > 10000:
        return f"Total spending: ₹{total:.2f}. You are within a moderate range. keep an eye on your budget."
    else:
        return f"Total spending: ₹{total:.2f}. excellent job! You're managing your finances very well."


def convert_currency(amount, from_currency="INR", to_currency="USD"):
    """
    Converts an amount from one currency to another using the ExchangeRate-API.
    
    Args:
        amount (float): The value to convert.
        from_currency (str): Source currency code (e.g., 'INR').
        to_currency (str): Target currency code (e.g., 'USD').
        
    Returns:
        float or str: The converted amount as a float, or an error message as a string.
    """
    if not EXCHANGE_API_KEY:
        return "Error: EXCHANGE_API_KEY not found in environment. Please check your .env file."

    try:
        # Construct the API request URL
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
        
        response = requests.get(url)
        data = response.json()

        if data.get("result") == "success":
            converted_amount = data["conversion_result"]
            return round(converted_amount, 2)
        else:
            return f"Conversion failed: {data.get('error-type', 'Unknown error')}"

    except Exception as e:
        return f"Network or API Error: {str(e)}"