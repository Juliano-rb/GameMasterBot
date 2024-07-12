# in-memory database class based on key-value atribution
class Database:
    def __init__(self) -> None:
        self.data = {}

    def get(self, key):
        return self.data.get(key, {})

    def set(self, key, value):
        self.data[key] = value
