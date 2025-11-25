# Newborn Rhythm - Baby Care Logger
# Version 0.4 - added on-screen history list
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

        # --- HISTORY LABEL + LISTBOX ---
        tk.Label(self, text="Recent events", fg=self.fg, bg=self.bg,
                 font=("Arial", 12, "bold")).pack(pady=(12, 4))

        self.history = tk.Listbox(
            self, height=12, bg=self.btn, fg=self.fg,
            font=("Consolas", 11), activestyle="none"
        )
        self.history.pack(fill="both", expand=True, padx=12, pady=6)

        # Fill history when app starts
        self.refresh_history()

    def log(self, event_type: str):
        """Log a new event and refresh the list on screen."""
        append_event(event_type)
        self.refresh_history()

    def refresh_history(self):
        """Reload the last 10 events from the CSV into the listbox."""
        self.history.delete(0, tk.END)
        rows = read_events()
        last_rows = rows[-10:]  # show only last 10 events
        for r in last_rows:
            ts = r["timestamp_iso"].replace("T", " ")
            line = f"{ts}  •  {r['event_type']}"
            self.history.insert(tk.END, line)

if __name__ == "__main__":
    ensure_csv()
    App().mainloop()
