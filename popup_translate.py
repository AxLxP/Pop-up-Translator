import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import subprocess

def get_clipboard_text():
    try:
        result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except Exception as e:
        return f"Hata: {str(e)}"

def translate_text(text, dest='tr'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=dest)
        return translated.text
    except Exception as e:
        return f"Error: {str(e)}"

def show_popup(original, translated):
    root = tk.Tk()
    root.title("Translator")
    root.geometry("700x400")
    root.minsize(500, 300)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(3, weight=1)

    ttk.Label(root, text="Selected Text:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
    
    original_frame = ttk.Frame(root)
    original_frame.grid(row=1, column=0, sticky="nsew", padx=10)
    original_frame.rowconfigure(0, weight=1)
    original_frame.columnconfigure(0, weight=1)
    original_box = tk.Text(original_frame, wrap=tk.WORD)
    original_box.insert(tk.END, original)
    original_box.config(state='disabled')
    original_box.grid(row=0, column=0, sticky="nsew")

    original_scroll = ttk.Scrollbar(original_frame, command=original_box.yview)
    original_box.config(yscrollcommand=original_scroll.set)
    original_scroll.grid(row=0, column=1, sticky="ns")

    ttk.Label(root, text="Türkçe:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
    
    translated_frame = ttk.Frame(root)
    translated_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0,10))
    translated_frame.rowconfigure(0, weight=1)
    translated_frame.columnconfigure(0, weight=1)
    translated_box = tk.Text(translated_frame, wrap=tk.WORD)
    translated_box.insert(tk.END, translated)
    translated_box.config(state='disabled')
    translated_box.grid(row=0, column=0, sticky="nsew")

    translated_scroll = ttk.Scrollbar(translated_frame, command=translated_box.yview)
    translated_box.config(yscrollcommand=translated_scroll.set)
    translated_scroll.grid(row=0, column=1, sticky="ns")

    root.mainloop()

if __name__ == "__main__":
    selected_text = get_clipboard_text()
    translated = translate_text(selected_text)
    show_popup(selected_text, translated)

