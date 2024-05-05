import tkinter as tk
import time
import PySimpleGUI as sg

# TODO:
# - update window with time in-place
# - close popup window
# - timer with configurable time
# - stopwatch, timer toggle
# - settings from file, font

sg.set_options(font=("Courier New", 24))
#layout = [[sg.Button('POPUP')]]
#window = sg.Window('title', layout)

#win = None
bg_color = '#add123'
font = "Courier New"
font_size = 24

class FeroTimer(tk.Tk):

    def __init__(self):
        super().__init__()

        # Initialize variables
        self.start_time = None
        self.paused_time = 0
        self.paused = False
        width, height = 300, 150

        self.time_str = tk.StringVar()
        self.time_str.set("00:00:00")

        # Configure the main window
        #self.title("Transparent Stopwatch")
        #self.geometry(f"{width}x{height}")
        #self.attributes("-alpha", 1.0)  # Set transparency (0.0 = fully transparent, 1.0 = fully opaque)

        # Create and configure widgets
        #self.label = tk.Label(self, textvariable=self.time_str, font=(font, font_size))    #text="00:00:00"
        #self.label.pack(pady=20)

        #self.start_button = tk.Button(self, text="Start", command=self.start_stopwatch)
        #self.start_button.pack(side="left", padx=10)

        #self.pause_button = tk.Button(self, text="Pause", command=self.pause_stopwatch)
        #self.pause_button.pack(side="left", padx=10)

        #self.reset_button = tk.Button(self, text="Reset", command=self.reset_stopwatch)
        #self.reset_button.pack(side="right", padx=10)

        main_layout = [
            [sg.Text("00:00:00", key='time_text')],
            [sg.Button("Start")],
            [sg.Button("Pause")],
            [sg.Button("Reset")],
        ]
        main_window = sg.Window("FeroTimer", main_layout)

        timer_layout = [[sg.Text("oh", key='timer_text', background_color=bg_color, pad=(0, 0))]]
        timer_win = sg.Window('timer', timer_layout, no_titlebar=True, keep_on_top=True,
            location=(1000, 200), auto_close=False, auto_close_duration=1,
            transparent_color=bg_color, margins=(0, 0), finalize=True)

        def update_clock():
            if self.start_time is not None and not self.paused:
                elapsed_time = time.time() - self.start_time
                time_str = self.format_time(elapsed_time)
                self.label.config(text=time_str)
                timer_win['timer_text'].update(time_str)
                print(time_str)

            self.after(100, update_clock)  # Update every 100 milliseconds

        while True:
            event, values = main_window.read()

            if event == sg.WINDOW_CLOSED:
                break
            elif event == "Start":
                new_text = "XX:XX:XX"
                timer_win['timer_text'].update(new_text)
                self.start_stopwatch()

            # Update the stopwatch every 100 milliseconds
            update_clock()

        timer_win.close()

    def start_stopwatch(self):
        if self.start_time is None or self.paused:
            self.start_time = time.time() - self.paused_time
            self.paused = False

    def pause_stopwatch(self):
        if self.start_time is not None and not self.paused:
            self.paused_time = time.time() - self.start_time
            self.paused = True

    def reset_stopwatch(self):
        self.start_time = None
        self.paused_time = 0
        self.paused = False
        self.label.config(text="00:00:00")

    #def update_clock(self):
    #    if self.start_time is not None and not self.paused:
    #        elapsed_time = time.time() - self.start_time
    #        time_str = self.format_time(elapsed_time)
    #        self.label.config(text=time_str)
    #        self.timer_win['timer_text'].update(time_str)
    #        print(time_str)

    #    self.after(100, self.update_clock)  # Update every 100 milliseconds

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    app = FeroTimer()
    app.mainloop()
