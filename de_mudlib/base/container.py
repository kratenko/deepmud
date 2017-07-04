class Container(pyclass("/base/entity")):
    def __init__(self):
        super().__init__()
        self.contents = []

    def insert(self, item):
        self.contents.append(item)
        item.environment = self

    def remove(self, item):
        item.environment = None
        self.contents.remove(item)
