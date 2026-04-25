import socketio
import uvicorn
from fastapi import FastAPI
import google.generativeai as genai
import speech_recognition as sr
import asyncio
import edge_tts
import os
import pygame # We use pygame to play the saved audio file
#Awareness (She Sees Your Screen)
import pyautogui
import base64
from io import BytesIO

async def see_screen():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    
    # Convert to format Gemini understands
    buffered = BytesIO()
    screenshot.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Update your process_command to handle "look" requests
async def process_command(text):
    text = text.lower()
    
    # If you ask her to look at something
    if "what is on my screen" in text or "look at this" in text:
        print("👀 Looking at screen...")
        await sio.emit('response', {'text': "Looking...", 'mood': 'observing'})
        
        # Get image
        img_data = await see_screen()
        
        # Ask Gemini with the image
        prompt = "Look at this screenshot of the user's computer. Explain what they are working on or looking at. Be brief."
        
        #^ those are bot Awareness (She Sees Your Screen)

# --- CONFIGURATION ---
GOOGLE_API_KEY = "AIzaSyBLO6ngoJ_i53U1SEvCp3idtb2zgRA6NFo" # <--- PASTE YOUR KEY AGAIN!

# Configure AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Configure Server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = FastAPI()
app.mount('/', socketio.ASGIApp(sio, app))

# Initialize Audio Player
pygame.mixer.init()

# --- NEW: WAIFU VOICE FUNCTION ---
async def speak_waifu(text):
    """Generates a cute voice using Edge TTS and plays it safely"""
    print(f"🔊 Waifu Speaking: {text}")
    
    voice = "en-US-AnaNeural" 
    output_file = "reply.mp3"
    
    try:
        # 1. Generate the audio file
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # 2. Initialize Mixer (if not already done)
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # 3. Load and Play
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # 4. Wait until it finishes talking
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        # 5. Unload the file so we can overwrite it next time
        pygame.mixer.music.unload()
            
    except Exception as e:
        print(f"❌ AUDIO ERROR: {e}")

# --- AI BRAIN ---
async def ask_gemini(text):
    try:
        prompt = f"You are a cute anime girl assistant. Your answers are short, sweet, and helpful. User said: {text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # --- PRINT THE REAL ERROR SO WE CAN SEE IT ---
        print("\n\n🔴 GEMINI ERROR DETAILS:")
        print(e)
        print("-----------------------------\n")
        return "I'm having trouble connecting to my brain..."
    

# Create a simple memory list
chat_history = []

async def ask_gemini(text):
    global chat_history
    
    # Add user text to history
    chat_history.append(f"User: {text}")
    
    # Keep history short (last 5 turns) so it doesn't get too big
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]
        
    # Build the full context
    full_conversation = "\n".join(chat_history)
    system_prompt = "You are a witty, helpful AI. Answer the user based on this conversation history:\n"
    
    try:
        response = model.generate_content(system_prompt + full_conversation)
        reply = response.text
        
        # Add AI reply to history
        chat_history.append(f"AI: {reply}")
        return reply
    except Exception as e:
        return "I forgot what we were talking about..."


# --- PROCESSING COMMANDS ---
async def process_command(text):
    text = text.lower()
    
    # 1. Notify Frontend
    await sio.emit('response', {'text': "Thinking...", 'mood': 'thinking'})
    
    # 2. Get AI Reply
    ai_reply = await ask_gemini(text)
    
    # 3. Send Text to Frontend
    await sio.emit('response', {'text': ai_reply, 'mood': 'happy'})
    
    # 4. Speak with Waifu Voice
    await speak_waifu(ai_reply)

# --- SERVER EVENTS ---
@sio.event
async def connect(sid, environ):
    print(f"Connected: {sid}")
    await sio.emit('response', {'text': "I'm ready!", 'mood': 'happy'})

@sio.event
async def process_voice(sid, data):
    print("\n--- 🎤 Manual Listen Triggered ---")
    
    # 1. VISUAL CUE: Tell Frontend to show "Listening..."
    await sio.emit('response', {'text': "Listening...", 'mood': 'listening'})
    
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    # CRITICAL FIX: Make it more sensitive to quiet voices
    recognizer.energy_threshold = 300  # Lower number = more sensitive
    recognizer.dynamic_energy_threshold = True
    
    with mic as source:
        try:
            # Short adjust for background noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening now... (Speak!)")
            
            # INCREASED TIMEOUT: Wait 10 seconds for you to start talking
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
            print("Processing audio...")
            text = recognizer.recognize_google(audio)
            print(f"✅ Heard: {text}")
            
            # Send to AI
            await process_command(text)
            
        except sr.WaitTimeoutError:
            print("❌ Error: You didn't speak in time.")
            await sio.emit('response', {'text': "I didn't hear anything...", 'mood': 'confused'})
        except sr.UnknownValueError:
            print("❌ Error: Could not understand audio.")
            await sio.emit('response', {'text': "Can you say that again?", 'mood': 'confused'})
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)