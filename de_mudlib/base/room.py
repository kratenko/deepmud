import logging
logger = logging.getLogger(__name__)

class Room(pyclass("/base/container")):
    def __init__(self):
        super().__init__()
        self.exits = []

    def add_exit(self, direction, destination):
        self.exits.append((direction, destination))

    def try_command(self, supplier, command):
        if command.command == "w":
            logger.info("xROOM: '%s'", command.command)
            return "Da geht's nicht weiter."
        else:
            logger.info("ROOM: '%s'", command.command)
        return super().try_command(supplier, command)