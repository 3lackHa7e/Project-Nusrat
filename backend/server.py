import os
import subprocess
import pygame
import time  # <-- This is the new import we needed!
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
# 2. SETUP GEMINI AI (Tuba's Brain)
# ==========================================
# PUT YOUR NEW, SAFE GEMINI API KEY HERE!
genai.configure(api_key="YOUR_API_KEY") 

# Using the 2.5 Flash model you requested!
model = genai.GenerativeModel('gemini-2.5-flash') 

# ==========================================
# 3. SPEECH RECOGNITION (Tuba's Ears)
# ==========================================
recognizer = sr.Recognizer()

def listen_and_think():
    with sr.Microphone() as source:
        print("Adjusting for background noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("\n🎤 LISTENING! Speak into your microphone now...")
        
        try:
            # Listen to your voice (waits up to 5 seconds for you to start talking)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing your speech...")
            
            # Convert voice to text
            user_text = recognizer.recognize_google(audio)
            print(f"Abid said: {user_text}")
            
            # Ask Gemini!
            print("Thinking...")
            response = model.generate_content(
                f"You are Tuba, a sweet, helpful desktop companion. Keep your answer short (1-2 sentences). Abid says: {user_text}"
            )
            
            ai_text = response.text
            print(f"Tuba says: {ai_text}")
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
    # When you Double-Click her, it sends 'manual_trigger'
    if data.get('text') == 'manual_trigger':
        
        # 1. Tell the speech bubble she is listening
        socketio.emit('response', {'text': 'Listening... 🎤'})
        
        # 2. Turn on the mic and get Gemini's answer
        ai_response = listen_and_think()
        
        # 3. Send the final answer to the speech bubble
        socketio.emit('response', {'text': ai_response})
        
        # 4. Make her jump for joy!
        socketio.emit('expression', {'mood': 'happy'})

        # ==========================================
        # 🔊 5. THE NEW BULLETPROOF AUDIO PLAYER
        # ==========================================
        try:
            print("Generating voice audio...")
            
            # 1. Clean the text so quotes/symbols don't break the Edge-TTS command
            safe_text = ai_response.replace('"', '').replace("'", "").replace('\n', ' ')
            
            # 2. Delete the old audio file so she doesn't accidentally repeat herself
            if os.path.exists("voice.mp3"):
                os.remove("voice.mp3")

            # 3. Create the new audio file using Ana's voice, bumped up in pitch and speed!
            # --rate=+10% makes her speak slightly faster
            # --pitch=+15Hz makes her voice higher and cuter
            command = f'python -m edge_tts --voice en-US-AnaNeural --rate=+10% --pitch=+15Hz --text "{safe_text}" --write-media voice.mp3'
            os.system(command)
            
            # 4. VERY IMPORTANT: Give Windows half a second to actually save the file!
            time.sleep(0.5)
            
            # 5. Play the audio
            if os.path.exists("voice.mp3"):
                print("Playing audio out loud...")
                pygame.mixer.init()
                pygame.mixer.music.load("voice.mp3")
                pygame.mixer.music.play()

                # Wait for her to finish speaking
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                    
                pygame.mixer.quit()
            else:
                print("Error: The voice.mp3 file was not created. Is edge-tts installed?")
            
        except Exception as e:
            print(f"Voice Error: {e}")

if __name__ == '__main__':
    print("Starting Tuba's Server on port 5000...")
    socketio.run(app, port=5000)
