class Flower(pyclass("/base/item")):
    kind = "cloneable"

    def create(self):
        super().create()
        self.description = "A beautiful flower."

