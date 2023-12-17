import os


GITHUB_ACTION: bool = 'GITHUB_ACTION' in os.environ  # GitHub CI run?
