from threading import Thread
import argparse
import curses
import logging
import sys
import traceback

import adb
import ctrl
import ui


def _log_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            if kwargs['args'].debug:
                logger = logging.getLogger(__name__)
                logger.error(traceback.format_exc())
            else:
                traceback.print_exc()
            sys.exit(1)
    return wrapper


@_log_exception
def _logcat_worker(args, ctx):
    path = None
    if args.input:
        path = args.input.name

    adb.logcat_worker(lambda x: ctx.queue.put((ctrl.EVENT_LOGCAT, x)),
                      path=path, lambd=args.random_delay)


@_log_exception
def _ui_worker(args, ctx):
    ui.input_worker(ctx.root_window, lambda x: ctx.queue.put((ctrl.EVENT_KEYPRESS, x)))


@_log_exception
def _main(window, *_, **kwargs):
    args = kwargs['args']

    ctx = ctrl.create_context(window)

    path = None
    if args.input:
        path = args.input.name
    t1 = Thread(target=_logcat_worker, kwargs={'args': args, 'ctx': ctx})
    t1.daemon = True
    t1.start()

    t2 = Thread(target=_ui_worker, kwargs={'args': args, 'ctx': ctx})
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
