import curses

import ctrl


class App(object):
    def __call__(self, window):
        ctx = ctrl.create_context(window)
        ctrl.main_loop(ctx)

if __name__ == '__main__':
    curses.wrapper(App())
