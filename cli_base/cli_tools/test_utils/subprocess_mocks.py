from unittest.mock import patch

from bx_py_utils.test_utils.context_managers import MassContextManager


class MockToolsExecutor(MassContextManager):
    """
    Helper to mock `ToolsExecutor` in tests.
    """

    def __init__(self, *, target, return_codes: dict[str, int] = None, outputs: dict[str, str] = None):
        self.return_codes = return_codes
        self.outputs = outputs
        self.mocks = (patch.object(target, 'ToolsExecutor', self),)

        self.calls = []

    def __call__(self, cwd=None):
        self.cwd = cwd
        return self

    def _store_call(self, file_name: str, popenargs, kwargs):
        info = dict(file_name=file_name)
        if popenargs:
            info['popenargs'] = popenargs
        if kwargs:
            info['kwargs'] = kwargs
        self.calls.append(info)

    def verbose_check_call(self, file_name: str, *popenargs, **kwargs):
        self._store_call(file_name, popenargs, kwargs)
        return self.return_codes[file_name]

    def verbose_check_output(self, file_name: str, *popenargs, **kwargs):
        self._store_call(file_name, popenargs, kwargs)
        return self.outputs[file_name]
