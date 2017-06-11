class SecondRoom(pyclass("/base/room")):
    def __init__(self):
        super().__init__()
        self.description = "This is the rest of the world."
        self.add_exit("west", "/stuff/startroom")
        self.insert(clone("/stuff/flower"))
