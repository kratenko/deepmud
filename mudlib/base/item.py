class Item(object):
    """
    Base class for everything existing in mudlib.
    """
    def __init__(self):
        self._mlclass = None
        # environment: item this item is inside of.
        self.environment = None

    def create(self):
        pass

    def test_me(self):
        return "I am an Item"
