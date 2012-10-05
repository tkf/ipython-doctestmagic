import doctest

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)


class DummyForDoctest(object):
    pass


def common_doctest_arguments(func):
    commons = [
        argument(
            '-v', '--verbose', default=False, action='store_true',
            help='See :func:`doctest.run_docstring_examples`.',
        ),
        argument(
            '-n', '--name', default='NoName',
            help='See :func:`doctest.run_docstring_examples`.',
        )
    ]
    for c in commons:
        func = c(func)
    return func


@magics_class
class DoctestMagic(Magics):

    def _run_docstring_examples(self, obj, args):
        globs = self.shell.user_ns
        doctest.run_docstring_examples(
            obj, globs, verbose=args.verbose, name=args.name)

    @magic_arguments()
    @argument(
        'object', nargs='+',
        help='Doctest is ran against docstrings of this object.',
    )
    @common_doctest_arguments
    @line_magic('doctest')
    def doctest_object(self, line):
        """
        Run doctest of given object.
        """
        args = parse_argstring(self.doctest_object, line)
        objects = map(self.shell.ev, args.object)

        for obj in objects:
            self._run_docstring_examples(obj, args)

    @magic_arguments()
    @common_doctest_arguments
    @cell_magic('doctest')
    def doctest_cell(self, line, cell):
        """
        Run doctest written in a cell.
        """
        args = parse_argstring(self.doctest_cell, line)
        obj = DummyForDoctest()
        obj.__doc__ = cell
        self._run_docstring_examples(obj, args)


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    if not _loaded:
        ip.register_magics(DoctestMagic)
        _loaded = True

_loaded = False
