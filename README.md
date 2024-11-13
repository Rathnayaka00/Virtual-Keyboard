# Hand Gesture-Based Virtual Keyboard

## Overview:
This project demonstrates a hand gesture-based virtual keyboard that allows users to type by detecting hand gestures in real-time using **OpenCV**, **cvzone**, and **pynput**. The system maps hand gestures to keyboard buttons, making it a fun and innovative way to interact with a computer.

## Features:
- **Hand Gesture Detection:** The system detects hand gestures using OpenCV and **cvzone HandTrackingModule**.
- **Virtual Keyboard:** It includes keys for lowercase, uppercase, backspace, space, enter, and caps lock functionality.
- **Customizable Background:** You can modify the background image of the virtual keyboard interface.

## Technologies Used:
- **Python 3.x**
- **OpenCV** for real-time video processing
- **cvzone** for hand detection and interaction
- **pynput** for controlling the keyboard
- **NumPy** for array operations

## How It Works:
1. **Hand Tracking:** The webcam captures the hand in front of it, and **cvzone** is used to track and detect the position of the hand.
2. **Gesture to Key Mapping:** The tracked hand gestures are mapped to keys on a virtual keyboard displayed on the screen.
3. **Keyboard Control:** The **pynput** library simulates keypresses on the system based on detected gestures.

## How to Run:
1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/Rathnayaka00/Virtual-Keyboard.git
    ```
2. Install the required dependencies:
    ```bash
    pip install opencv-python cvzone pynput numpy
    ```
3. Run the `gesture_keyboard.py` file:
    ```bash
    python gesture_keyboard.py
    ```
4. The system will open the webcam and start detecting hand gestures. Interact with the virtual keyboard using your hand movements!

## Contributing:
Feel free to fork the repository and submit pull requests. Any contributions are welcome!

## License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
