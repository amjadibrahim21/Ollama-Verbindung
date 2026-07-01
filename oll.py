import tkinter as tk
import requests

import ttkbootstrap as tb
from ttkbootstrap.constants import *

app = tb.Window(themename="darkly")
def send():
    prompt = text_input.get("1.0", tk.END).strip()
    if not prompt:
        return

    # User-Feedback während des Wartens
    output.delete("1.0", tk.END)
    output.insert(tk.END, "Lade Antwort...")
    app.update() 

    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        })
        res.raise_for_status()
        data = res.json()

        output.delete("1.0", tk.END)
        output.insert(tk.END, data.get("response", "Keine Antwort erhalten."))
    except requests.exceptions.ConnectionError:
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Fehler: Verbindung zu Ollama konnte nicht hergestellt werden. Läuft der Server?")
    except Exception as e:
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"Ein Fehler ist aufgetreten: {str(e)}")




# UI Aufbau
app = tk.Tk()
app.title("Ollama UI")
app.geometry("400x400")

tk.Label(app, text="Prompt:").pack(pady=5)
text_input = tk.Text(app, height=5)
text_input.pack(padx=10, pady=5)

btn = tk.Button(app, text="Senden", command=send)
btn.pack(pady=10)

tk.Label(app, text="Antwort:").pack(pady=5)
output = tk.Text(app, height=10)
output.pack(padx=10, pady=5)
app.mainloop()