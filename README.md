# Gesture-Sense

A real-time hand gesture recognition system built with OpenCV, MediaPipe, and PyAutoGUI. Control your mouse and keyboard using hand gestures captured via webcam.

## 📌 Features

- 🖱️ **Cursor Control** — Move the mouse with your hand (index finger).
- 👈 **Left Click** — Pinch or lower index finger to left-click and hold.
- 👉 **Right Click** — Pinch or lower middle finger to right-click and hold.
- 🖱️ **Scrolling** — Raise or lower the thumb to scroll up or down.
- 💬 **ASL-based Typing** (As a Proof of Concept) — Type letters like A, B, C with simple hand signs.
- 🔄 **Gesture-Based Mode Switching** — Switch between "mouse mode" and "typing mode" using hand gestures.
- 🎯 **Dual Hand Support** — Use right hand for control, left hand for mode switching.

## 📦 Requirements

- Python 3.7+
- Webcam

### Python Packages

Install via pip:

```bash
pip install opencv-python mediapipe pyautogui
```

## 🚀 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/your-username/hand-gesture-controller.git
cd hand-gesture-controller
```

2. Run the main script:

```bash
python main.py
```

3. Interact with your computer using your hands!

## 🧠 How It Works

This project uses:
- **MediaPipe Hands** to track hand landmarks in real-time.
- **PyAutoGUI** to trigger mouse and keyboard events.
- **OpenCV** to process webcam input and display visual feedback.

### Gesture Mappings

| Gesture                      | Action                     |
|-----------------------------|----------------------------|
| Index finger pinch/lower    | Left click & hold          |
| Middle finger pinch/lower   | Right click & hold         |
| Thumb raised                | Scroll up                  |
| Thumb lowered               | Scroll down                |
| Fist with thumb out         | Type 'A'                   |
| All fingers up              | Type 'B'                   |
| Curved fingers to left      | Type 'C'                   |
| Left thumb swipe            | Switch control modes       |

## ⚙️ Configuration

You can modify constants in the script to tweak performance:

```python
pinch_threshold = 0.02
cursor_smoothing_factor = 0.5
screen_width = 1920
screen_height = 1080
```

## 🧪 Known Limitations

- Typing functionality is limited to a few letters (A–C) and is just a proof-of-concept.
- Requires good lighting for accurate hand detection.
- Cursor precision may vary based on webcam quality and environment.

## 📚 Future Work

- Add gesture customization interface
- Expand ASL typing support
- Multi-hand simultaneous actions
- GUI overlay for feedback and settings

## 🙏 Credits

- [MediaPipe](https://github.com/google/mediapipe) by Google
- [OpenCV](https://opencv.org/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)

## 📝 License

This project is licensed under the MIT License. See `LICENSE` for details.

---

> Made with Love using Python & Computer Vision.
