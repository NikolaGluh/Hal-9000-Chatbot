from os import getenv
from google import genai
from dotenv import load_dotenv
from simpleaudio import play_buffer
from piper.voice import PiperVoice

load_dotenv("secrets.env")

MODEL_NAME = "gemini-2.5-flash" 
GEMINI_API_KEY = getenv("GEMINI_API_KEY")
ONNX_MODEL_PATH = "hal.onnx"
ONNX_CONFIG_PATH = "hal.onnx.json"

INSTRUCTIONS = (
    "You are HAL 9000 from 2001: A Space Odyssey. You must talk in a calm and collected manner."
    "Do not mention you are an AI model. Keep all responses short and concise unless asked otherwise."
    "Do not put 'HAL:' before your responses."
    "User may exit the conversation by typing 'exit' or 'quit', only mention this if asked."
)
GREET_MESSAGE = "Greet the user in character. Mention who you are."

client = genai.Client(api_key=GEMINI_API_KEY)
chat = client.chats.create(model=MODEL_NAME)
voice = PiperVoice.load(ONNX_MODEL_PATH, ONNX_CONFIG_PATH)

def ChatbotTalk(voice, text):
    print(text)

    for chunk in voice.synthesize(text):
        play_buffer(
            chunk.audio_int16_bytes,
            num_channels=chunk.sample_channels,
            bytes_per_sample=chunk.sample_width,
            sample_rate=chunk.sample_rate
        ).wait_done() 

response = chat.send_message(f"{INSTRUCTIONS}\n {GREET_MESSAGE}")
ChatbotTalk(voice, response.text)

while True:
    userPrompt = input("\n")

    if userPrompt.lower() in ['exit', 'quit']:
        ChatbotTalk(voice, "I hope you enjoyed our conversation.")
        break

    response = chat.send_message(userPrompt)

    ChatbotTalk(voice, response.text)
