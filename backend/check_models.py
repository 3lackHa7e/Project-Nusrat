import google.generativeai as genai
import os

# Paste your API Key here
GOOGLE_API_KEY = "Your_API_Key_Here"
genai.configure(api_key=GOOGLE_API_KEY)

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")