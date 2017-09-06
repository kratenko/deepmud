class Flur(pyclass("/base/room")):
    def create(self):
        self.add_description(
                "Ein Flur in einem Herrenhaus",
                "Du stehst in einem Flur. Eine breite Treppe führt nach oben. Im Süden ist eine riesige Tür."
        )
        tuer = clone("/item/door")
        tuer.key_secret = "herrenhaus.messing"
        tuer.move(to=self)

        self.add_exit("sueden", "draussen")
        self.add_exit("hoch", "../1._stock/flur")
