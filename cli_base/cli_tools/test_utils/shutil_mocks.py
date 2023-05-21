class ShutilWhichMock:
    def __init__(self, map: dict):
        self.map = map

        self.calls = []

    def which(self, command, path=None):
        self.calls.append(command)
        return self.map.get(command)
