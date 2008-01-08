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

"The proxy used as a result object for PyUnit suites"

# TODO: separate the PyUnit result-object passed to the fixtures and
#       the observable proxy that proxies everything to reporters.
#       Notice the '_apply_method' duplication in each method, this should
#       be removed.

from test_info import TestInfo
from err_info import ErrInfo

def synchronize(func, lock=None):
    if lock is None:
        import threading
        lock = threading.RLock()

    def wrapper(*args, **kwargs):
        lock.acquire()
        try:
            return func(*args, **kwargs)
        finally:
            lock.release()

    return wrapper

def _should_skip(err):
    import testoob
    try:
        return issubclass(err[0], testoob.SkipTestException)
    except TypeError:
        # subclass check failed, assume not a subclass
        return False

class ReporterProxy:
    def __init__(self, threads=False):
        self.observing_reporters = []
        self.shouldStop = False

        if threads:
            self._apply_method = synchronize(self._apply_method)

    def add_observer(self, reporter):
        self.observing_reporters.append(reporter)

    def _apply_method(self, name, *args):
        for reporter in self.observing_reporters:
            getattr(reporter, name)(*args)

    def start(self):
        self._apply_method("start")

    def stop(self):
        self.shouldStop = True
        self._apply_method("stop")

    def done(self):
        self._apply_method("done")

    def startTest(self, test):
        self._apply_method("startTest", TestInfo(test))

    def stopTest(self, test):
        self._apply_method("stopTest", TestInfo(test))

    def addError(self, test, err):
        if _should_skip(err):
            self._apply_method("addSkip", TestInfo(test), ErrInfo(test, err))
            return

        self._apply_method("addError", TestInfo(test), ErrInfo(test, err))

    def addFailure(self, test, err):
        self._apply_method("addFailure", TestInfo(test), ErrInfo(test, err))

    def addSuccess(self, test):
        self._apply_method("addSuccess", TestInfo(test))

    def addAssert(self, test, assertName, varList, exception):
        self._apply_method("addAssert", TestInfo(test), assertName, varList, exception)

    def addSkip(self, test, err):
        self._apply_method("addSkip", TestInfo(test), ErrInfo(test, err))

    def isSuccessful(self):
        for reporter in self.observing_reporters:
            if not reporter.isSuccessful():
                return False # One failed reporter is enough
        return True
