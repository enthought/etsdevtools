###########################################################################
# File:    endo
# Project: endo
# Date:    2005-06-08
# Author:  David Baer
#
# Description:
#  Creates documentation from Python source
#
###########################################################################

import compiler
import compiler.ast
import compiler.visitor
import sys
import re
import os

import gzip
import cPickle as pickle

import warnings

from cStringIO import StringIO

from tokenize import generate_tokens, COMMENT, NEWLINE, INDENT
from traceback import print_exception

try:
    from enthought.etsconfig.api import ETSConfig
except:
    from enthought.traits.trait_base import ETSConfig
ETSConfig.toolkit = 'null'
    
import enthought.endo as endo
import enthought.endo.docobjects as docobjects
import enthought.endo.docerror as docerror
from enthought.endo.namespace import Namespace
from enthought.endo.output import OutputHTML
from enthought.endo.util import alpha_sort

from optparse import OptionParser, OptionGroup
from glob import glob


moddir = os.path.abspath(os.path.dirname(endo.__file__))
sys.path.append(moddir)
OutputHTML.DATA_PATH = os.path.join(moddir, 'data')

_INDENT = re.compile('^[ \t]*')
_COMMENT = re.compile('^# ?')

def _grab_comment(source_lines, assign_line):
    # look for indentation on assignment line
    i = assign_line
    indent_string = _INDENT.search(source_lines[i]).group()
    i -= 1

    # match indentation on comment lines
    l = len(indent_string)
    while i > 0 and \
       len(source_lines[i]) > l and \
       source_lines[i][:l] == indent_string and \
       source_lines[i][l] not in [ ' ', '\t' ] and \
       source_lines[i].strip() != '' and \
       source_lines[i].strip()[0] == '#':
        i -= 1

    start, end = i + 1, assign_line
    result = source_lines[start:end]
    result = [ _COMMENT.sub('', x.replace(indent_string, '', 1)) for x in result ]

    return ''.join([ x + '\n' for x in result ])

def _balanced_parens(txt):
    # quick and dirty heuristic to test for open parens
    stack = [ ]
    match = { '(' : ')', '{' : '}', '[' : ']' }
    for ch in list(txt):
        if ch in match.keys():
            stack.append(ch)
        elif ch in match.values():
            if len(stack) == 0:
                raise ValueError, "unmatched delimiter '%s'" % ch
            elif ch == match[stack[-1]]:
                stack = stack[:-1]
            else:
                raise ValueError, "mismatched delimiters '%s' '%s'" % (stack[-1], ch)
    if len(stack) == 0:
        return True
    else:
        return False

def _grab_assignment_rhs(source_lines, assign_line):
    input_source = StringIO(''.join([x + '\n' for x in source_lines[assign_line:]]))
    result_line = ''
    tok_count = 0
#    warnings.filterwarnings('ignore')
    for tok in generate_tokens(input_source.readline):
        tok_type, tok_string, tok_start, tok_end, tok_line = tok
        if tok_type == NEWLINE:
            break
        if tok_type == INDENT:
            # don't count (or save) indents
            continue
        tok_count += 1
        srow, scol = tok_start
        erow, ecol = tok_end
        if tok_type != COMMENT and tok_count > 2:
            # throw out comments, as well as leading ID, '='
            result_line += tok_line[scol:ecol]
#    warnings.resetwarnings()
    return result_line

def scan_file(options, filename, module_name):
    """
    return module document object for the given file
    """
    f = open(filename, 'rt')
    text = f.read()
    f.close()

    # buffer with dummy line to make line count accurate,
    code_lines = [ '(dummy)' ] + text.split('\n')

    # try parsing file
    att = 0
    while att < 2:
        att += 1
        try:
#            warnings.filterwarnings('ignore')
            ast = compiler.parseFile(filename)
#            warnings.resetwarnings()
            break
        except SyntaxError, exc:
            # for some reason, some modules need a CR added...
            if att < 2:
                text = text + '\n'
            else:
                sys.stderr.write("Syntax error %s:%d:%d: %s.\n" %
                                 (filename, exc.lineno, exc.offset, exc.text))
                return None

    f.close()

    result = docobjects.Module.fromAST(options, module_name, filename, ast)

    # find all attribute assignments
    attr_assigns = result.get_descendants(node_type = docobjects.Attribute)
    for attr in attr_assigns:
        # fill in docstrings with source comments!
        attr.docstring = _grab_comment(code_lines, attr.lineno)
        attr.rhs_text = _grab_assignment_rhs(code_lines, attr.lineno)

    return result

