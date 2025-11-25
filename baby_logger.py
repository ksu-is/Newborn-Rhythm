# Newborn Rhythm - Baby Care Logger
# Version 0.1 (placeholder)
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

