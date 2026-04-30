import os
from dotenv import load_dotenv
from groq import Groq

# Load Groq API key from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(user_input, chat_history=None, system_instruction=None):
    """
    Generates a response from the Groq AI model.
    Uses system_instruction for persona and chat_history for context.
    """
    try:
        messages = []
        
        # Add system instruction if provided
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})

        # Add chat history (limiting to last 4 interactions)
        if chat_history:
            for role, msg in chat_history[-4:]:
                msg_role = "user" if role == "User" else "assistant"
                messages.append({"role": msg_role, "content": msg})

        # Add the current user input
        messages.append({"role": "user", "content": user_input})

        # Call the Groq API
        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.4,
            max_tokens=1000,
            top_p=0.9
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"I'm sorry, I'm having trouble processing that right now. (Error: {str(e)})"