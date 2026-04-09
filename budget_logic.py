import requests
import os
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")


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
            return "Currency conversion failed."

    except Exception as e:
        return f"Error: {str(e)}"