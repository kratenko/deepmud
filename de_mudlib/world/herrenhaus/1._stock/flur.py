class Flur(pyclass("/base/room")):
    def create(self):
        self.add_description(
                "Ein Flur in einem Herrenhaus",
                "Du stehst in einem Flur. Eine breite Treppe führt nach unten. Im Westen ist eine Tür."
        )
        self.add_exit("westen", "bibliothek")
        self.add_exit("runter", "../erdgeschoss/flur")
