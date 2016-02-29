from threading import Thread
import argparse
import curses
import logging

import adb
import ctrl
import ui


def _main(window, *_, **kwargs):
    args = kwargs['args']

    ctx = ctrl.create_context(window)

    path = None
    if args.input:
        path = args.input.name
    t1 = Thread(target=adb.logcat_worker,
                args=(lambda x: ctx.queue.put((ctrl.EVENT_LOGCAT, x)), ),
                kwargs={'path': path, 'lambd': args.random_delay})
    t1.daemon = True
    t1.start()

    t2 = Thread(target=ui.input_worker,
                args=(ctx.root_window,
                      lambda x: ctx.queue.put((ctrl.EVENT_KEYPRESS, x))))
    t2.daemon = True
    t2.start()

    ctrl.main_loop(ctx)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='lokatt')
    parser.add_argument('--debug', metavar='path', type=argparse.FileType('a'))
    parser.add_argument('--input', metavar='path', type=argparse.FileType('r'))
    parser.add_argument('--random-delay', metavar='lambda', type=float)
    args = parser.parse_args()

    if args.random_delay is not None:
        if args.random_delay <= 0:
            raise ValueError('lambda must be greater than zero')
        if args.input is None:
            raise ValueError('--random-delay requires --input')

    if args.debug is not None:
        if args.debug.name == '<stdout>':
            raise ValueError('debug: stdout not supported')
        FORMAT = '%(filename)s:%(lineno)d: %(message)s'
        logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename=args.debug.name)
    else:
        logging.basicConfig(level=logging.CRITICAL + 1)

    curses.wrapper(_main, args=args)
