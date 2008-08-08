
###########################################################################
# File:    html.py
# Project: docutils
# Date:    2005-07-11
# Author:  David Baer
# 
# Description:
#  HTML output backend
# 
###########################################################################

"""HTML output backend

usage:

   >>> output = OutputHTML(parsed_options)     # parsed_options from cmd line
"""

import os
import re
import sys
import shutil
import warnings

# local imports
from enthought.endo.util import alpha_sort

sys.path.append('..')

### Information about objects to document
import enthought.endo.docobjects as docobjects

### Template engine for HTML output
from enthought.endo.template import TemplateLoader

### Needed for formatting exceptions in a pretty way
from traceback import print_exception

### Basic output architecture -- extended here for HTML
from base import OutputBase, FormattingException

### Useful utility functions for generating documentation
from tools import unparse, object_link, class_link, \
     hierarchicalize_modules, format_params, fix_indent, encode_entities

### Try to import docutils -- needed for processing RST
try:
    from docutils.core import publish_parts, publish_programmatically
    from docutils.utils import SystemMessage
    _HAS_DOCUTILS = True
except ImportError:
    _HAS_DOCUTILS = False

# Regular expression for matching HTML paragraph tags.
_match_para_contents = re.compile(r'<p.*?>(.*)</p>', re.DOTALL)

