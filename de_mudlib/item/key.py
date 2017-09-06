class Key(pyclass("/base/describable")):

    kind = "cloneable"

    def __init__(self):
        super().__init__()
        self.name = "schlüssel"
        self.add_description("Ein Schlüssel", "Ein Schlüssel")
        self.key_secret = None

    def can_lock(self, secret):
        if self.key_secret:
            if secret == self.key_secret:
                return True
        return False
