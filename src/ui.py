import curses


class BufferWindow(object):
    def __init__(self, root_window):
        self._root_window = root_window
        self._window = root_window.subwin(0, 0)
        self._window.syncok(0)
        self._window.immedok(0)
        self._window.scrollok(1)
        self._window.idlok(1)

        self._maxy, self._maxx = self._window.getmaxyx()

    def _add_entry(self, entry):
        self._window.addnstr('{:20s} {}\n'.format(entry.tag[:20], entry.text), self._maxx)

    def _schedule_refresh(self):
        self._window.noutrefresh()

    def add_logcat_entry(self, entry):
        self._add_entry(entry)
        self._schedule_refresh()


def refresh():
    curses.doupdate()


def input_worker(window, callback):
    while True:
        ch = window.getch()
        callback(ch)
