# ✋ GestureSense

**GestureSense** is a real-time hand gesture controller that lets you control your computer using just your hands — no touchpad or mouse needed. Powered by OpenCV, MediaPipe, and PyAutoGUI, this project transforms your webcam into a gesture-based input system.

## 🚀 Features

| Gesture                        | Action               |
| ------------------------------ | -------------------- |
| ☝️ Move index finger           | Control mouse cursor |
| 🤏 Pinch or index        | Left click & hold |
| 🤏 Pinch or middle       | Right click & hold |
| 👍 Raise thumb                 | Scroll up            |
| 👎 Lower thumb                 | Scroll down          |
| ✋ ASL alphabet               | Type "A", "B", "C" |
| 👈 Tuck in left thumb and rotate | Switch control modes |

---

## 🎮 Modes

You can switch between different gesture modes using your **left hand**:

* 🖱️ **Mouse Mode** — Move the cursor, click, and scroll.
* 🔤 **Typing Mode** — Type basic ASL letters like A, B, and C.
* 🧭 **Radial Mode** — Debug or expand with radial gesture detection.

---

## 💻 Requirements

* Python 3.7 or later
* A working webcam

### Python Packages

Install dependencies using pip:

```bash
pip install opencv-python mediapipe pyautogui
```

---

## 🛠️ Installation & Usage

1. Clone the repository:

```bash
git clone https://github.com/your-username/gesture-sense.git
cd gesture-sense
```

2. Run the main script:

```bash
python main.py
```

3. Raise your right hand and start interacting!

---

## ⚙️ Configuration

You can tweak the system to your liking by modifying these variables in `main.py`:

```python
pinch_threshold = 0.02
screen_width = 1920
screen_height = 1080
cursor_smoothing_factor = 0.5
```

---

## 🧠 How It Works

GestureSense uses:

* **MediaPipe Hands** — for fast, real-time hand and finger tracking
* **OpenCV** — for capturing and displaying video frames
* **PyAutoGUI** — to simulate mouse and keyboard actions

The system detects finger positions and angles, recognizes patterns (like pinches or hand shapes), and maps them to mouse or keyboard input.

---

## 🚧 Limitations

* ASL typing is limited to basic gestures (A–C) and is proof-of-concept.
* Hand tracking accuracy depends on lighting and webcam quality.

---

## 🙌 Acknowledgments

* [MediaPipe](https://github.com/google/mediapipe) by Google
* [OpenCV](https://opencv.org/)
* [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more info.

---

> By ephemera (crepes). <3

---