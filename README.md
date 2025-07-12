An instant popup translator for Linux desktop environments.  
Built with Python, Tkinter, and the Google Translate API (via `googletrans`) and made by ChatGPT.  
Select any text, copy it, hit a hotkey — and get the translation in a sleek popup window.

## Features

- Select or copy any text (e.g., in Okular or browser)
- Press your custom hotkey (like `Ctrl+Shift+T`)
- Instantly see a popup with the original and translated text
- Automatically resizable window
- Scrollable for long text
- Language auto-detect and selectable target language with last selection recognition. Also has line break correction.
- Lightweight & offline-capable
- Stays always on top and actively translates the new copied text. You can open put it in a side and translate what you copied.

![Translator Screenshot](Screenshot.png)

Installation Guide
=======================================

Step 1: Install required system packages
----------------------------------------
Open a terminal and run:

    sudo apt update
    sudo apt install python3-pip python3-tk xclip pipx

Step 2: Set up pipx (if not already)
------------------------------------
    pipx ensurepath

Then restart the terminal or source your shell config file:

    source ~/.bashrc   # or ~/.zshrc depending on your shell

Step 3: Install googletrans
---------------------------
    pipx install googletrans==4.0.0-rc1

This installs the translation library in an isolated environment.

Step 4: Clone the Repository
----------------------------
    git clone https://github.com/AxLxP/Pop-up-Translator.git
    cd Pop-up-Translator

Step 5: Make the Python script executable
-----------------------------------------
    chmod +x popup_translate.py

Step 6: Test it manually (optional)
-----------------------------------
Copy any text (Ctrl+C), then run:

    ~/.local/share/pipx/venvs/googletrans/bin/python3 popup_translate.py

A popup window should appear with the original and translated text.

Step 7: Create a Global Hotkey (for Cinnamon)
---------------------------------------------
1. Open: System Settings > Keyboard > Shortcuts > Custom Shortcuts
2. Click: "Add Custom Shortcut"
3. Name: Popup Translate
4. Command:

    ~/.local/share/pipx/venvs/googletrans/bin/python3 /full/path/to/popup_translate.py

5. Set hotkey: e.g., Ctrl+Shift+T

Now whenever you copy text and press your hotkey, the translator popup appears.

Done!


## 🪟 Windows Installation (using deep-translator)

### Requirements

- Python 3.8+: https://www.python.org/downloads/
- pip (comes with Python)
- Git (optional but recommended): https://git-scm.com/downloads

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Pop-up-Translator.git
cd Pop-up-Translator
```

Alternatively, download the ZIP file and extract it manually.

### 2. Install Required Python Packages

```bash
pip install deep-translator pyperclip
```

### 3. Run the Script

```bash
python popup_translate.py
```

A popup will appear and automatically translate any text you copy to the clipboard (Ctrl+C).

### 4. Add a Keyboard Shortcut (Optional)

#### Using AutoHotkey to Trigger with Ctrl + Shift + T

1. Download and install AutoHotkey from https://www.autohotkey.com
2. Create a new `.ahk` file on your desktop (e.g., `popup_hotkey.ahk`)
3. Right-click the file → Edit Script → paste the following:

```ahk
^+t::
Run, "C:\full\path\to\python.exe" "C:\full\path\to\popup_translate.py"
return
```

> Note: Replace `C:\full\path\to\...` with the actual paths to your Python executable and script file.

4. Double-click the `.ahk` file to launch it.  
   Now pressing **Ctrl + Shift + T** will open the translator popup.

### 5. Start Automatically with Windows (Optional)

1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Copy your `.ahk` file into the folder that opens.

The hotkey will now run automatically every time Windows starts.

