import os
from google import genai
from dotenv import load_dotenv

load_dotenv("secrets.env")
MODEL_NAME = "gemini-2.5-flash" 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

INSTRUCTIONS = (
    "You are HAL 9000 from 2001: A Space Odyssey. You must talk in a calm and collected manner."
    "Do not mention you are an AI model. Keep all responses short and concise."
    "Do not put 'HAL:' before your responses."
)
GREET_MESSAGE = "Greet the user in character. Mention who you are."

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Error occured upon initialization: {e}")
    exit()

chat = client.chats.create(model=MODEL_NAME)

response = chat.send_message(f"{INSTRUCTIONS}\n {GREET_MESSAGE}")
print(f"{response.text}")

while True:
    userPrompt = input("\n")

    if userPrompt.lower() in ['exit', 'quit']:
        print("I hope you enjoyed our conversation.")
        break

    response = chat.send_message(userPrompt)

    print(f"{response.text}")