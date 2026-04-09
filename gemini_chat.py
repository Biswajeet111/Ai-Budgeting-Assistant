import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API keys
load_dotenv()

# Configure Gemini API
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)


def get_ai_response(user_input, chat_history=None):
    """
    Generate AI response using Gemini API.
    """

    try:

        # Prepare chat history text
        history_text = ""

        if chat_history:
            for role, msg in chat_history:
                history_text += f"{role}: {msg}\n"

        # Full prompt
        full_prompt = (
            history_text
            + "User: "
            + user_input
        )

        # Generate response
        response = model.generate_content(
            full_prompt,
            generation_config={
                "temperature": 0.3,
                "top_p": 0.9
            }
        )

        return response.text

    except Exception as e:
        return f"Error generating response: {str(e)}"