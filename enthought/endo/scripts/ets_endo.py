""" 
Copyright 2008 Enthought, Inc.
License: BSD Style

This script figures out appropriate subdirectories of a specified or
working directory to document, infers the structure of package names and 
subdirectories, and runs endo.py, passing all the package info that it found, 
along with any endo arguments passed to it on the command line.

By default, the script simply finds subdirectories of the specified
directory that contain packages, as evidenced by an __init__.py file, and
documents those. You can use the --project (or -j) option to specify a directory
as containing a setuptools-based project; in that case, the script documents
only those packages specified by the setup.py for that project. 

If you use the --project/-j option, the name and version number of the
specified project(s) are inserted into the header of the output, using
endo's --header option. However, explicitly using the --header or
--header_filename option replaces any header created by this feature.

The script assumes that the directories follow the naming and structure 
conventions of the "enthought" repository, and therefore may not be appropriate
for other repositories.

Specifically, it assumes that the project directories are structured as follows::

    Project_M.m/
        setup.py
        pkg/
            __init__.py
            subpkg/
                __init__.py
                
There may be multiple *pkg* directories under a project directory (though in the
Enthought repository, there is usually only one, named 'enthought'), and there
may be multiple *subpkg* directories under a project directory.
"""
import optparse
import os
import StringIO
import subprocess
import sys

from endo import add_endo_options

class ETSEndoException(Exception): pass

ENDO = "endo.py"

header_template = "--header=<p>API Documentation set for: %s</p>"

def _get_package_dirs(apath):
    result = [ ]
    stack = [ apath ]
    while len(stack) > 0:
        top = stack.pop()
        if os.access(os.path.join(top, '__init__.py'), os.R_OK):
            # __init__.py exists -- dir is a package
            result.append(top)

        # check sub directories
        dirs = [ os.path.join(top, d) for d in os.listdir(top) 
                 if os.path.isdir(os.path.join(top, d)) ]
        stack.extend(dirs)
    return result

def _get_project_packages(apath):
    # Based on enthought.svn.project_set.ProjectSet._get_project_info_from_svn()
    packages = []
    setup_file = os.path.join(apath, 'setup.py')
    if not os.path.exists(setup_file):
        raise ETSEndoException('No setup.py was found in specified project directory: %s' % apath)
    elif not os.access(setup_file, os.R_OK):
        raise ETSEndoException('Reading of setup.py is not permitted in project directory: %s' % apath)
    else:
        try:
            f = open(setup_file, 'r')
            setup = f.read()
            f.close()
        except Exception, e:
            raise ETSEndoException('An error occurred while reading %s.\n The exception was: %s' % (setup_file, str(e)))
        
        try:
            kwds = _safe_setup_execution(setup)
        except Exception, e:
            raise ETSEndoException('Unable to parse %s.\ The exception was: %s' % (setup_file, str(e)))
        
        if 'namespace_packages' in kwds:
            packages.extend(kwds['namespace_packages'])
        if 'packages' in kwds:
            packages.extend(kwds['packages'])
            
    return packages

def _safe_setup_execution(setup):
    # Based on enthought.svn.project_set.ProjectSet._safe_setup_execution()
    """
    Safely execute a setup.py to return project info.

    Raise an ``Exception`` if execution fails.

    """

    # Temporarily replace setuptools' and distutils' setup method with
    # a version that just records the keyword arguments.
    class Keywords(object):
        keywords = {}
    k = Keywords()
    def my_setup(**kws):
        k.keywords = kws
    import setuptools
    old_setuptools_setup = setuptools.setup
    setuptools.setup = my_setup
    try:
        import numpy.distutils.core
        old_numpy_distutils_setup = numpy.distutils.core.setup
        numpy.distutils.core.setup = my_setup
    except Exception:
        old_numpy_distutils_setup = None

    # Redirect stdout and stderr to prevent output from showing up at the
    # console
    buffer = StringIO.StringIO()
    sys.stdout = sys.stderr = buffer

    # Parse the setup.py.  If an exception happens while running
    # the full version, try running it when it is not the main file.
    try:
        try:
            scope = {'__file__':'setup.py', '__name__':'__main__'}
            exec setup in scope
            print "Fully executed setup.py"
        except:
            scope = {'__file__':'setup.py'}
            exec setup in scope
            print "Executed setup.py but not as __main__"
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        setuptools.setup = old_setuptools_setup
        if old_numpy_distutils_setup is not None:
            numpy.distutils.core.setup = old_numpy_distutils_setup

    # Retrieve whatever project information we can get from the setup.py
    if len(k.keywords) > 0:
        info = k.keywords.copy()
    else:
        info = {}

    return info
    
    
def main():
    """ Entry point for the installed script.
    """
    ropts = []
    header = ""
    # Parse the user's command line
    parser = optparse.OptionParser(
        version = '0.1',
        description = ('Runs endo on packages within a directory.'
            'If no path is explicitly specified, then the current directory '
            'is treated as the root of the tree to be documented.'),
        usage = '%prog [endo_options] [path]'
        )
    add_endo_options(parser)
    group = optparse.OptionGroup(parser, "%prog-specific Options", "Not passed through to endo")
    group.add_option("-j", "--project", dest="project_list", action="append",
                     metavar="PATH", default=[], 
                     help="Root of Setuptools-based project located at PATH")
    parser.add_option_group(group)
    options, args = parser.parse_args()
    if len(args) < 1:
        runpath = os.getcwd()
    else:
        runpath = os.path.abspath(args[-1])
        
    if options.project_list != []:
        packages = []
        for proj in options.project_list:
            if options.verbose:
                sys.stdout.write("Looking for packages in project %s.\n" % proj)
            if not os.path.isabs(proj):
                proj = os.path.join(runpath, proj)
            try:
                packages = _get_project_packages(proj)
            except Exception, e:
                print str(e)
            for pkg in packages:
                ropts.append('-r%s=%s' % (pkg, os.path.join(runpath, proj, pkg.replace('.', os.sep))))

        if (not options.header) and (not options.header_filename):
            header = header_template % ', '.join(proj.replace("_", " ") for proj in options.project_list)
    else:
        ropts.extend( ['=r%s' % pdir for pdir in _get_package_dirs(runpath) ] )
        
    #ropts.sort(reverse=True) # FIXME: Hack that puts the traits packages in the desired order
    
    endo_args = []
    skip = False
    for arg in sys.argv[1:]: # Remove options endo doesn't understand
        if (arg == '-j') or (arg == '--project'):
            skip = True
            continue
        elif arg.startswith('-j') or arg.startswith('--project'):
            continue
        if not skip:
            endo_args.append(arg)
        else:
            skip = False

    loc = os.path.dirname(os.path.abspath(__file__))
    endo_cmd = [ sys.executable, os.path.join(loc, ENDO)] + endo_args + ropts + [header]
    if options.verbose:
        sys.stdout.write("Calling: %s\n" % endo_cmd)
    ret = subprocess.call(endo_cmd)

if __name__ == "__main__":
    main()

