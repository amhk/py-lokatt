class Context:
    pass


def create_context(window):
    ctx = Context()
    ctx.window = window
    return ctx


def main_loop(ctx):
    import sys
    ctx.window.addstr(repr(sys.argv))
    ctx.window.getch()
