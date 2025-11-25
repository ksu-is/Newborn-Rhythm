# Newborn Rhythm - Baby Care Logger
# Version 0.3 - added buttons + append_event
# Created by Mariana Vazquez

import csv
import os
from datetime import datetime, timezone
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

def now_iso():
    """Current timestamp in ISO format."""
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def append_event(kind):
    """Append a new event (feed, diaper, sleep) to the CSV file."""
    ensure_csv()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([now_iso(), kind])

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Newborn Rhythm — Simple Logger")
        self.geometry("420x520")
        self.configure(bg="#111111")

        # Colors
        self.fg = "#f0f0f0"
        self.bg = "#111111"
        self.btn = "#222222"

        tk.Label(self, text="Newborn Rhythm", fg=self.fg, bg=self.bg,
                 font=("Arial", 18, "bold")).pack(pady=10)

        # --- FEED BUTTON ---
        self.btn_feed = tk.Button(
            self, text="FEED", bg=self.btn, fg=self.fg,
            font=("Arial", 18, "bold"), width=18, height=2,
            command=lambda: self.log("feed")
        )
        self.btn_feed.pack(pady=8)

        # --- DIAPER BUTTON ---
        self.btn_diaper = tk.Button(
            self, text="DIAPER", bg=self.btn, fg=self.fg,
            font=("Arial", 18, "bold"), width=18, height=2,
            command=lambda: self.log("diaper")
        )
        self.btn_diaper.pack(pady=8)

        # --- SLEEP BUTTON ---
        self.btn_sleep = tk.Button(
            self, text="SLEEP START", bg=self.btn, fg=self.fg,
            font=("Arial", 18, "bold"), width=18, height=2,
            command=lambda: self.log("sleep_start")
        )
        self.btn_sleep.pack(pady=8)

        tk.Label(self, text="(Event saving not yet visible — will show history in Commit 4)",
                 fg=self.fg, bg=self.bg, font=("Arial", 10, "italic")).pack(pady=10)

    def log(self, event_type):
        append_event(event_type)

if __name__ == "__main__":
    ensure_csv()
    App().mainloop()
