import logging
import sys
import unittest
from unittest.case import _Outcome


class RaiseLogOutput(logging.Handler):
    LOGGING_FORMAT = '%(levelname)s:%(name)s:%(message)s'

    def __init__(self):
        super().__init__()
        self.setFormatter(logging.Formatter(self.LOGGING_FORMAT))

    def emit(self, record):
        raise AssertionError(
            f'Uncaptured log message during the test:\n'
            '------------------------------------------------------------------------------------\n'
            f'{self.format(record)}\n'
            '------------------------------------------------------------------------------------\n'
            '(Hint: use self.assertLogs() context manager)'
        )


class LoggingMustBeCapturedTestCaseMixin:
    def setUp(self):
        super().setUp()
        self.logger = logging.getLogger()

        self.old_handlers = self.logger.handlers[:]
        self.old_level = self.logger.level
        self.old_propagate = self.logger.propagate

        self._log_buffer_handler = RaiseLogOutput()
        self.logger.addHandler(self._log_buffer_handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

    def tearDown(self):
        self.logger.handlers = self.old_handlers
        self.logger.propagate = self.old_propagate
        self.logger.setLevel(self.old_level)
        super().tearDown()


class OutputWriteTracker:
    def __init__(self):
        self.output_written = False
        self._original_stdout = None
        self._original_stderr = None

    class _StreamWrapper:
        def __init__(self, original, tracker):
            self._original = original
            self._tracker = tracker

        def write(self, data):
            self._tracker.output_written = True
            return self._original.write(data)

        def flush(self):
            return self._original.flush()

        def __getattr__(self, attr):
            return getattr(self._original, attr)

    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = self._StreamWrapper(sys.stdout, self)
        sys.stderr = self._StreamWrapper(sys.stderr, self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr
        return self.output_written


class OutputMustCapturedTestCaseMixin:
    def setUp(self):
        super().setUp()
        self._output_tracker = OutputWriteTracker()
        self._output_tracker.__enter__()

    def tearDown(self):
        outcome: _Outcome = self._outcome
        test_success = not outcome.result.errors

        output_written = self._output_tracker.__exit__(None, None, None)
        super().tearDown()

        if output_written and test_success:
            raise AssertionError('Output was written during test!')


class BaseTestCase(
    OutputMustCapturedTestCaseMixin,
    LoggingMustBeCapturedTestCaseMixin,
    unittest.TestCase,
):
    """
    A base TestCase that ensures that all logging and output is captured during tests.
    """
