from Queue import PriorityQueue
import shlex

from cmd import get_command
from ui import BufferWindow, StatusbarWindow
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

    def get_number_of_entries(self):
        return len(self._entries)


class Statusbar(object):
    def __init__(self, window):
        self._window = window
        self._n = 0
        self._refresh_window()

    def _refresh_window(self):
        self._window.accept(self._n)

    def accept(self, buf):
        n = buf.get_number_of_entries()
        if n != self._n:
            self._n = n
            self._refresh_window()


def create_context(root_window):
    ctx = Context()
    ctx.queue = PriorityQueue()
    ctx.root_window = root_window
    ctx.done = False
    return ctx


def main_loop(ctx):
    win = BufferWindow(ctx.root_window)
    buf = Buffer(win)

    win = StatusbarWindow(ctx.root_window)
    statusbar = Statusbar(win)

    while not ctx.done:
        type_, data = ctx.queue.get()

        if type_ == EVENT_LOGCAT:
            buf.accept(data)
            statusbar.accept(buf)

        if type_ == EVENT_KEYPRESS:
            if data == ord('q'):
                _post_command(ctx, 'quit')

        if type_ == EVENT_COMMAND:
            name = data[0]
            argv = data[1:]
            cmd = get_command(name)
            if cmd is not None:
                try:
                    cmd(ctx, argv)
                except ValueError as e:
                    cmd = get_command('error')
                    argv = ['{}: {}'.format(name, e.message), ]
                    cmd(ctx, argv)
            else:
                cmd = get_command('error')
                argv = ['{}: command not found'.format(name), ]
                cmd(ctx, argv)

        refresh_ui()


def _post_command(ctx, argv):
    if type(argv) == str:
        argv = shlex.split(argv)
    ctx.queue.put((EVENT_COMMAND, argv))
