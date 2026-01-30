

class FakeNamedTemporaryFile:
    """
    A fake context manager that simulates tempfile.NamedTemporaryFile
    but does not create any actual files.

    with patch('tempfile.NamedTemporaryFile', FakeNamedTemporaryFile):
        # ...
    """

    def __init__(self, prefix: str = 'prefix', suffix: str = 'suffix'):
        self.name = f'/tmp/{prefix}<rnd>{suffix}'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
