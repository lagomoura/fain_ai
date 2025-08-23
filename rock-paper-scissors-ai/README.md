# Rock, Paper, Scissors AI

This project is a real-time Rock, Paper, Scissors game where you can play against an AI using hand gestures. The application uses your webcam to detect your hand movements and recognize your choice of rock, paper, or scissors.

## Features

- Real-time hand gesture recognition using MediaPipe.
- Play against an AI that makes random choices.
- Instant feedback with on-screen animations for wins and losses.
- Score tracking to see who's winning.

## Requirements

- Python 3.x
- OpenCV
- MediaPipe

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/rock-paper-scissors-ai.git
   cd rock-paper-scissors-ai
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. **Make sure your webcam is connected and working.**
2. **Run the `main.py` script:**
   ```bash
   python main.py
   ```
3. **Show your hand to the camera to make your choice.** The game will automatically detect your gesture and play against the AI.
4. **Press the `ESC` key to exit the game.**

## Project Structure

- `main.py`: The main script to run the game.
- `src/`: Contains the core modules of the application.
  - `game.py`: Handles the game logic, such as determining the winner.
  - `hand_gesture.py`: Recognizes hand gestures using MediaPipe.
  - `ui.py`: Displays the game's user interface.
  - `animations.py`: Manages the animations for wins and losses.
- `requirements.txt`: A list of the Python dependencies required for the project.
