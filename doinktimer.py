from datetime import datetime
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import time
import threading
import PySimpleGUI as sg

settings_file = 'config.txt'
runner_file = 'timer.txt'

start_time = 0
end_time = 0
paused_time = 0
countdown_seconds = 0
paused = True
was_reset = False
countdown = False
time_text = "00:00:00"
main_window = None
timer_window = None
timer_location = (100, 100)
WHITE = '#ffffff'
BLACK = '#000000'


def main():
    global main_window
    global timer_window

    settings = read_settings(settings_file)
    font = settings.get('font')
    main_font_size = settings.get('main_font_size')
    main_timer_font_size = settings.get('main_timer_font_size')
    timer_font_size = settings.get('timer_font_size')
    bg_color = settings.get('bg_color')
    timer_color = settings.get('timer_color')

    sg.set_options(font=(font, main_font_size))

    if timer_color == bg_color and bg_color == BLACK:
        bg_color = WHITE

    # Timer window with transparent background
    timer_layout = [
        [sg.Text(time_text, key='timer_text', text_color=timer_color, background_color=bg_color,
                 pad=(0, 0), font=(font, timer_font_size))]
    ]
    timer_window = sg.Window('timer', timer_layout, no_titlebar=False, keep_on_top=True,
                             location=timer_location, auto_close=False, transparent_color=bg_color,
                             margins=(0, 0), finalize=True)
    # Main control window
    main_layout = [
        [sg.Text(time_text, key='timer_text', font=(font, main_timer_font_size))],
        [sg.Button("Start", size=(6, 1)), sg.Button("Pause", size=(6, 1)), sg.Button("Reset", size=(6, 1))],
        [sg.Button("Set", size=(6, 1)), sg.Input(key="input_time", size=(12, 1), enable_events=True)],
    ]
    main_window = sg.Window("DoinkTimer", main_layout, resizable=True)

    observer_thread = threading.Thread(target=start_observer)
    observer_thread.start()

    reset_config()

    try:
        while True:

            timer_event, timer_values = timer_window.read(timeout=0)
            if timer_event == sg.WINDOW_CLOSED:
                break

            event, values = main_window.read(timeout=0)
            if event == sg.WINDOW_CLOSED:
                break
            elif event == "Start":
                start_stopwatch()
            elif event == "Pause":
                pause_stopwatch()
            elif event == "Reset":
                reset_stopwatch()
            elif event == "Set":
                set_stopwatch(values["input_time"])

            update_clock()
    except KeyboardInterrupt:
        observer_thread.join()


def start_stopwatch():
    global start_time
    global end_time
    global paused
    global paused_time
    global countdown
    global countdown_seconds
    if paused:
        paused = False
        if not countdown:
            start_time = time.time() - paused_time
        else:
            start_time = time.time() - paused_time
            #countdown_seconds = calculate_seconds(end_time)
            end_time = time.time() + countdown_seconds - paused_time
        print("Timer started.")


def pause_stopwatch():
    global start_time
    global paused
    global paused_time
    if start_time is not None and not paused:
        paused_time = time.time() - start_time
        paused = True
        print("Timer paused. " + str(paused_time))


def reset_stopwatch():
    global start_time
    global paused
    global paused_time
    global countdown
    global was_reset
    global countdown_seconds
    paused = True
    start_time = 0
    paused_time = 0
    countdown_seconds = 0
    countdown = False
    was_reset = True
    print("Timer reset.")


def set_stopwatch(input_time):
    global start_time
    global end_time
    global countdown
    global countdown_seconds
    global was_reset
    try:
        # Try to convert the input value to time
        datetime.strptime(input_time, "%H:%M:%S").time()
        countdown = True
        countdown_seconds = calculate_seconds(input_time)
        was_reset = True
        print("Timer set to " + input_time)
    except ValueError:
        sg.popup_error("Please enter a valid time (HH:MM:SS).")


def update_timers(new_time):
    global timer_window
    global main_window
    timer_window['timer_text'].update(new_time)
    main_window['timer_text'].update(new_time)


# Check the runner text file for "remote" interaction
def check_runner_command():
    config = read_settings(runner_file)
    command = config.get('command')

    print("Reading command from runner file: " + command)
    if command == 'start':
        start_stopwatch()
    elif command == 'pause':
        pause_stopwatch()
    elif command == 'reset':
        reset_stopwatch()
    elif command == 'set':
        settings = read_settings(settings_file)
        set_time = settings.get('countdown_time')
        set_stopwatch(set_time)
    else:
        return False

    reset_config()
    return True


def update_clock():
    global start_time
    global paused
    global was_reset
    if not paused:
        if not countdown:
            elapsed_time = time.time() - start_time
            update_timers(format_time(elapsed_time)) # need a way to just tell it zero here when reset case hit
        else:
            elapsed_time = end_time - time.time()
            update_timers(format_time(elapsed_time))
            if elapsed_time <= 0:
                reset_stopwatch()

        if start_time == 0:
            paused = True
            return
    elif was_reset:
        update_timers(format_time(countdown_seconds))
        was_reset = False


def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def calculate_seconds(time_str):
    input_time = datetime.strptime(time_str, "%H:%M:%S").time()
    return input_time.hour * 3600 + input_time.minute * 60 + input_time.second


def read_settings(file_path):
    settings = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line into key and value
                key, value = line.strip().split('=')
                settings[key] = value
    except FileNotFoundError:
        print(f"Settings file not found: {file_path}")
    except Exception as e:
        print(f"Error reading settings: {e}")
    return settings


def reset_config():
    with open('timer.txt', 'w') as file:
        file.write('command=none\n')


def start_observer():
    event_handler = RunnerHandler()
    observer = PollingObserver()
    observer.schedule(event_handler, runner_file, recursive=False)
    observer.start()
    observer.is_alive()


class RunnerHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(event)
        check_runner_command()


if __name__ == "__main__":
    main()
