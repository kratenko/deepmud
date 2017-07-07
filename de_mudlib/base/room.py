class Room(pyclass("/base/container")):
    def __init__(self):
        super().__init__()
        self.exits = []
        self.guarded_descriptions = []
        self.unguarded_description = {'short': '<missing>', 'long': '<missing>', 'guard': None}

    def add_exit(self, direction, destination):
        self.exits.append((direction, destination))

    def add_description(self, short_msg, long_msg, guard=None):
        desc = {'short': short_msg, 'long': long_msg, 'guard': guard}
        if not guard:
            self.unguarded_description = desc
        else:
            self.guarded_descriptions.append(desc)

    def get_description(self, context: dict):
        for desc in self.guarded_descriptions:
            if desc['guard'](**context):
                return desc
        return self.unguarded_description

