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

"convenience functions for running tests"

###############################################################################
# apply_runner
###############################################################################
from testoob.extracting import suite_iter as _suite_iter
from testoob.extracting import full_extractor as _full_extractor

def apply_decorators(callable, decorators):
    "Wrap the callable in all the decorators"
    result = callable
    for decorator in decorators:
        result = decorator(result)
    return result

def apply_runner(suites, runner, interval=None, stop_on_fail=False,
                 extraction_decorators=None, fixture_decorators=None):
    """Runs the suite."""
    from fixture_decorators import BaseFixture, InterruptedFixture
    if not fixture_decorators: fixture_decorators = [BaseFixture]
    if extraction_decorators is None: extraction_decorators = []
    test_extractor = apply_decorators(_full_extractor, extraction_decorators)

    def running_loop(fixture_decorators):
        import time
        first = True
        for suite in _suite_iter(suites):
            for fixture in test_extractor(suite):
                try:
                    decorated_fixture = apply_decorators(fixture, fixture_decorators)
                    if not first and interval is not None:
                        time.sleep(interval)
                    first = False
                    if not runner.run(decorated_fixture) and stop_on_fail:
                        return
                except KeyboardInterrupt, e:
                    fixture_decorators = [InterruptedFixture]
                    # Run the current test again with InterrupFixture decorator
                    # So it'll be added to the skipped tests' list too.
                    decorated_fixture = apply_decorators(fixture, fixture_decorators)
                    runner.run(decorated_fixture)

    running_loop(fixture_decorators)
    runner.done()
    return runner.isSuccessful()

###############################################################################
# run
###############################################################################
def run(suite=None, suites=None, **kwargs):
    "Convenience frontend for text_run_suites"
    if suite is None and suites is None:
        raise TypeError("either suite or suites must be specified")
    if suite is not None and suites is not None:
        raise TypeError("only one of suite or suites may be specified")

    if suites is None:
        suites = [suite]

    return run_suites(suites, **kwargs)

def _apply_debug(reporter, runDebug):
    if runDebug is None:
        return reporter

    def replace(reporter, flavor, methodname):
        original = getattr(reporter, methodname)
        def replacement(test, err):
            runDebug(test, err, flavor, reporter, original)
        setattr(reporter, methodname, replacement)

    replace(reporter, "error", "addError")
    replace(reporter, "failure", "addFailure")

    return reporter

def _create_reporter_proxy(reporters, runDebug, threads):
    from testoob.reporting import ReporterProxy
    result = ReporterProxy(threads)
    for reporter in reporters:
        result.add_observer(_apply_debug(reporter, runDebug))
    return result

def run_suites(suites, reporters, runner=None, runDebug=None, threads=None, **kwargs):
    "Run the test suites"
    if runner is None:
        from simplerunner import SimpleRunner
        runner = SimpleRunner()
    runner.reporter = _create_reporter_proxy(reporters, runDebug, threads=threads)
    
    return apply_runner(suites=suites,
                        runner=runner,
                        **kwargs)

###############################################################################
# text_run
###############################################################################
def text_run(*args, **kwargs):
    """
    Run suites with a TextStreamReporter.
    Accepts keyword 'verbosity' (0, 1, 2 or 3, default is 1)
    and 'immediate' (True or False)
    """
    from testoob.utils import _pop

    verbosity = _pop(kwargs, "verbosity", 1)
    immediate = _pop(kwargs, "immediate", False)
    coverage  = _pop(kwargs, "coverage",  (None, None))
    silent    = _pop(kwargs, "silent",    False)

    kwargs.setdefault("reporters", [])

	# Always have at least one base reporter, so isSuccessful always works
    from testoob.reporting.base import BaseReporter
    kwargs["reporters"].append(BaseReporter())

    import sys
    from testoob.reporting import TextStreamReporter
    reporter_class = _pop(kwargs, "reporter_class", TextStreamReporter)

    if not silent:
        reporter_instance = reporter_class(
                verbosity=verbosity,
                immediate=immediate,
                descriptions=1,
                stream=sys.stderr)

        kwargs["reporters"].append(reporter_instance)

    for reporter in kwargs["reporters"]:
        reporter.setCoverageInfo(*coverage)

    return run(*args, **kwargs)
