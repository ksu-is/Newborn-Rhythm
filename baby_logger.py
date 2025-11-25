# Newborn Rhythm - Baby Care Logger
# Version 0.1 
# Created by Mariana Vazquez

import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Newborn Rhythm — Simple Logger")
        self.geometry("420x520")
        self.configure(bg="#111111")

        tk.Label(self, text="Newborn Rhythm", fg="#f0f0f0", bg="#111111",
                 font=("Arial", 18, "bold")).pack(pady=20)

if __name__ == "__main__":
    App().mainloop()
# Newborn Rhythm - Baby Care Logger
# Version 0.2 - added CSV helpers
# Created by Mariana Vazquez

import csv
import os
import tkinter as tk

CSV_PATH = "events.csv"

def ensure_csv():
    """Create the events.csv file with headers if it doesn't exist."""
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp_iso", "event_type"])

def read_events():
    """Read all events from the CSV file and return them as a list of dicts."""
    ensure_csv()
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Newborn Rhythm — Simple Logger")
        self.geometry("420x520")
        self.configure(bg="#111111")

        tk.Label(self, text="Newborn Rhythm", fg="#f0f0f0", bg="#111111",
                 font=("Arial", 18, "bold")).pack(pady=20)

if __name__ == "__main__":
    ensure_csv()
    App().mainloop()

