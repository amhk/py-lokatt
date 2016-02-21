import argparse
import inspect
import sys


class _CommandArgumentParser(argparse.ArgumentParser):
    def error(self, msg):
        raise ValueError(msg)


class _Command(object):
    def __init__(self, name, desc):
        self.name = name
        self.parser = _CommandArgumentParser(prog=name, description=desc, add_help=False)

    def get_help(self):
        return self.parser.format_help()

    def _execute(self, ctx, args):
        raise NotImplementedError()

    def __call__(self, ctx, argv):
        args = self.parser.parse_args(argv)
        self._execute(ctx, args)


class _GotoLine(_Command):
    def __init__(self):
        _Command.__init__(self, 'goto-line', 'Goto buffer line.')
        self.parser.add_argument('--lineno', type=int, required=True)
        self.parser.add_argument('--anchor', type=str, choices=('top', 'middle', 'bottom'),
                                 required=True)

    def _execute(self, ctx, args):
        ctx.buf.goto_line(args.lineno, args.anchor)


class _Quit(_Command):
    def __init__(self):
        _Command.__init__(self, 'quit', 'Quit program execution.')

    def _execute(self, ctx, args):
        ctx.done = True


class _Error(_Command):
    def __init__(self):
        _Command.__init__(self, 'error', 'Display an error message.')
        self.parser.add_argument('words', metavar='string', type=str, nargs='+')

    def _execute(self, ctx, args):
        raise Exception(' '.join(args.words))


def _create_commands():
    def is_command_subclass(x):
        if not inspect.isclass(x):
            return False
        bases = [b.__name__ for b in inspect.getmro(x)]
        if '_Command' not in bases:
            return False
        if '_Command' == bases[0]:
            return False
        return True

    out = dict()
    mod = sys.modules[__name__]
    for _, cls in inspect.getmembers(mod, is_command_subclass):
        obj = cls()
        name = obj.name
        out[name] = obj
    return out


COMMANDS = _create_commands()


def get_command(name):
    return COMMANDS.get(name)
