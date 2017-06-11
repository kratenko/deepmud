class StartRoom(pyclass('/base/room')):
    def create(self):
        super().create()
        self.description = "This is where the world started."
        self.add_exit("east", "/stuff/secondroom")