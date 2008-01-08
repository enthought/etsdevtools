# Testoob, Python Testing Out Of (The) Box
# Copyright (C) 2005-2006 The Testoob Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"XSL converters for XML output"

# TODO: only one converter, do we need this?

def _read_file(filename):
    from os.path import join, dirname
    f = open(join(dirname(__file__), filename))
    try: return f.read()
    finally: f.close()

import html_xsl
BASIC_CONVERTER = html_xsl.XSL
