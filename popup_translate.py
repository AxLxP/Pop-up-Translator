import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import subprocess
import time
import os
import re

LANGUAGES = {
    "Turkish (tr)": "tr",
    "English (en)": "en",
    "German (de)": "de",
    "French (fr)": "fr",
    "Spanish (es)": "es",
    "Japanese (ja)": "ja",
    "Russian (ru)": "ru"
}

CONFIG_PATH = os.path.expanduser("~/.config/gpt_clip_translator")
LANG_FILE = os.path.join(CONFIG_PATH, "lang.cfg")

def simulate_copy():
    subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+c'])
    time.sleep(0.3)

def get_clipboard_text():
    try:
        result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except Exception as e:
        return f"Clipboard Error: {str(e)}"

def clean_copied_text(text):
    text = re.sub(r'(?<![.?!])\n(?!\n)', ' ', text)
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()

def translate_text(text, dest='tr'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=dest)
        return translated.text
    except Exception as e:
        return f"Translation Error: {str(e)}"

def load_last_language():
    if os.path.exists(LANG_FILE):
        with open(LANG_FILE, 'r') as f:
            lang = f.read().strip()
            if lang in LANGUAGES:
                return lang
    return "Turkish (tr)"

def save_last_language(lang_key):
    os.makedirs(CONFIG_PATH, exist_ok=True)
    with open(LANG_FILE, 'w') as f:
        f.write(lang_key)

def show_popup():
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.title("Translator")
    root.geometry("700x400")
    root.minsize(500, 300)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(4, weight=1)

    # ORİJİNAL METİN
    ttk.Label(root, text="Selected Text:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
    original_frame = ttk.Frame(root)
    original_frame.grid(row=1, column=0, sticky="nsew", padx=10)
    original_frame.rowconfigure(0, weight=1)
    original_frame.columnconfigure(0, weight=1)
    original_box = tk.Text(original_frame, wrap=tk.WORD)
    original_box.config(state='disabled')
    original_box.grid(row=0, column=0, sticky="nsew")
    ttk.Scrollbar(original_frame, command=original_box.yview).grid(row=0, column=1, sticky="ns")

    # DİL SEÇİMİ
    last_lang = load_last_language()
    ttk.Label(root, text="Target Language:", font=("Arial", 9)).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
    language_var = tk.StringVar(value=last_lang)
    language_select = ttk.Combobox(root, textvariable=language_var, values=list(LANGUAGES.keys()), state="readonly")
    language_select.grid(row=2, column=0, sticky="e", padx=10)

    # ÇEVİRİ
    ttk.Label(root, text="Translation:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=(10, 0))
    translated_frame = ttk.Frame(root)
    translated_frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=(0, 10))
    translated_frame.rowconfigure(0, weight=1)
    translated_frame.columnconfigure(0, weight=1)
    translated_box = tk.Text(translated_frame, wrap=tk.WORD)
    translated_box.config(state='disabled')
    translated_box.grid(row=0, column=0, sticky="nsew")
    ttk.Scrollbar(translated_frame, command=translated_box.yview).grid(row=0, column=1, sticky="ns")

    previous_text = ""

    def update_translation(text):
        original_box.config(state='normal')
        original_box.delete('1.0', tk.END)
        original_box.insert(tk.END, text)
        original_box.config(state='disabled')

        translated_box.config(state='normal')
        translated_box.delete('1.0', tk.END)
        target_code = LANGUAGES[language_var.get()]
        translated_text = translate_text(text, dest=target_code)
        translated_box.insert(tk.END, translated_text)
        translated_box.config(state='disabled')

    def on_language_change(*args):
        save_last_language(language_var.get())
        if previous_text:
            update_translation(previous_text)

    language_select.bind("<<ComboboxSelected>>", on_language_change)

    def check_clipboard():
        nonlocal previous_text
        current = clean_copied_text(get_clipboard_text())
        if current and current != previous_text:
            previous_text = current
            update_translation(current)
        root.after(1000, check_clipboard)

    # İlk açılışta bir kez simulate_copy çalışsın
    simulate_copy()
    current = clean_copied_text(get_clipboard_text())
    previous_text = current
    if current:
        update_translation(current)

    # Sonrasında sadece clipboard değişimini izle
    root.after(1000, check_clipboard)
    root.mainloop()

if __name__ == "__main__":
    show_popup()
