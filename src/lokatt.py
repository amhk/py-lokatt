from threading import Thread
import curses
import logging

import adb
import ctrl
import ui


class App(object):
    def __call__(self, window):
        ctx = ctrl.create_context(window)

        t1 = Thread(target=adb.logcat_worker,
                    args=(lambda x: ctx.queue.put((ctrl.EVENT_LOGCAT, x)), ))
        t1.daemon = True
        t1.start()

        t2 = Thread(target=ui.input_worker,
                    args=(ctx.root_window,
                          lambda x: ctx.queue.put((ctrl.EVENT_KEYPRESS, x))))
        t2.daemon = True
        t2.start()

        ctrl.main_loop(ctx)

if __name__ == '__main__':
    debug = False
    if debug:
        FORMAT = '%(filename)s:%(lineno)d: %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='/tmp/lokatt.log')
    else:
        logging.basicConfig(level=logging.CRITICAL + 1)

    curses.wrapper(App())
