import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Use supported model
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash"
)


def get_ai_response(user_input, chat_history=None):
    """
    Generate AI response using Gemini API.
    """

    try:

        history_text = ""

        if chat_history:
            for role, msg in chat_history:
                history_text += f"{role}: {msg}\n"

        full_prompt = history_text + "User: " + user_input

        response = model.generate_content(
            full_prompt,
            generation_config={
                "temperature": 0.3,
                "top_p": 0.9,
                "max_output_tokens": 500
            }
        )

        return response.text

    except Exception as e:

        return f"Error generating response: {str(e)}"