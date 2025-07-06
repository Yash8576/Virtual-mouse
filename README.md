# Virtual Gesture-Controlled Mouse

A virtual mouse system for macOS that uses **hand gestures** to control the mouse pointer, clicks, scrolling, and zoom — all powered by **MediaPipe**, **OpenCV**, **PyAutoGUI**, and **NumPy**.

No physical mouse needed. Just your webcam and your hand.

---

## Demo
Adding soon

---

##  Features

-  **Thumb-Based Cursor Control**  
-  **Left Click** – Pinch **thumb + index finger** (within distance threshold)  
-  **Right Click** – Pinch **thumb + index + middle finger** together  
-  **Zoom In** – Open 3 fingers (index, middle, ring) and move upward  
-  **Zoom Out** – Move same 3 fingers to the right  
-  **Scroll** – Raise 4 fingers (index to pinky), move **up** to scroll down or **right** to scroll up  
-  Noise Filtering & Debouncing – Prevents accidental actions during motion

---

## How It Works

- **MediaPipe** detects hand and finger landmarks in real-time
- **OpenCV** accesses the webcam and visualizes detection
- **NumPy** is used to measure distances between fingertips
- **PyAutoGUI** translates gestures into system mouse/keyboard events

---

##  Requirements

- Python 3.8+
- macOS (tested) or any system that supports webcam + PyAutoGUI

###  Install dependencies:
```bash
pip install opencv-python mediapipe pyautogui numpy
