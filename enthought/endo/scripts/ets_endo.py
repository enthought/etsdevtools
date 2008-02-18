""" This script finds subdirectories of the current working directory that
contain component packages, infers the package name and subdirectory structure,
and runs endo.py, passing all the package info that it found, along with any
arguments passed to it on the command line.

It assumes that the directories follow the naming and structure conventions of
the "enthought" repository, and therefore may not be appropriate for other
repositories.

Specifically, it assumes that the directories are structured as follows::

    Project_M.m/
        setup.py
        pkg/
            __init__.py
            subpkg/
                __init__.py
                
There may be multiple pkg directories under a project directory (though in the
Enthought repository, there is usually only one, named 'enthought'), and there
may be multiple subpkg directories under a project directory.
"""
import optparse
import os
import subprocess
import sys

from setuptools import find_packages

from enthought.svn.checkouts import Checkouts
from endo import add_endo_options

ENDO = "endo.py"

def get_component_dirs():
    result = []
    for file in os.listdir('.'):
        if os.path.isdir(file):
            if os.path.exists(os.path.join(file, 'setup.py')):
                result.append(file)
    return result


def main():
    """ Entry point for the installed script.
    """
    ropts = []
    # Parse the user's command line
    parser = optparse.OptionParser(
        version = '0.1',
        description = ('Runs endo on all SVN checkouts within a directory.'
            'If no path is explicitly specified, then the current directory '
            'is treated as the root of the checkouts to be documented.'),
        usage = '%prog [endo_options] [path]'
        )
    add_endo_options(parser)
    options, args = parser.parse_args()
    if len(args) < 1:
        path = [os.getcwd()]
    else:
        path = [args[-1]]
        
    checkouts = Checkouts(path, verbose=options.verbose)
    
    for checkout in checkouts.checkouts:
        pkgs = find_packages(checkout)
        for pkg in pkgs:
            pdir = os.path.join(checkout, pkg.replace('.', '/'))
            ropts.append('-r%s=%s' % (pkg, pdir))

    # FIXME: Hack that puts the traits packages in the desired order
    ropts.sort(reverse=True)

    loc = os.path.dirname(os.path.abspath(__file__))
    endo_args = [ sys.executable, os.path.join(loc, ENDO)] + sys.argv[1:] + ropts
    ret = subprocess.call(endo_args)

if __name__ == "__main__":
    main()

