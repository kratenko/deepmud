class Item(object):
    """
    Base class for everything existing in mudlib.
    """
    kind = "singleton"

    def __init__(self):
        self._mlclass = None
        # environment: item this item is inside of.
        self.environment = None
        self.actions = None

    def add_action(self, command, callback):
        if self.actions is None:
            self.actions = []
        if type(command) is str:
            command = (command,)
        self.actions.append(command, callback)

    def create(self):
        pass

    def test_me(self):
        return "I am an Item"
