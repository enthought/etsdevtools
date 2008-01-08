###########################################################################
# File:    template.py
# Project: endo
# Date:    2005-07-29
# Author:  David Baer
# 
# Description:
#  Simple template engine
# 
###########################################################################

"""
This is a simple template engine.  It supports a limited number of control
structures, as well as simple python expressions referencing variables in
the template context.

Usage:

>>> t = Template(template_code)
>>> context = { 'spam' : 1, 'eggs' : 2 }
>>> text = t.render(context)

Template tags:

{{ EXPR }}

   Evaluate EXPR against the template context and insert the result
   in the output.

{% assign VAR=EXPR %}

   Assign the name VAR in the current context to the value of EXPR.

{% block NAME %}{% endblock %}

   Everything enclosed in a block may be overridden by an extending template.

{% extends "base_template" %}

   Render "base_template", but replace all blocks that are overridden in
   this template

{% for VAR1[,VAR2[,VAR3]] in LIST_EXPR %}{% endfor %}

   A for loop, just as in Python.

{% if TEST %} [{% else %}] {% endif %}

   Evaluate test and execute the appropriate block.

{% include TEMPLATE [PARAM1=EXPR1 [PARAM2=EXPR2]] %}

   Evaluate the specified template against the current context (with
   specified additional parameters), and insert the resulting text
   in the output.




"""

import re
from traceback import format_exception, format_stack
import sys

NODE_SEQ  = 1
NODE_LIT  = 2
NODE_FOR  = 3
NODE_IF   = 4
NODE_VARIABLE = 5
NODE_BLOCK = 6
NODE_EXTENDS = 7
NODE_INCLUDE = 8
NODE_ASSIGN = 9
NODE_SUPER = 10
NODE_GENID = 11

TOK_LITERAL  = 0
TOK_VARIABLE = 1
TOK_CONTROL  = 2
TOKEN_VARIABLE_TAG = re.compile(r'\{\{([^\}]|\}[^\}])*\}\}')
TOKEN_CONTROL_TAG = re.compile(r'\{%([^%\}]|%[^\}])*%\}')

_ID = 0
def gen_id():
    global _ID
    _ID += 1
    result = '%05d' % _ID
    #print "GENERATED ID '%s'" % result
    return result

def _lexicalize(code):
    L = [ (x.start(), x.end(), TOK_VARIABLE, x.group()[2:-2].strip()) for x in TOKEN_VARIABLE_TAG.finditer(code) ]

    L.extend([ (x.start(), x.end(), TOK_CONTROL, x.group()[2:-2].strip()) for x in TOKEN_CONTROL_TAG.finditer(code) ])
    L.sort()

    literals_list = [ ]
    lastend = 0
    for index in range(0, len(L)):
        start, end = L[index][:2]
        if start > lastend:
            literals_list.append((lastend, start, TOK_LITERAL, code[lastend:start]))
        lastend = end
    if len(code) > lastend:
        literals_list.append((lastend, len(code), TOK_LITERAL, code[lastend:]))

    L.extend(literals_list)
    L.sort()
    return L

def _parse_if(if_test, tok_iterator):
    seq, endblock = _parse_seq(tok_iterator, [ 'else', 'endif' ])
    if endblock == 'else':
        else_seq = _parse_seq(tok_iterator, [ 'endif' ])[0]
    else:
        else_seq = (NODE_SEQ, [ ])
    return (NODE_IF, if_test, seq, else_seq)

def _parse_seq(tok_iterator, endblock = [ ]):
    result = [ ]
    break_tok = None

    for tok_start, tok_end, tok_type, tok_text in tok_iterator:
        if tok_type == TOK_LITERAL:
            result.append((NODE_LIT, tok_text))
        elif tok_type == TOK_VARIABLE:
            result.append((NODE_VARIABLE, tok_text))
        elif tok_type == TOK_CONTROL:
            control_type = tok_text.split()[0]
            if control_type in endblock:
                break_tok = control_type
                break
            if control_type == 'block':
                block_name = tok_text.split()[1]
                seq, junk = _parse_seq(tok_iterator, [ 'endblock' ])
                result.append((NODE_BLOCK, block_name, seq))
            elif control_type == 'if':
                if_test = tok_text[len(control_type):].strip()
                result.append(_parse_if(if_test, tok_iterator))
            elif control_type == 'for':
                rest = ' '.join(tok_text.split()[1:])
                loop_vars, list_var = rest.split(' in ')
                loop_vars = re.compile(', *').split(loop_vars)
                seq, junk = _parse_seq(tok_iterator, [ 'endfor' ])
                result.append((NODE_FOR, loop_vars, list_var, seq))
            elif control_type == 'extends':
                name = eval(tok_text.split()[1], { })
                result.append((NODE_EXTENDS, name))
            elif control_type == 'include':
                fields = tok_text.split()
                name = fields[1]
                params = [ (pname, value) for pname, value in map(lambda x: x.split('='), fields[2:]) ]
                result.append((NODE_INCLUDE, name, params))
            elif control_type == 'assign':
                arg = tok_text.split()[1]
                name, value = arg.split('=')
                result.append((NODE_ASSIGN, name, value))
            elif control_type == 'super':
                fields = tok_text.split()
                params = [ (pname, value) for pname, value in map(lambda x: x.split('='), fields[1:]) ]
                result.append((NODE_SUPER, params))
            elif control_type == 'genid':
                arg = tok_text.split()[1]
                result.append((NODE_GENID, arg))

    return ((NODE_SEQ, result), break_tok)
            

