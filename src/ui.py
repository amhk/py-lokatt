import curses


class BufferWindow(object):
    def __init__(self, root_window):
        self._root_window = root_window
        rh, rw = root_window.getmaxyx()

        self._window = root_window.subwin(rh - StatusbarWindow.HEIGHT, rw, 0, 0)
        self._window.syncok(0)
        self._window.immedok(0)
        self._window.scrollok(1)
        self._window.idlok(1)
        self._window.leaveok(1)

        self._y = 0
        self._height, self._width = self._window.getmaxyx()

    def _add_entry(self, entry):
        if self._y >= self._height - 1:
            self._window.scroll(1)

        text = entry.text
        tag = entry.tag[:20]
        self._window.insnstr(self._y, 0, '{:20s} {}'.format(tag, text), self._width)

        if self._y < self._height - 1:
            self._y += 1

    def _schedule_refresh(self):
        self._window.noutrefresh()

    def add_logcat_entry(self, entry):
        self._add_entry(entry)
        self._schedule_refresh()

    def fill(self, entries):
        self._window.erase()
        self._y = 0
        for e in entries:
            self._add_entry(e)
        self._schedule_refresh()

    def height(self):
        return self._height


class StatusbarWindow(object):
    HEIGHT = 1

    def __init__(self, root_window):
        curses.curs_set(0)

        self._root_window = root_window
        rh, rw = root_window.getmaxyx()

        self._window = root_window.subwin(StatusbarWindow.HEIGHT, rw, rh - StatusbarWindow.HEIGHT, 0)
        self._window.syncok(0)
        self._window.immedok(0)
        self._window.scrollok(0)
        self._window.leaveok(1)

        self._height, self._width = self._window.getmaxyx()

    def _schedule_refresh(self):
        self._window.noutrefresh()

    def accept(self, n):
        self._window.erase()
        self._window.insnstr('[lokatt] {}{}'.format(n, ' ' * self._width), self._width, curses.A_BOLD | curses.A_REVERSE)
        self._schedule_refresh()


def refresh():
    curses.doupdate()


def input_worker(window, callback):
    while True:
        ch = window.getch()
        callback(ch)
