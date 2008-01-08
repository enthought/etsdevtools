""" This script finds subdirectories of the current working directory that
contain component packages, infers the package name and subdirectory structure,
and runs endo.py, passing all the package info that it found, along with any
arguments passed to it on the command line.

It assumes that the directories follow the naming and structure conventions of
the "enthought" repository, and therefore may not be appropriate for other
repositories.

Specifically, it assumes that the directories are structured as follows::

    pkg.subpkg_M.m/
        setup.py
        pkg/
            subpkg/
                __init__.py
"""

import os
import re
import subprocess
import sys

ENDO = "endo.py"

def get_component_dirs():
    result = []
    for file in os.listdir('.'):
        if os.path.isdir(file):
            if os.path.exists(os.path.join(file, 'setup.py')):
                result.append(file)
    return result


def main():
    cdirs = get_component_dirs()
    ropts = []
    patt = re.compile('^((\w+\.*)+)_(\d+\.\d+)')
    for dirname in cdirs:
        match = re.match(patt, dirname)
        if match is not None:
            base = match.group(1)
        else:
            base = dirname
        path = base.split('.')
        fullpath = dirname
        for sub in path:
            fullpath = os.path.join(fullpath, sub)
        option = "-r"+base+"="+fullpath
        ropts.append(option)

    # FIXME: Hack that puts the traits packages in the desired order
    ropts.sort(reverse=True)

    loc = os.path.dirname(os.path.abspath(__file__))
    endo_args = [ sys.executable, os.path.join(loc, ENDO)] + sys.argv[1:] + ropts
    ret = subprocess.call(endo_args)


if __name__ == "__main__":
    main()