class Template:
    """
    HTML template object
    """
    LOADER = None

    def set_loader(cls, template_loader):
        "specify default template loader"
        cls.LOADER = template_loader
    set_loader = classmethod(set_loader)

    def __init__(self, code, file = '(string)', loader = None):
        """
        Load new template.

          code   : template code
          file   : filename of template (optional, for error messages)
          loader : template loader to use for {%extends%}, {%include%}
        """
        tok_iterator = iter(_lexicalize(code))
        self.parse_tree = _parse_seq(tok_iterator)[0]
        self.file = file

        if loader is None:
            self.loader = self.LOADER
        else:
            self.loader = loader

        if len(self.parse_tree[1]) > 0 and self.parse_tree[1][0][0] == NODE_EXTENDS:
            supertemplate_name = self.parse_tree[1][0][1]
            self.supertemplate = self.loader.load(supertemplate_name)
        else:
            self.supertemplate = None

    def render_seq(self, seq, context, blocks = [ ], superblock = None):
        """
        Render a SEQ node -- internal use only
        """
        result = ''
        for node in seq[1]:
            node_type = node[0]
            if node_type == NODE_LIT:
                result += node[1]
            elif node_type == NODE_FOR:
                loop_vars, list_var, loop_seq = node[1:]
                try:
                    loop_list = eval(list_var, context)
                except:
                    exc_info = sys.exc_info()
                    result += '\n<!--(file: %s)\n' % self.file + ''.join(format_exception(*exc_info)) + '\n-->\n'
                    loop_list = [ ]
                for t_list in loop_list:
                    for index in range(0, len(t_list)):
                        context[loop_vars[index]] = t_list[index]
                    result += self.render_seq(loop_seq, context, blocks, superblock)
            elif node_type == NODE_BLOCK:
                name = node[1]
                i = len(blocks) - 1
                done = False
                # if an override exists at a lower level...
                while i >= 0:
                    if blocks[i].has_key(name):
                        # found an override at level i
                        # ... so the only blocks that can override this are
                        # ... at level < i
                        #
                        # note that we provide this block to the overriding
                        #   block (last param below)
                        my_superblock = self.render_seq(node[2], context, blocks, superblock)
                        my_repl = self.render_seq(blocks[i][name], context, blocks[:i], my_superblock)
                        result += my_repl
                        done = True
                        break
                    else:
                        i -= 1
                if not done:
                    result += self.render_seq(node[2], context, blocks, superblock)
            elif node_type == NODE_IF:
                test_expr = node[1]
                try:
                    test_result = eval(test_expr, context)
                except:
                    exc_info = sys.exc_info()
                    result += '\n<!--(file: %s)\n' % self.file + ''.join(format_exception(*exc_info)) + '\n' + repr(seq) + ''.join(format_stack()) + '\n-->\n'
                    test_result = False
                if test_result:
                    result += self.render_seq(node[2], context, blocks, superblock)
                else:
                    result += self.render_seq(node[3], context, blocks, superblock)
            elif node_type == NODE_VARIABLE:
                try:
                    value = eval(node[1], context)
                except:
                    exc_info = sys.exc_info()
                    result += '\n<!--(file: %s)\n' % self.file + ''.join(format_exception(*exc_info)) + '\n-->\n'
                    value = ''
                result += str(value)
            elif node_type == NODE_INCLUDE:
                t_name = node[1]
                params = node[2]
                subcontext = context.copy()
                for name, value in params:
                    try:
                        value = eval(value, context)
                        subcontext[name] = value
                    except:
                        exc_info = sys.exc_info()
                        result += '\n<!--(file: %s)\n' % self.file + ''.join(format_exception(*exc_info)) + '\n-->\n'
                try:
                    real_name = eval(t_name, context)
                    t = self.loader.load(real_name)
                    result += t.render(subcontext)
                except:
                    exc_info = sys.exc_info()
                    result += '\n<!--(file: %s)\n' % self.file + ''.join(format_exception(*exc_info)) + '\n -->\n'
            elif node_type == NODE_ASSIGN:
                name, value = node[1:3]
                try:
                    value = eval(value, context)
                    context[name] = value
                except:
                    exc_info = sys.exc_info()
                    result += '\n<!--(file: %s)\n' % self.file + ''.join(format_exception(*exc_info)) + '\n-->\n'
            elif node_type == NODE_SUPER:
                # this is an override, but we want to include the overridden
                # text
                if superblock is not None:
                    result += superblock
            elif node_type == NODE_GENID:
                arg = node[1]
                new_id = gen_id()
                context[arg] = new_id
                
        return result

    def render(self, context = { }, blocks = [ ]):
        """
        Render template with the specified context.

        context : dictionary of variables and values
        blocks  : internal use only
        """
        if self.supertemplate is not None:
            b = blocks[:]
            b.append(self._get_blocks(context))
            return self.supertemplate.render(context, b)
        return self.render_seq(self.parse_tree, context, blocks)

    def _get_blocks(self, context):
        "internal function -- get top-level blocks to override base template"
        result = { }
        for node in self.parse_tree[1]:
            node_type = node[0]
            if node_type == NODE_BLOCK:
                name = node[1]
                result[name] = (NODE_SEQ, [ node ])
        return result
                
