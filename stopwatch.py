import tkinter as tk
from tkinter import ttk
import time
class StopwatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🕐 Elegant Stopwatch")
        self.root.geometry("550x550")
        self.root.config(bg="#1E1E2E")

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_count = 0

        tk.Label(root, text="⏱️ Stopwatch", font=("Verdana", 18, "bold"), fg="#FFD700", bg="#1E1E2E").pack(pady=10)

        self.time_display = tk.Label(root, text="00:00:00.000", font=("Courier New", 40, "bold"),
                                     fg="#FFD700", bg="#2A2D3E", padx=20, pady=10,
                                     relief="ridge", bd=5, width=15)
        self.time_display.pack(pady=10)

        btn_frame = tk.Frame(root, bg="#1E1E2E")
        btn_frame.pack(pady=10)

        self.start_btn = self.create_button(btn_frame, "▶ Start", "#27AE60", self.start)
        self.split_btn = self.create_button(btn_frame, "⏸ Split", "#2980B9", self.split)
        self.pause_btn = self.create_button(btn_frame, "⏯ Pause", "#E67E22", self.pause)
        self.reset_btn = self.create_button(btn_frame, "🔄 Reset", "#C0392B", self.reset)

        lap_frame = tk.Frame(root, bg="#1E1E2E")
        lap_frame.pack(pady=10, fill="both", expand=True)

        self.lap_list = ttk.Treeview(lap_frame, columns=("Lap", "Time"), show="headings", height=12)
        self.lap_list.heading("Lap", text="🏁 Lap #", anchor="center")
        self.lap_list.heading("Time", text="⏱️ Split Time", anchor="center")
        self.lap_list.column("Lap", width=80, anchor="center")
        self.lap_list.column("Time", width=200, anchor="center")

        scrollbar = ttk.Scrollbar(lap_frame, orient="vertical", command=self.lap_list.yview)
        self.lap_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.lap_list.pack(side="left", fill="both", expand=True)

        self.update_display()

    def create_button(self, frame, text, color, command):
        """Creates Stylish Buttons"""
        btn = tk.Button(frame, text=text, font=("Arial", 13, "bold"), bg=color,
                        fg="white", width=8, height=1, activebackground="#34495E",
                        relief="raised", bd=5, command=command, padx=5, pady=3)
        btn.pack(side="left", padx=8)
        return btn

    def update_display(self):
        """Updates the stopwatch display every 10ms"""
        if self.running:
            current_time = time.time() - self.start_time + self.elapsed_time
            formatted_time = self.format_time(current_time)
            self.time_display.config(text=formatted_time)
        self.root.after(10, self.update_display)

    def format_time(self, seconds):
        """Formats time into HH:MM:SS.MS"""
        millis = int((seconds - int(seconds)) * 1000)
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"

    def start(self):
        """Starts the stopwatch"""
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True

    def pause(self):
        """Pauses the stopwatch"""
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running = False

    def reset(self):
        """Resets the stopwatch and clears splits"""
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_count = 0
        self.time_display.config(text="00:00:00.000")
        self.lap_list.delete(*self.lap_list.get_children())

    def split(self):
        """Records a split time while the stopwatch continues"""
        if self.running:
            self.lap_count += 1
            split_time = self.format_time(time.time() - self.start_time + self.elapsed_time)
            self.lap_list.insert("", "end", values=(f"#{self.lap_count}", split_time))
            self.lap_list.yview_moveto(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
