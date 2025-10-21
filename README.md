# DrawIt

# Hand Tracking Drawing App

This is a Python-based hand tracking application that allows users to draw on a virtual canvas using only their hands. It uses the webcam feed, tracks the user's hand with MediaPipe, and enables drawing when the user pinches their thumb and index finger together.

The canvas appears as an overlay on the video feed, and users can change colors or clear the canvas using simple keyboard inputs. There is no graphical user interface—everything is handled via OpenCV windows and the webcam.

## How it works

1. The webcam feed is captured using OpenCV.
2. MediaPipe detects hand landmarks in real-time.
3. When the thumb and index fingertips are close together (a pinch gesture or similar to holding a pencil), drawing mode activates.
4. The fingertip position is smoothed over recent frames to reduce jitter.
5. Lines are drawn on a canvas NumPy array.
6. The canvas is composited with the live camera feed and displayed.

## Installation

Clone the repository and install dependencies:

    git clone https://github.com/kyledo67/handtracker.git
    cd handtracker
    pip install -r requirements.txt

Dependencies:

- opencv-python
- mediapipe
- numpy

## Running the application

To launch:

    python main.py

A window will open displaying the camera feed. Once your hand is detected, pinch your thumb and index finger to start drawing.

## Controls

- Press 'q' to quit the program
- Press 'c' to clear the canvas
- Press 'r' to set drawing color to red
- Press 'g' to set drawing color to green
- Press 'b' to set drawing color to blue

## File structure

    your-folder/
    ├── main.py
    ├── requirements.txt
    └── README.md

## Notes

- A webcam is required for this application to function.
- The application does not include a frontend—interaction.