class OutputHTML(OutputBase):
    "HTML output backend"

    DATA_PATH = '/usr/share/enthought/endo'
    HAS_DOCUTILS = _HAS_DOCUTILS

    def __init__(self, options):
        """Constructor

          * options is the parsed set of command-line options
        """
        OutputBase.__init__(self, options)
        self.template_loader = TemplateLoader(self.options.additional_templates + [ self.DATA_PATH ])
        self.exceptions = [ ]
        self.rst_errors = [ ]
        
    def _downgrade_headers(html_body):
        h = html_body

        h = h.replace('<h3', '<h5').replace('</h3', '</h5')
        h = h.replace('<h2', '<h4').replace('</h2', '</h4')
        h = h.replace('<h1', '<h3').replace('</h1', '</h3')

        return h

    _downgrade_headers = staticmethod(_downgrade_headers)

    def _para_body(self, html_body, index=0):
        """Extracts the contents of a paragraph tag pair.
        
        The *index* parameter determines which paragraph tag pair in 
        *html_body* has its contents extracted.
        
        Returns **None** if *html_body* contains no paragraph tags.
        """
        p_list = re.findall(_match_para_contents, html_body)
        if (len(p_list) > index):
            return p_list[index]
        else:
            return None
            
            
    def _format_docstring(self, context, docstring):
        """format docstring according to user options

           * context is a docobjects.DocObject instance associated with
             docstring
           * docstring is the string to format
        """
        options = self.options
        
        if options.debug:
            print "Formatting docstring for",context.abs_name
        if options.rst:
            # restructured text -- need to interpret
            overrides = { 'input_encoding' : 'ascii',
                          'output_encoding' : 'utf-8',
                          'report_level' : 10,
                          'halt_level' : 1,
                          'traceback' : True }
            docstring = fix_indent(docstring)
            try:
                if isinstance(context, docobjects.Module):
                    source_path = ("%s.__doc__ (in %s)" %
                                   (context.name, context.file))
                else:
                    source_path = ("%s (@ %s:line#%d)" %
                                   (context.file, context.name, context.lineno))

                docstring_parts = publish_parts(docstring,
                    source_path=source_path,
                    writer_name='html4css1',
                    settings_overrides=overrides,
                    enable_exit_status=True)

                html_body = docstring_parts['html_body']

                html_body = self._downgrade_headers(html_body)
                
                return html_body
            except KeyboardInterrupt, exc:
                raise exc
            except SystemMessage, exc:
                warnings.warn("failed to interpret %s docstring as RST -- falling back to plain text\n" % context.abs_name)
                exc_info = sys.exc_info()
                if isinstance(context, docobjects.Module):
                    mod_name = context.abs_name
                else:
                    mod_name = context.parent_module.abs_name
                self.rst_errors.append((mod_name, exc_info))
            except:
                warnings.warn("failed to interpret %s docstring as RST -- falling back to plain text\n" % context.abs_name)
                exc_info = sys.exc_info()
                if isinstance(context, docobjects.Module):
                    mod_name = context.abs_name
                else:
                    mod_name = context.parent_module.abs_name
                self.exceptions.append((mod_name, exc_info))

        # just format as text (also fallback in case of exception in rst formatting)
        return '<pre>%s</pre>' % encode_entities(docstring)
        
    def _format_name_links(n, package_namespace):
        "split name n into name components and link each one"
        name_parts = n.split('.')
        disp_parts = [ ]
        for i in range(0, len(name_parts)):
            partial = '.'.join(name_parts[:i+1])
            if package_namespace.resolve(partial) is not None:
                disp_parts.append('<a href="%s.html">%s</a>' % (partial,
                                                                name_parts[i]))
            else:
                disp_parts.append(name_parts[i])
        return '<span class="prefix">' + \
               ''.join([ d + '.&#8203;' for d in disp_parts[:-1] ]) + \
               '</span>' + \
               disp_parts[-1]
    _format_name_links = staticmethod(_format_name_links)

    def get_extra_style(self):
        "returns the list of additional stylesheet files specified by user"
        options = self.options
        # Templating code expects this list to be a list of tuples
        style_files = [ (os.path.basename(f),)
                        for f in options.additional_stylesheets ]
        return style_files

    def copy_data_files(self):
        "copy style, image, and script support files to output directory"
        options = self.options
        output_dir = options.docdir
        file_list = [ os.path.join(self.DATA_PATH, f) for f in
                      [ 'default.css', 'module.css', 'class.css',
                        'plus.png', 'minus.png', 'scr.js' ]
                    ]

        file_list += options.additional_stylesheets + options.data_files

        for src in file_list:
            dest = os.path.join(output_dir, os.path.basename(src))
            shutil.copyfile(src, dest)

    def write(self, obj):
        """Write HTML documentation

          * obj is a docobjects.DocObject instance to be documented
            (must be either Module or Class)

        This method produces a file PACKAGE.NAME.MODULE.NAME.html
        for modules, and PACKAGE.NAME.MODULE.NAME.CLASS.html for classes
        """
        output_dir = self.options.docdir
        customheader = self.options.header
        customfooter = self.options.footer
        normative_obj_name = obj.abs_name
        package_namespace = self.package_namespace
        extrastyle = self.get_extra_style()

        disp_name = self._format_name_links(normative_obj_name, package_namespace)
        docstring = self._format_docstring(obj, obj.docstring)

        if isinstance(obj, docobjects.Module):
            # open output file
            fn = "%s.html" % normative_obj_name
            of = open(os.path.join(output_dir, fn), 'wt')

            # prepare arguments particular to modules
            title = "Module %s" % normative_obj_name
            header_title = "Module %s" % disp_name
            stylesheet = "module.css"
            template_name = 'module'
            obj.sort_sub_modules()
            sub_modules = [ (x.name, 
                             object_link(x), 
                             self._para_body(
                                 self._format_docstring(x, 
                                     re.split('\.[ (\\n)]', 
                                         x.docstring.strip())[0])))
                            for x in obj.sub_modules if not x.is_package() ]
            sub_packages = [ (x.name, object_link(x), x.docstring.strip().split('\n')[0])
                             for x in obj.sub_modules if x.is_package() ]
            imported_objects = [ (name, imp_obj.abs_name, object_link(imp_obj))
                                 for name, imp_obj in
                                 obj.get_imported_objects() ]
                
        elif isinstance(obj, docobjects.Class):
            # open output file
            fn = "%s.html" % normative_obj_name
            of = open(os.path.join(output_dir, fn), 'wt')

            # prepare arguments particular to classes
            title = "Class %s" % normative_obj_name
            header_title = "Class %s" % disp_name
            stylesheet = "class.css"
            template_name = 'class'
            superclasses = [ (x.name, object_link(x), x.abs_name)
                             for x in obj.get_bases() ]

            inh_attr_children, inh_class_children, inh_func_children, \
                inh_traits_children = obj.inherited_children()

            inh_variables = [ (a.name, object_link(a))
                              for a in inh_attr_children ]
            inh_classes = [ (c.name, object_link(c))
                            for c in inh_class_children ]
            inh_functions = [ (f.name, format_params(f.argnames, f.defaults, f),
                               object_link(f))
                              for f in inh_func_children ]
            inh_traits = [ (t.name, object_link(t))
                           for t in inh_traits_children ]

        # load html template
        template = self.template_loader.load(template_name)

        # this will hold our table of contents for use at the top of the page
        contents = [ ]

        # split children so that they can be linked to in appropriate sections
        attr_children, class_children, func_children, traits_children = \
                       obj.divide_children()

        # prepare template arguments
        variables = [ (a.name, self._format_docstring(a, a.docstring),
                       '<pre>%s = %s\n\n</pre>' %
                       (a.name, unparse(a.rhs_expr, a, False)))
                      for a in attr_children ]
        classes = [ (c.name, 
                     object_link(c), 
                     self._para_body(
                         self._format_docstring(c, 
                             re.split('\.[ (\\n)]', 
                                 c.docstring.strip())[0])))
                    for c in class_children ]
        functions = [ (f.name, format_params(f.argnames, f.defaults, f),
                       self._format_docstring(f, f.docstring))
                      for f in func_children ]
        traits = [ (t.name, self._format_docstring(t, t.docstring),
                    '<pre>%s = %s\n\n</pre>' %
                    (t.name, unparse(t.rhs_expr, t, True)))
                   for t in traits_children ]

        # render template with local variables as arguments and write
        of.write(template.render(vars()))
        of.close()

        # recurse through class objects below this object
        for child in class_children:
            self.write(child)

    def write_index(self):
        """Write hierarchical module index

        Generates index.html in output directory
        """
        output_dir = self.options.docdir
        customheader = self.options.header
        customfooter = self.options.footer
        module_list = self.modules
        package_name = self.package_namespace.name
        extrastyle = self.get_extra_style()

        header_title = "Module Index"
        title = "%s -- %s" % (package_name, header_title)
        stylesheet = "default.css"

        of = open(os.path.join(output_dir, 'index.html'), 'wt')

        # load module index HTML template
        template = self.template_loader.load('module_index')

        # prepare hierarchy of packages, modules
        mods_with_names = [(m.abs_name.lower(), m) for m in module_list]
        mods_with_names.sort()
        
        modules_sorted = [ m[1] for m in mods_with_names ]
        packages_sorted = [ m[1] for m in mods_with_names if m[1].is_package() ]
        
        module_hierarchy = self._add_links(hierarchicalize_modules(modules_sorted))
        package_hierarchy = self._add_links(hierarchicalize_modules(packages_sorted))
            
        # generate an overall docstring by concatenating the docstrings for
        # top-level packages (usually there will be only one)
        docstring = "\n".join([ self._format_docstring(m, m.docstring) for m, l, s in package_hierarchy ])

        # render template with local variables as arguments and write to disk
        of.write(template.render(vars()))
        of.close()
        
    def _find_classes(module_list):
        "find all classes at top level of modules"
        return reduce(lambda x, y: x + y, [ m.divide_children()[1] for m in module_list ])
    _find_classes = staticmethod(_find_classes)

    def write_class_index(self):
        """Generate alphabetical index of classes

        Generates class_index.html in output directory
        """
        output_dir = self.options.docdir
        customheader = self.options.header
        customfooter = self.options.footer
        module_list = self.modules
        package_name = self.package_namespace.name
        extrastyle = self.get_extra_style()

        class_list = self._find_classes(module_list)
        header_title = "Class Index"
        title = "%s -- %s" % (package_name, header_title)
        stylesheet = "default.css"

        of = open(os.path.join(output_dir, 'class_index.html'), 'wt')

        # load class index HTML template
        template = self.template_loader.load('alpha_list')

        alpha_sort(class_list)

        # group class objects by first letter of local name
        classes_grouped = { }
        for c in class_list:
            letter = c.name[0].upper()
            link = class_link(c)
            display_name = c.name
            text = "%s" % c.abs_name

            classes_grouped[letter] = classes_grouped.get(letter, [ ]) + [ (display_name, link, text) ]

        # list of available first letters (for links at top of index)
        letter_list = classes_grouped.keys()
        letter_list.sort()
        
        # sort by class name within letter categories
        for letter in letter_list:
            alpha_sort(classes_grouped[letter])

        objects = classes_grouped
        
        # render template with local variables as arguments and write to disk
        of.write(template.render(vars()))

        of.close()

    def _find_variables_and_functions(module_list):
        "find all top-level variables, functions, and traits"
        obj_list = [ ]
        for m in module_list:
            temp = m.divide_children()
            children = [ (c.name.upper(), c.abs_name.upper(), c) for c in temp[0] + temp[2] + temp[3] ]
            obj_list.extend(children)

        # sort alphabetically by local name
        alpha_sort(obj_list)
        obj_list = [ r[2] for r in obj_list ]

        # group by first letter
        result = { }
        for obj in obj_list:
            letter = obj.name[0].upper()
            display_name = obj.name
            if isinstance(obj, docobjects.Function):
                display_name += '()'
            link = object_link(obj)
            text = obj.abs_name

            result[letter] = result.get(letter, [ ]) + [ (link, display_name, text) ]

        return result
    _find_variables_and_functions = staticmethod(_find_variables_and_functions)

    def write_namespace_index(self):
        """Generate index of variables and functions

        Creates namespace_index.html in output directory
        """
        output_dir = self.options.docdir
        customheader = self.options.header
        customfooter = self.options.footer
        module_list = self.modules
        package_name = self.package_namespace.name
        extrastyle = self.get_extra_style()

        objects = self._find_variables_and_functions(module_list)
        
        # various template arguments
        header_title = "Namespace Index"
        title = "%s -- %s" % (package_name, header_title)
        stylesheet = "default.css"

        # load template for alphabetic index
        template = self.template_loader.load('alpha_list')

        # prepare list of first letters
        letter_list = objects.keys()
        letter_list.sort()

        # render template and write to disk
        of = open(os.path.join(output_dir, 'namespace_index.html'), 'wt')
        of.write(template.render(vars()))
        of.close()

    def _add_links(cls, hierarchy):
        """The hierarchicalize_modules function in the tools module
        does not know about HTML.  This function generates links to
        objects organized in hierarchy."""
        result = [ ]
        for obj, subobjs in hierarchy:
            subobjs = cls._add_links(subobjs)
            if obj.is_concrete():
                link = object_link(obj)
            else:
                link = ''
            result.append((obj, link, subobjs))
        return result

    _add_links = classmethod(_add_links)
            
    def write_class_hierarchy(self):
        """Write class hierarchy index

        Generates class_hierarchy.html in output directory
        """
        output_dir = self.options.docdir
        customheader = self.options.header
        customfooter = self.options.footer
        module_list = self.modules
        package_name = self.package_namespace.name
        extrastyle = self.get_extra_style()

        # generate class hierarchy
        hierarchy = self._add_links(docobjects.build_class_hierarchy(module_list))

        # template arguments
        header_title = "Class Hierarchy"
        title = "%s -- %s" % (package_name, header_title)
        stylesheet = "default.css"

        # load template for collapsible tree-control view of hierarchy
        t = self.template_loader.load('hierarchy')
        
        # render template with local variables as arguments and write to disk
        of = open(os.path.join(output_dir, 'class_hierarchy.html'), 'wt')
        show_abs_name = True
        of.write(t.render(vars()))
        of.close()

    def print_exception_list(self, header, exc_list):
        """Show the list of exceptions generated during documentation processing

           * header   : the text to display at the top of the list
           * exc_list : list of tuples generated by sys.exc_info()
        """
        sys.stdout.write("\n\n\n%s\n\n" % header)
        for mod_name, exc_info in exc_list:
            exc_type, exc_value, exc_traceback = exc_info
            sys.stdout.write("Module: %s\n" % mod_name)
            if exc_type in [ FormattingException, SystemMessage ]:
                sys.stdout.write(str(exc_value) + '\n\n\n')
            else:
                print_exception(exc_type, exc_value, exc_traceback,
                                file=sys.stdout)
                sys.stdout.write('\n\n')
    
    def generate(self):
        "Generate HTML documentation in output directory"
        options = self.options
        output_dir = options.docdir
        package_namespace = self.package_namespace
        module_list = self.modules
        
        if len(module_list) == 0:
            # nothing to document!
            sys.stderr.write("There are no modules to document!\n")
            return

        # copy needed support files into output directory
        self.copy_data_files()

        # generate indices
        self.write_index()
        self.write_class_index()
        self.write_namespace_index()
        self.write_class_hierarchy()

        # write page for each module, recording exceptions and moving on
        for mod in module_list:
            try:
                if self.options.verbose:
                    sys.stdout.write("Documenting %s ... " % mod.abs_name)
                    sys.stdout.flush()
                self.write(mod)
                if self.options.verbose:
                    sys.stdout.write("ok.\n")
            except KeyboardInterrupt:
                sys.stderr.write("Interrupted!  Exiting...\n")
                sys.exit(0)
            except:
                if self.options.verbose:
                    sys.stdout.write("error! moving on...\n")
                exc_info = sys.exc_info()
                self.exceptions.append((mod.name, exc_info))

        if len(self.exceptions) > 0:
            self.print_exception_list("The following exceptions were encountered:", self.exceptions)

        if len(self.rst_errors) > 0:
            self.print_exception_list("The following RST errors were encountered:", self.rst_errors)

        

