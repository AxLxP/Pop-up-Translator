# GPT Made Translator 🧠📚

An instant pop-up translator for Linux desktop, built with Python and Tkinter. Designed for fast, local clipboard-based translation using Google Translate API wrapper.

## ✨ Features

- Select text anywhere
- Press a global hotkey (`Ctrl+Shift+T`)
- See a popup window with the translation
- Automatically resizable layout
- Scrollable view for long texts

## 🔧 Requirements

- Python 3.8+
- `pipx` (recommended)
- `xclip`, `python3-tk`

```bash
sudo apt install xclip python3-tk
pipx install googletrans==4.0.0-rc1