def search_tree(path):
    """ search python package tree """
    result = [ ]
    stack = [ path ]
    while len(stack) > 0:
        top = stack.pop()
        if os.access(os.path.join(top, '__init__.py'), os.R_OK):
            # __init__.py exists -- dir is a package
            result.extend(glob(os.path.join(top, '*.py')))

            # check sub directories
            dirs = [ os.path.join(top, d) for d in os.listdir(top)
                                          if os.path.isdir(os.path.join(top, d)) ]

            stack.extend(dirs)

    return result

def filename_to_module_name(root_dir, package_name, path):
    """ convert file name to module name """
    # normalize path to remove ., ..
    if package_name:
        module_name = os.path.normpath(path)
        root_dir = os.path.normpath(root_dir)
        module_name = module_name.replace(root_dir + os.path.sep, '')
    else:
        module_name = os.path.basename(path)
        root_dir = os.path.normpath(os.path.dirname(path))

    # remove trailing .py
    if module_name[-3:] == '.py': module_name = module_name[:-3]

    # replace path separators with .'s
    path_tuple = module_name.split(os.path.sep)
    #if path_tuple[0] == '':
    #    # this is caused by a leading /
    #    path_tuple = path_tuple[1:]
    if path_tuple[-1] == '__init__':
        path_tuple = path_tuple[:-1]
    module_name = '.'.join(path_tuple)

    if package_name:
        if module_name:
            module_name = package_name + '.' + module_name
        else:
            module_name = package_name

    if module_name == '':
        module_name = os.path.basename(root_dir)


    return module_name

def create_output_dir(dirname):
    if os.path.isdir(dirname) and os.access(dirname, os.W_OK):
        return
    else:
        try:
            os.mkdir(dirname)
        except:
            raise docerror.DocWriteError, "couldn't create output directory '%s'" % dirname

def read_header_footer_files(options):
    # read header file if any
    if options.header_filename is not None:
        f = open(options.header_filename, 'rt')
        options.header = f.read()
        f.close()

    # read footer file if any
    if options.footer_filename is not None:
        f = open(options.footer_filename, 'rt')
        options.footer = f.read()
        f.close()

def write_state(state, filename):
    f = gzip.GzipFile(filename=filename, mode='wb')
    pickle.dump(state, f)
    f.close()

def add_module_names(filename_list):
    result = [ ]

    for package, package_root, filenames in filename_list:
        fn = [ ]
        for filename in filenames:
            module_name = filename_to_module_name(package_root, package, filename)
            fn.append((module_name, filename))
        alpha_sort(fn)
        result.append((package, package_root, [ (x[0], x[1]) for x in fn ]))

    return result


def add_endo_options(option_parser):
    group = OptionGroup(option_parser, "Input options",
                        "Specify what you want to document")
    group.add_option("-r", "--package", dest="package_list", action="append",
                     metavar="[NAME=]PATH", default=[],
                     help="document package located at PATH (with dotted name NAME)")

    group.add_option("-p", "--package-name", dest="package", metavar="NAME",
                     help="default package name", default="")
    group.add_option("--rst", dest="rst", action="store_true",
                             default=False,
                             help="interpret docstrings as ReStructured Text")
    group.add_option("--include-protected", dest="include_protected",
                             action="store_true", default=False,
                             help="include protected methods/functions in documentation")
    option_parser.add_option_group(group)

    group = OptionGroup(option_parser, "Output options", "")

    group.add_option("-d", "--document-dir", dest="docdir",
                             metavar="DIR", help="write documentation here",
                             default="doc")

    option_parser.add_option_group(group)

    group = OptionGroup(option_parser, "Customization options",
                        "Customize the generated documentation")
    group.add_option("--css", dest="additional_stylesheets",
                     metavar="FILE", action="append", help="add CSS stylesheet",
                     default=[ ])
    group.add_option("--override-templates",
                     dest="additional_templates",
                     default=[], action="append",
                     metavar="DIR",
                     help="check this directory first for templates (revert to default if not found)")
    group.add_option("--data", dest="data_files",
                     metavar="FILE",
                     action="append",
                     help="additional data files to copy",
                     default=[ ])
    group.add_option("--header-file", dest="header_filename",
                     metavar="FILE",
                     help="file containing HTML text to use as header",
                     default=None)
    group.add_option("--header", dest="header",
                     metavar="STRING",
                     help="HTML text to use as a header",
                     default="")
    group.add_option("--footer-file", dest="footer_filename",
                     metavar="FILE",
                     help="file containing HTML text to use as a footer",
                     default=None)
    group.add_option("--footer", dest="footer",
                     metavar="STRING",
                     help="HTML text to use as a footer",
                     default="")

    option_parser.add_option_group(group)

    option_parser.add_option("--debug", dest="debug",
                             action="store_true", default=False,
                             help="turn on debugging messages")
    option_parser.add_option("-s", "--silent", dest="silent",
                            action="store_true", default=False,
                            help="ignores all warnings")
    option_parser.add_option("--verbose", dest="verbose",
                             action="store_true", default=False,
                             help="show detailed status messages")
    option_parser.add_option("--dump-state", dest="state_file",
                             metavar="FILE", default=None,
                             help="dump parser state to file and quit")


