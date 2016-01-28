from Queue import PriorityQueue
import curses


EVENT_COMMAND = 10
EVENT_KEYPRESS = 20
EVENT_LOGCAT = 30


class Context:
    pass


def create_context(window):
    ctx = Context()
    ctx.queue = PriorityQueue()
    ctx.window = window
    ctx.done = False
    return ctx


def main_loop(ctx):
    while not ctx.done:
        type_, data = ctx.queue.get()
        y, _ = curses.getsyx()
        maxy, _ = ctx.window.getmaxyx()

        if y > maxy - 2:
            ctx.window.erase()
            ctx.window.move(0, 0)

        ctx.window.addstr('type={} data={}\n'.format(type_, repr(data)))
        ctx.window.refresh()

        if type_ == EVENT_KEYPRESS and data == ord('q'):
            ctx.done = True
