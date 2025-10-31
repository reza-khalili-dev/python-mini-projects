# main.py
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from deep_translator import GoogleTranslator
import threading

# ---------------------------- Languages ---------------------------- #
LANGUAGES = {
    "Automatic": "auto",
    "English": "en",
    "Persian": "fa",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Russian": "ru",
    "Turkish": "tr",
    "Hindi": "hi",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Polish": "pl",
    "Indonesian": "id"
}

# ---------------------------- App UI ---------------------------- #
app = ttk.Window(title="Translator", themename="superhero", size=(900, 520))

top = ttk.Frame(app, padding=10)
top.pack(fill=X)

middle = ttk.Frame(app, padding=10)
middle.pack(fill=BOTH, expand=True)

bottom = ttk.Frame(app, padding=10)
bottom.pack(fill=X)

src_var = ttk.StringVar(value="Automatic")
dest_var = ttk.StringVar(value="Persian")

src_menu = ttk.Combobox(top, textvariable=src_var, values=list(LANGUAGES.keys()), width=25)
src_menu.pack(side=LEFT, padx=5)

dest_menu = ttk.Combobox(top, textvariable=dest_var, values=list(LANGUAGES.keys()), width=25)
dest_menu.pack(side=LEFT, padx=5)

# Swap button
def swap():
    s, d = src_var.get(), dest_var.get()
    src_var.set(d); dest_var.set(s)
    inp = input_text.get("1.0", END).strip()
    out = output_text.get("1.0", END).strip()
    input_text.delete("1.0", END); output_text.delete("1.0", END)
    input_text.insert("1.0", out); output_text.insert("1.0", inp)

swap_btn = ttk.Button(top, text="🔁 Swap", bootstyle="warning", command=swap)
swap_btn.pack(side=LEFT, padx=5)

# Fullscreen + Compact
full = False
compact = False

def toggle_full():
    global full
    full = not full
    app.attributes("-fullscreen", full)

def toggle_small():
    global compact
    compact = not compact
    app.geometry("700x400" if compact else "900x520")

ttk.Button(top, text="🖥 Fullscreen", bootstyle="info", command=toggle_full).pack(side=RIGHT, padx=5)
ttk.Button(top, text="⇳ Compact", bootstyle="secondary", command=toggle_small).pack(side=RIGHT)

# Text Areas
left = ttk.Frame(middle); right = ttk.Frame(middle)
left.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
right.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

ttk.Label(left, text="Input", font=("Segoe UI", 11, "bold")).pack(anchor="w")
input_text = tk.Text(left, font=("Segoe UI", 11), wrap="word")
input_text.pack(fill=BOTH, expand=True)

ttk.Label(right, text="Output", font=("Segoe UI", 11, "bold")).pack(anchor="w")
output_text = tk.Text(right, font=("Segoe UI", 11), wrap="word")
output_text.pack(fill=BOTH, expand=True)

status = ttk.StringVar(value="Ready ✅")
ttk.Label(bottom, textvariable=status, anchor="w").pack(fill=X, side=BOTTOM)

# Buttons
def clear_all():
    input_text.delete("1.0", END)
    output_text.delete("1.0", END)
    status.set("Cleared ✅")

ttk.Button(bottom, text="Clear", bootstyle="warning-outline", command=clear_all).pack(side=RIGHT, padx=5)

def copy_out():
    app.clipboard_clear()
    app.clipboard_append(output_text.get("1.0", END).strip())
    status.set("Copied ✅")

ttk.Button(bottom, text="Copy Output", bootstyle="secondary", command=copy_out).pack(side=RIGHT, padx=5)

# Translation
def translate():
    text = input_text.get("1.0", END).strip()
    if not text:
        status.set("Please type text first ⚠️")
        return

    def run():
        try:
            src = LANGUAGES[src_var.get()]
            dest = LANGUAGES[dest_var.get()]
            result = GoogleTranslator(source=src, target=dest).translate(text)
            output_text.delete("1.0", END)
            output_text.insert("1.0", result)
            status.set("Translated ✅")
        except Exception as e:
            output_text.insert("1.0", f"Error: {e}")
            status.set("Error ❌")

    threading.Thread(target=run).start()

translate_btn = ttk.Button(bottom, text="Translate (Ctrl+Enter)", bootstyle=SUCCESS, command=translate)
translate_btn.pack(side=RIGHT, padx=5)

# Shortcut
app.bind_all("<Control-Return>", lambda e: translate())

# Enable Ctrl+V (paste) in input_text
def paste_input(event=None):
    input_text.event_generate("<<Paste>>")
    return "break"

input_text.bind("<Control-v>", paste_input)  # Windows/Linux
input_text.bind("<Control-V>", paste_input)  # Handle Shift
input_text.bind("<Command-v>", paste_input)  # Mac

# Enable Ctrl+C (copy) in input_text
def copy_input(event=None):
    input_text.event_generate("<<Copy>>")
    return "break"

input_text.bind("<Control-c>", copy_input)
input_text.bind("<Control-C>", copy_input)
input_text.bind("<Command-c>", copy_input)


app.mainloop()
