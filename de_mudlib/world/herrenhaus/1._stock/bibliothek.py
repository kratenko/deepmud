class Bibliothek(pyclass("/base/room")):

    def create(self):
        self.add_description(
                "Die Bibliothek eines Herrenhauses",
                "Du bist in einer gemütlich eingerichteten Bibliothek."
        )
        self.add_exit("osten", "flur")

        key = clone(self._mlclass.relative_path("schluessel"))
        key.move(self)
