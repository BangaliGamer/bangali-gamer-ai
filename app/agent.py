import google.generativeai as genai
from app.config import Config
from app.prompts import get_system_instruction

class BangaliGamerAgent:
    def __init__(self, is_admin=False):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # Load the right instructions based on user role
        self.model = genai.GenerativeModel(
            model_name="gemini-3.5-flash",
            system_instruction=get_system_instruction(is_admin)
        )
        
        self.chat_session = self.model.start_chat(history=[])

    def get_response(self, user_message: str) -> str:
        try:
            response = self.chat_session.send_message(user_message)
            return response.text
        except Exception as e:
            return f"[System Error] AI Agent failed to connect. Error: {str(e)}"