def main():
    quit_now = False
    option_parser = OptionParser(usage = """
%prog [options] [-r [package_name=path/to/package]]*
                  [[module_prefix=]path/to/module.py]*""")
    #option_parser.add_option("-r", "--recursive", dest="recursive",
    #                         help="walk a directory recursively",
    #                         action="store_true", default=False)
    
    add_endo_options(option_parser)
    (options, args) = option_parser.parse_args()

    read_header_footer_files(options)

    if options.rst and not OutputHTML.HAS_DOCUTILS:
        option_parser.error("Option --rst specified, but docutils not found in default import path.\n")

    if len(args) < 1 and len(options.package_list) < 1:
        option_parser.error("Please specify at least one module or one package (with -r)")

    filename_list = [ ]

    # add package files
    for package_arg in options.package_list:
        if package_arg.find('=') != -1:
            package_name, package_dir = package_arg.split('=')
        else:
            # obtain package name from directory
            package_dir = package_arg
            package_name = os.path.split(os.path.normpath(package_dir))[-1]
        package_dir_list = [ (package_name, x) for x in glob(package_dir) ]
        alpha_sort(package_dir_list)
        new_files = [ (package_name, package_dir, search_tree(package_dir))
                      for package_name, package_dir in package_dir_list ]
        [ alpha_sort(entry[2]) for entry in new_files ]
        filename_list.extend(new_files)

    # add additional modules
    for module_arg in args:
        if module_arg.find('=') != -1:
            module_prefix, module_file = module_arg.split('=')
        else:
            module_prefix = options.package
            module_file = module_arg
        module_file_list = [ (module_prefix, x) for x in glob(module_file) ]
        alpha_sort(module_file_list)
        new_files = [ (module_prefix, os.path.dirname(f), [ f ])
                      for module_prefix, f in module_file_list ]
        alpha_sort(new_files)
        filename_list.extend(new_files)

    # create output dir if it doesn't exist
    create_output_dir(options.docdir)

    # set package name if it doesn't exist
    if not(options.package):
        options.package = ', '.join([ package_name
                                      for package_name,
                                          package_root,
                                          filenames
                                      in filename_list ])

    filename_list = add_module_names(filename_list)

    backend = OutputHTML(options)
    exceptions = [ ]
    scanned = {}
    for package, package_root, filenames in filename_list:
        for mod_name, filename in filenames:
            try:
                if str(mod_name) not in scanned: # Avoid duplicates
                    if options.verbose:
                        sys.stdout.write("Scanning %s ... " % filename)
                        sys.stdout.flush()
                    module_obj = scan_file(options, filename, mod_name)
                    scanned[mod_name] = filename
                    if module_obj is not None:
                        backend.add_module(module_obj)
                    if options.verbose:
                        sys.stdout.write("ok.\n")
            except KeyboardInterrupt:
                sys.stdout.write("interrupted!  Exiting...\n")
                quit_now = True
                break
            except:
                # save exception info and move on
                exc_info = sys.exc_info()
                exceptions.append((filename, exc_info))

                if options.verbose:
                    sys.stdout.write("error, moving on.\n")

        if quit_now:
            break

    if (options.silent):
        warnings.filterwarnings("ignore")

    # set the docobjects warning var to be the module imported here
    # so they can share the same warnings filters
    docobjects.warnings = warnings

    if options.state_file is not None:
        write_state(backend, options.state_file)
    elif not quit_now:
        # resolve intra-package imports
        backend.write_output()

    # print all exceptions that were raised while reading sources
    if len(exceptions) > 0:
        sys.stderr.write("The following exceptions were encountered while processing the source files:\n\n")

        for filename, exc_info in exceptions:
            exc_type, exc_value, exc_traceback = exc_info
            sys.stderr.write("%s\n%s\n" % (filename, '-' * len(filename)))
            print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
            sys.stderr.write("\n")



if __name__ == "__main__":
    main()

