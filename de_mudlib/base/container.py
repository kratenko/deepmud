class Container(pyclass("/base/describable")):
    def __init__(self):
        super().__init__()
        self.contents = []

    def insert(self, item):
        self.contents.append(item)
        item.environment = self

    def remove(self, item):
        item.environment = None
        self.contents.remove(item)

    def find(self, name):
        for thing in self.contents:
            if thing.name and self.unify(thing.name) == self.unify(name):
                return thing
        return None

    def unify(self, command):
        # TODO: nicht nur Deutsch unterstützen
        return command.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
