import tkinter as tk
from datetime import timedelta

class CountdownTimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Countdown Timer")

        self.time_var = tk.StringVar()
        self.time_var.set("00:00:00")

        self.label = tk.Label(master, textvariable=self.time_var, font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.start_button = tk.Button(master, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="right", padx=10)

        self.timer_running = False
        self.end_time = None

    def start_timer(self):
        if not self.timer_running:
            self.end_time = timedelta(minutes=1)  # Set the countdown time (1 minute in this example)
            self.update_display()
            self.timer_running = True
            self.master.after(1000, self.update_timer)

    def update_timer(self):
        if self.timer_running:
            self.end_time -= timedelta(seconds=1)
            self.update_display()
            if self.end_time > timedelta(0):
                self.master.after(1000, self.update_timer)
            else:
                self.timer_running = False

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.end_time = None
        self.time_var.set("00:00:00")

    def update_display(self):
        seconds = self.end_time.total_seconds()
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        self.time_var.set(time_str)

def main():
    root = tk.Tk()
    app = CountdownTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
