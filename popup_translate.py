import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import subprocess
import time
import os
import re

# Language display name → Google Translate code
LANGUAGES = {
    "Turkish (tr)": "tr",
    "English (en)": "en",
    "German (de)": "de",
    "French (fr)": "fr",
    "Spanish (es)": "es",
    "Japanese (ja)": "ja",
    "Russian (ru)": "ru"
}

# Config path to store last used language
CONFIG_PATH = os.path.expanduser("~/.config/gpt_clip_translator")
LANG_FILE = os.path.join(CONFIG_PATH, "lang.cfg")

# Simulate Ctrl+C to copy selected text
def simulate_copy():
    subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+c'])
    time.sleep(0.3)  # Wait for clipboard to update

# Get clipboard contents
def get_clipboard_text():
    try:
        result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except Exception as e:
        return f"Clipboard Error: {str(e)}"

# Fix broken line endings in copied text
def clean_copied_text(text):
    # Replace line breaks that do not follow sentence-ending punctuation with space
    text = re.sub(r'(?<![.?!])\n(?!\n)', ' ', text)
    # Convert multiple line breaks to a single paragraph break
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()

# Translate using Google Translate
def translate_text(text, dest='tr'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=dest)
        return translated.text
    except Exception as e:
        return f"Translation Error: {str(e)}"

# Load last used language
def load_last_language():
    if os.path.exists(LANG_FILE):
        with open(LANG_FILE, 'r') as f:
            lang = f.read().strip()
            if lang in LANGUAGES:
                return lang
    return "Turkish (tr)"

# Save selected language
def save_last_language(lang_key):
    os.makedirs(CONFIG_PATH, exist_ok=True)
    with open(LANG_FILE, 'w') as f:
        f.write(lang_key)

# Show the GUI
def show_popup(original):
    root = tk.Tk()
    root.title("Translator")
    root.geometry("700x400")
    root.minsize(500, 300)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(4, weight=1)

    # Original text display
    ttk.Label(root, text="Selected Text:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
    original_frame = ttk.Frame(root)
    original_frame.grid(row=1, column=0, sticky="nsew", padx=10)
    original_frame.rowconfigure(0, weight=1)
    original_frame.columnconfigure(0, weight=1)
    original_box = tk.Text(original_frame, wrap=tk.WORD)
    original_box.insert(tk.END, original)
    original_box.config(state='disabled')
    original_box.grid(row=0, column=0, sticky="nsew")
    ttk.Scrollbar(original_frame, command=original_box.yview).grid(row=0, column=1, sticky="ns")

    # Language selector
    last_lang = load_last_language()
    ttk.Label(root, text="Target Language:", font=("Arial", 9)).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
    language_var = tk.StringVar(value=last_lang)
    language_select = ttk.Combobox(root, textvariable=language_var, values=list(LANGUAGES.keys()), state="readonly")
    language_select.grid(row=2, column=0, sticky="e", padx=10)

    # Translation output box
    ttk.Label(root, text="Translation:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=(10, 0))
    translated_frame = ttk.Frame(root)
    translated_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=(0, 10))
    translated_frame.rowconfigure(0, weight=1)
    translated_frame.columnconfigure(0, weight=1)
    translated_box = tk.Text(translated_frame, wrap=tk.WORD)
    translated_box.config(state='disabled')
    translated_box.grid(row=0, column=0, sticky="nsew")
    ttk.Scrollbar(translated_frame, command=translated_box.yview).grid(row=0, column=1, sticky="ns")

    # Translation logic
    def do_translation(*args):
        translated_box.config(state='normal')
        translated_box.delete('1.0', tk.END)
        lang_key = language_var.get()
        save_last_language(lang_key)
        target_code = LANGUAGES[lang_key]
        translated_text = translate_text(original, dest=target_code)
        translated_box.insert(tk.END, translated_text)
        translated_box.config(state='disabled')

    # Re-translate if language changes
    language_select.bind("<<ComboboxSelected>>", do_translation)

    # Translate on launch
    root.after(100, do_translation)

    root.mainloop()

# Main execution
if __name__ == "__main__":
    simulate_copy()
    raw_text = get_clipboard_text()
    selected_text = clean_copied_text(raw_text)
    show_popup(selected_text)
