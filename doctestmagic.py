import doctest

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)


class DummyForDoctest(object):
    pass


@magics_class
class DoctestMagic(Magics):

    @magic_arguments()
    @argument(
        '-f', '--verbose', default=False, action='store_true',
        help='See :func:`doctest.run_docstring_examples`.',
    )
    @argument(
        '-n', '--name', default='NoName',
        help='See :func:`doctest.run_docstring_examples`.',
    )
    @argument(
        'object', nargs='+',
        help='Doctest is ran against docstrings of this object.',
    )
    @line_magic('doctest')
    def doctest_object(self, line):
        """
        Run doctest of given object.
        """
        args = parse_argstring(self.doctest_object, line)
        globs = self.shell.user_ns
        objects = map(self.shell.ev, args.object)

        for obj in objects:
            doctest.run_docstring_examples(
                obj, globs, verbose=args.verbose)

    @magic_arguments()
    @cell_magic('doctest')
    def doctest_cell(self, line, cell):
        """
        Run doctest written in a cell.
        """
        args = parse_argstring(self.doctest_cell, line)
        globs = self.shell.user_ns
        obj = DummyForDoctest()
        obj.__doc__ = cell
        doctest.run_docstring_examples(
            obj, globs, verbose=args.verbose)
