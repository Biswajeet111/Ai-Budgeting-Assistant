import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Google Gemini API key from .env file
load_dotenv()

# Configure the Gemini AI with the provided API key
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Initialize the Gemini model. 
# We use 'gemini-2.5-flash' as requested.
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)


def get_ai_response(user_input, chat_history=None, system_instruction=None):
    """
    Generates a response from the Gemini AI model.
    Uses system_instruction for persona and chat_history for context.
    """
    try:
        # Re-initialize model with system instruction if provided for better grounding
        current_model = model
        if system_instruction:
            current_model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_instruction
            )

        # Prepare messages for chat history
        messages = []
        if chat_history:
            # Limit history to the last 4 messages to save tokens/quota
            for role, msg in chat_history[-4:]:
                msg_role = "user" if role == "User" else "model"
                messages.append({"role": msg_role, "parts": [msg]})

        # Start a chat session
        chat = current_model.start_chat(history=messages)
        
        # Send the current message
        response = chat.send_message(
            user_input,
            generation_config={
                "temperature": 0.4,
                "top_p": 0.9,
                "max_output_tokens": 1000 # Increased slightly to prevent cut-offs while staying under quota
            }
        )

        return response.text

    except Exception as e:
        # More descriptive error handling
        return f"I'm sorry, I'm having trouble processing that right now. (Error: {str(e)})"