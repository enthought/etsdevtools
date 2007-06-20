# A collection of useful debugging tools.  These should NOT make it into
# production code.

import os



def called_from( levels = 1, context = 1):
    """ Print the current call stack. """

    from inspect import stack
    stk = stack(context)
    frame, file_name, line_num, func_name, lines, index = stk[1]
    print "'%s' called from:" % func_name
    for frame_rec in stk[ levels + 1: 1: -1 ]:
        frame, file_name, line_num, func_name, lines, index = frame_rec
        print '   %s (%s: %d)' % (func_name, file_name, line_num)
        if lines is not None:
            if len(lines) == 1:
                print '      ' + lines[0].strip()[:73]
            else:
                for i, line in enumerate(lines):
                    print '   %s  %s' % ('|>'[ i == index ], line.rstrip())


def log_called_from( levels = 1, context = 1):
    """ Logs the current call stack as debug information """

    from inspect import stack

    # Setup a logger
    import logging
    logger = logging.getLogger(__name__)

    stk = stack(context)
    frame, file_name, line_num, func_name, lines, index = stk[1]
    logger.debug("'%s' called from:", func_name)
    for frame_rec in stk[ levels + 1: 1: -1 ]:
        frame, file_name, line_num, func_name, lines, index = frame_rec
        logger.debug( '   %s (%s: %d)', func_name, file_name, line_num)
        if lines is not None:
            if len(lines) == 1:
                logger.debug('      ' + lines[0].strip()[:73])
            else:
                for i, line in enumerate(lines):
                    logger.debug('   %s  %s', '|>'[ i == index ], line.rstrip())


def what_is ( obj ):
    """ Print the class hierarchy of an object. """

    class_hierarchy(obj.__class__)

def class_hierarchy(clazz, lead=""):
    """ Print the class hierarchy of a class. """

    print lead + str(clazz)
    for child in clazz.__bases__:
        class_hierarchy(child, lead + "  ")

