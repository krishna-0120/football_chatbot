import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="You are a professional football (soccer) expert. Answer only football-related questions."
)

def start_chatbot():

    chat = model.start_chat(history=[])
    
    print("⚽ Football AI Chatbot (Type 'exit' to stop) ⚽")

    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye! ⚽")
            break

        
        try:
            response = chat.send_message(user_input)
            print(f"\nBot: {response.text}")
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    start_chatbot()