from Queue import PriorityQueue

from ui import BufferWindow
from ui import refresh as refresh_ui


EVENT_COMMAND = 10
EVENT_KEYPRESS = 20
EVENT_LOGCAT = 30


class Context:
    pass


class Buffer(object):
    def __init__(self, window):
        self._entries = []
        self._window = window

    def accept(self, entry):
        # TODO: if entry does not pass filter, bail
        self._entries.append(entry)
        self._window.add_logcat_entry(entry)


def create_context(root_window):
    ctx = Context()
    ctx.queue = PriorityQueue()
    ctx.root_window = root_window
    ctx.done = False
    return ctx


def main_loop(ctx):
    win = BufferWindow(ctx.root_window)
    buf = Buffer(win)

    while not ctx.done:
        type_, data = ctx.queue.get()

        if type_ == EVENT_LOGCAT:
            buf.accept(data)

        if type_ == EVENT_KEYPRESS:
            if data == ord('q'):
                ctx.done = True

        refresh_ui()
