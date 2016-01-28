def input_worker(window, callback):
    while True:
        ch = window.getch()
        callback(ch)
