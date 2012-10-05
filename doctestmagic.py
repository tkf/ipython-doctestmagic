import doctest
from contextlib import contextmanager

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
        verbose = args.verbose
        name = args.name
        optionflags = 0
        globs = self.shell.user_ns
        finder = doctest.DocTestFinder(verbose=verbose, recurse=False)
        runner = doctest.DocTestRunner(verbose=verbose,
                                       optionflags=optionflags)
        for test in finder.find(obj, name, globs=globs):
            runner.run(test, compileflags=None)
            self._test_counter += 1

    @contextmanager
    def _doctest_report(self, num_objects=None):
        self._test_counter = 0
        yield
        if num_objects is None:
            in_objects_message = ''
        else:
            in_objects_message = ' in {0} objects'.format(num_objects)
        print("Ran {0} doctests{1}.".format(
            self._test_counter + 1, in_objects_message))

    @magic_arguments()
    @argument(
        'object', nargs='+',
        help='Doctest is ran against docstrings of this object.',
    )
    @common_doctest_arguments
    @line_magic('doctest')
    def doctest_object(self, line):
        """
        Run doctest of given objects.
        """
        args = parse_argstring(self.doctest_object, line)
        objects = map(self.shell.ev, args.object)

        with self._doctest_report(len(objects)):
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
        with self._doctest_report():
            self._run_docstring_examples(obj, args)


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    if not _loaded:
        ip.register_magics(DoctestMagic)
        _loaded = True

_loaded = False
