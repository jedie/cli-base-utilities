from pathlib import Path

from rich import print


class UpdateTestSnapshotFiles:
    def __init__(self, *, root_path: Path, verbose=True):
        self.root_path = root_path
        self.verbose = verbose

        self.removed_file_count = None
        self.new_file_count = None

    def get_snapshotfiles(self):
        return self.root_path.rglob('*.snapshot.*')

    def __enter__(self):
        self.removed_file_count = 0
        for item in self.get_snapshotfiles():
            item.unlink()
            self.removed_file_count += 1

        if self.verbose:
            print(f'{self.removed_file_count} test snapshot files removed...')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.new_file_count = len(list(self.get_snapshotfiles()))
        if self.verbose:
            print(f'{self.new_file_count} test snapshot files created, ok.\n')

        if exc_type:
            return False
