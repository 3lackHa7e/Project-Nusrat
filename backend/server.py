import os
import subprocess
import pygame
import time
import speech_recognition as sr
import google.generativeai as genai
from flask import Flask
from flask_socketio import SocketIO

# ==========================================
# 1. SETUP FLASK & SOCKET.IO
# ==========================================
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# ==========================================
# 2. SETUP GEMINI AI (Brain)
# ==========================================
# PUT YOUR NEW, SAFE GEMINI API KEY HERE!
genai.configure(api_key="YOUR_API_KEY") 

# Using the 2.5 Flash model!
model = genai.GenerativeModel('gemini-2.5-flash') 

# ==========================================
# 3. SPEECH RECOGNITION (Ears)
# ==========================================
recognizer = sr.Recognizer()

def listen_and_think():
    with sr.Microphone() as source:
        print("Adjusting for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("\n🎤 LISTENING! Speak into your microphone now...")
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing your speech...")
            
            user_text = recognizer.recognize_google(audio)
            print(f"Abid said: {user_text}")
            
            print("Thinking...")
            response = model.generate_content(
                f"You are Nusrat, a sweet, helpful desktop companion. Keep your answer short (1-2 sentences). Abid says: {user_text}"
            )
            
            ai_text = response.text
            print(f"Nusrat says: {ai_text}")
            return ai_text

        except sr.WaitTimeoutError:
            return "I didn't hear anything, Abid..."
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand what you said!"
        except Exception as e:
            print(f"Error: {e}")
            return "My brain had a little glitch!"

# ==========================================
# 4. SOCKET COMMUNICATION
# ==========================================
@socketio.on('connect')
def handle_connect():
    print("✅ Frontend connected! Tuba is awake.")

@socketio.on('process_voice')
def handle_voice(data):
    if data.get('text') == 'manual_trigger':
        
        socketio.emit('response', {'text': 'Listening... 🎤'})
        
        ai_response = listen_and_think()
        
        socketio.emit('response', {'text': ai_response})
        
        socketio.emit('expression', {'mood': 'happy'})

        # ==========================================
        # 🔊 5. THE NEW BULLETPROOF AUDIO PLAYER
        # ==========================================
        try:
            print("Generating voice audio...")
            
            safe_text = ai_response.replace('"', '').replace("'", "").replace('\n', ' ')
            
            if os.path.exists("voice.mp3"):
                os.remove("voice.mp3")

            # 3. Create the new audio file using Ana's voice, bumped up in pitch and speed!
            # --rate=+10% makes her speak slightly faster
            # --pitch=+15Hz makes her voice higher and cuter
            command = f'python -m edge_tts --voice en-US-AnaNeural --rate=+10% --pitch=+15Hz --text "{safe_text}" --write-media voice.mp3'
            os.system(command)
            
            time.sleep(0.5)
            
            if os.path.exists("voice.mp3"):
                print("Playing audio out loud...")
                pygame.mixer.init()
                pygame.mixer.music.load("voice.mp3")
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                    
                pygame.mixer.quit()
            else:
                print("Error: The voice.mp3 file was not created. Is edge-tts installed?")
            
        except Exception as e:
            print(f"Voice Error: {e}")

if __name__ == '__main__':
    print("Starting Nusrat's Server on port 5000...")
    socketio.run(app, port=5000)
