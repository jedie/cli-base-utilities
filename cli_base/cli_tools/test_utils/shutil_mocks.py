class ShutilWhichMock:
    """
    Mock shutil.which() function.
    """

    def __init__(self, *, command_map: dict):
        self.command_map = command_map
        self.calls = []

    def which(self, command, mode=None, path=None):
        self.calls.append(command)
        return self.command_map[command]
