import PySimpleGUI as sg


def popup(message):
    global win
    if win:
        win.close()
    layout = [[sg.Text(message, background_color=bg, pad=(0, 0))]]
    win = sg.Window('title', layout, no_titlebar=True, keep_on_top=True,
        location=(1000, 200), auto_close=True, auto_close_duration=3,
        transparent_color=bg, margins=(0, 0))
    event, values = win.read(timeout=0)
    return win

bg = '#add123'
sg.set_options(font=("Courier New", 24))
layout = [[sg.Button('POPUP')]]
window = sg.Window('title', layout)
win = None
while True:

    event, value = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'POPUP':
        win = popup('Here is the message.')
        window.force_focus()

if win:
    win.close()
window.close()