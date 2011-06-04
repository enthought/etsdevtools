
###########################################################################
# File:    docerror.py
# Project: endo
# Date:    2005-06-09
# Author:  David Baer
#
# Description:
#   Exceptions for doc tool
#
###########################################################################

"Exception class for endo errors"

class DocError(Exception): pass

class DocWriteError(DocError): pass
