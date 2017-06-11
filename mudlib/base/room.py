class Room(pyclass("/base/container")):
    def __init__(self):
        super().__init__()
        self.exits = []

    def add_exit(self, direction, destination):
        self.exits.append((direction, destination))
