# Newborn Rhythm - Baby Care Logger
# Version 0.5 - added since-last-feed timer
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

def since_last_feed_str():
    """Return a readable 'since last feed' time string."""
    rows = read_events()
    # Look backwards for most recent feed
    for r in reversed(rows):
        if r["event_type"] == "feed":
            t = datetime.fromisoformat(r["timestamp_iso"])
            delta = datetime.now(t.tzinfo) - t
            secs = int(delta.total_seconds())
            h, rem = divmod(secs, 3600)
            m, _ = divmod(rem, 60)
            if h > 0:
                return f"Since last feed: {h}h {m}m"
            else:
                return f"Since last feed: {m}m"
    return "Since last feed: —"

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Newborn Rhythm — Simple Logger")
        self.geometry("420x560")
        self.configure(bg="#111111")

        self.fg = "#f0f0f0"
        self.bg = "#111111"
        self.btn = "#222222"

        # Title
        tk.Label(self, text="Newborn Rhythm", fg=self.fg, bg=self.bg,
                 font=("Arial", 18, "bold")).pack(pady=10)

        # Buttons
        tk.Button(self, text="FEED", bg=self.btn, fg=self.fg,
                  font=("Arial", 18, "bold"), width=18, height=2,
                  command=lambda: self.log("feed")).pack(pady=8)

        tk.Button(self, text="DIAPER", bg=self.btn, fg=self.fg,
                  font=("Arial", 18, "bold"), width=18, height=2,
                  command=lambda: self.log("diaper")).pack(pady=8)

        tk.Button(self, text="SLEEP START", bg=self.btn, fg=self.fg,
                  font=("Arial", 18, "bold"), width=18, height=2,
                  command=lambda: self.log("sleep_start")).pack(pady=8)

        # Since-last-feed label
        self.since_label = tk.Label(
            self, text="Since last feed: —",
            fg=self.fg, bg=self.bg, font=("Arial", 12)
        )
        self.since_label.pack(pady=6)

        # History section
        tk.Label(self, text="Recent events", fg=self.fg, bg=self.bg,
                 font=("Arial", 12, "bold")).pack(pady=(12, 4))

        self.history = tk.Listbox(
            self, height=12, bg=self.btn, fg=self.fg,
            font=("Consolas", 11), activestyle="none"
        )
        self.history.pack(fill="both", expand=True, padx=12, pady=6)

        self.refresh_all()

    def log(self, event_type: str):
        """Log event then refresh timer + history."""
        append_event(event_type)
        self.refresh_all()

    def refresh_all(self):
        """Update 'since last feed' label and event history."""
        self.since_label.config(text=since_last_feed_str())

        # Refresh history
        self.history.delete(0, tk.END)
        rows = read_events()[-10:]
        for r in rows:
            ts = r["timestamp_iso"].replace("T", " ")
            self.history.insert(tk.END, f"{ts}  •  {r['event_type']}")

        # Auto-refresh every 30 seconds
        self.after(30_000, self.refresh_all)

if __name__ == "__main__":
    ensure_csv()
    App().mainloop()

