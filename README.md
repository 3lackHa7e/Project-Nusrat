# Project Nusrat 🌸

**An AI-powered, physics-driven desktop companion built with Electron and Gemini 2.5 Flash.**

Project Nusrat brings a classic "Shimeji" desktop pet to life by giving it a real-time physics engine, full screen-edge awareness, and a conversational AI brain. She drops onto your desktop, roams around your monitor, climbs your screen edges, and listens to your voice commands.

![Project Nusrat Screenshot](link-to-your-image-here.png) *(Note: Add a screenshot or GIF of her walking on your screen here!)*

## ✨ Features

* 🧠 **Gemini AI Brain:** Powered by Google's `gemini-2.5-flash` model for fast, intelligent conversational responses.
* 🏃‍♀️ **Custom Physics Engine:** Features real-time gravity, drag-and-drop mechanics, momentum, and collision detection. She won't just walk; she falls, bounces, and reacts to your screen boundaries.
* 🧗‍♀️ **Advanced Screen Interactions:** She dynamically detects your monitor's edges to climb walls, crawl upside down on the ceiling, and drop back down to the floor.
* 🎨 **Full State-Machine Animation:** Smoothly transitions between idle, walking, running, sitting, sleeping, climbing, dangling, and petting animations based on her AI "thoughts."
* 🎙️ **Voice Integration:** Built-in microphone triggers allow you to speak directly to her.
* 👻 **Ghost Window Technology:** The Electron app runs as a transparent, click-through overlay. You can use your computer and click your desktop icons completely normally while she walks over them.

## 🛠️ Tech Stack

* **Frontend (The Body):** Electron, HTML, CSS, Vanilla JavaScript
* **Backend (The Brain):** Python, Flask, Socket.IO
* **AI Integration:** Google Generative AI (Gemini API)
* **Communication:** Real-time bi-directional WebSockets

---

## 🚀 Installation & Setup

To run Project Nusrat, you will need to run the Python backend and the Electron frontend simultaneously.

### Prerequisites
* [Node.js](https://nodejs.org/) installed
* [Python 3.x](https://www.python.org/) installed
* A Google Gemini API Key

### 1. Backend Setup (The Brain)
Open your terminal and navigate to the backend folder:
```bash
cd backend
```
Install the required Python libraries (make sure you have your virtual environment set up if you use one):
```bash
pip install flask flask-socketio google-generativeai
```
*Note: Ensure your Gemini API key is properly configured in your `server.py` file or environment variables before running.*

### 2. Frontend Setup (The Body)
Open a new terminal and navigate to the root/frontend folder:
```bash
# If your package.json is in the root folder:
npm install
```
Ensure all your Shimeji `.png` frames are placed correctly inside the `frontend/assets/` folder.

---

## 🎮 How to Run

You need two terminal windows open to bring her to life.

**Terminal 1 (Start the Brain):**
```bash
cd backend
python server.py
```

**Terminal 2 (Start the Body):**
```bash
# In the folder containing your main.js and package.json
npm start
```

---

## 🕹️ Controls & Interactions

Project Nusrat is designed to be interactive without getting in the way of your daily tasks.

* **Hover:** Unlocks her from "Ghost Mode" so you can interact with her.
* **Click & Drag:** Grab her by the scruff, drag her anywhere on your monitor, and throw her. Gravity will handle the rest.
* **Single Click:** Give her a pet! She will pause her roaming and play a happy animation.
* **Double Click:** Activates the microphone. A chat bubble will appear, allowing you to speak to the Gemini AI.

---

## 📂 Folder Structure
```text
Project-Nusrat/
├── backend/
│   └── server.py          # Flask & Socket.IO server, Gemini API logic
├── frontend/
│   ├── assets/            # Shimeji .png animation frames
│   └── index.html         # Physics engine, AI state machine, WebSockets
├── main.js                # Electron window configuration & IPC routing
├── package.json           # Node dependencies
└── README.md
```

## 🤝 Contributing
Feel free to fork this project, submit pull requests, or use the physics engine to build your own custom desktop companions! If you add new animations or AI features, I'd love to see them.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Made with ❤️ by Abid!
</p>
