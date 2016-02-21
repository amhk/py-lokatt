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
        self._scroll = True

    def _split_range(self, values, count, lineno, anchor):
        if anchor not in ('top', 'middle', 'bottom'):
            raise ValueError('bad anchor value {}'.format(anchor))

        if lineno < 0:
            lineno = len(values) + lineno + 1

        if anchor == 'top':
            low = lineno - 1
            high = low + count
            return values[low:high]

        elif anchor == 'middle':
            if count % 2 != 0:
                low = lineno - 1 - count / 2
            else:
                low = lineno - count / 2
            high = low + count
            return values[low:high]

        else:
            low = lineno - count
            high = lineno
            if low < 0:
                return values[:high]
            else:
                return values[low:high]

    def accept(self, entry):
        # TODO: if entry does not pass filter, bail
        self._entries.append(entry)
        if self._scroll:
            self._window.add_logcat_entry(entry)

    def get_number_of_entries(self):
        return len(self._entries)

    def goto_line(self, lineno, anchor):
        if lineno == 0:
            raise ValueError('bad line value 0')
        if anchor not in ('top', 'middle', 'bottom'):
            raise ValueError('bad anchor value {}'.format(anchor))

        self._scroll = False

        height = self._window.height()
        entries = self._split_range(self._entries, height, lineno, anchor)
        self._window.fill(entries)


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
    ctx.buf = None
    ctx.statusbar = None
    return ctx


def main_loop(ctx):
    win = BufferWindow(ctx.root_window)
    ctx.buf = Buffer(win)

    win = StatusbarWindow(ctx.root_window)
    ctx.statusbar = Statusbar(win)

    while not ctx.done:
        type_, data = ctx.queue.get()

        if type_ == EVENT_LOGCAT:
            ctx.buf.accept(data)
            ctx.statusbar.accept(ctx.buf)

        if type_ == EVENT_KEYPRESS:
            if data == ord('q'):
                _post_command(ctx, 'quit')
            if data == ord('1'):
                _post_command(ctx, 'goto-line --lineno=1 --anchor=top')
            if data == ord('2'):
                _post_command(ctx, 'goto-line --lineno=100 --anchor=middle')
            if data == ord('3'):
                _post_command(ctx, 'goto-line --lineno=-1 --anchor=bottom')

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
