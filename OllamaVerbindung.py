import ttkbootstrap as tb
from ttkbootstrap.constants import *
import requests


def send():
    prompt = text_input.get("1.0", "end").strip()

    if not prompt:
        return

    output.delete("1.0", "end")
    output.insert("end", "Lade Antwort...")
    app.update()

    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        res.raise_for_status()

        data = res.json()


        output.delete("1.0", "end")
        output.insert("end", data.get("response", "Keine Antwort erhalten."))

    except requests.exceptions.ConnectionError:
        output.delete("1.0", "end")
        output.insert("end", "Fehler: Ollama läuft nicht oder ist nicht erreichbar.")

    except Exception as e:
        output.delete("1.0", "end")
        output.insert("end", f"Fehler:\n{e}")



app = tb.Window(themename="darkly")  
app.title("Ollama Chat")
app.geometry("700x600")
app.resizable(False, False)


title = tb.Label(
    app,
    text="Ollama Chat",
    font=("Arial", 20, "bold")
)
title.pack(pady=15)



prompt_label = tb.Label(
    app,
    text="Prompt:"
)
prompt_label.pack(anchor="w", padx=20)

text_input = tb.Text(
    app,
    height=6,
    font=("Arial", 11)
)
text_input.pack(fill="x", padx=20, pady=10)



send_button = tb.Button(
    app,
    text="Senden",
    bootstyle="success",
    command=send
)
send_button.pack(pady=10)



answer_label = tb.Label(
    app,
    text="Antwort:"
)
answer_label.pack(anchor="w", padx=20)

output = tb.Text(
    app,
    height=15,
    font=("Arial", 11)
)
output.pack(fill="both", expand=True, padx=20, pady=10)



app.mainloop()