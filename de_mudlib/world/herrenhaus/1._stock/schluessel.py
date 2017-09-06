class Schluessel(pyclass("/item/key")):

    def create(self):
        self.name = "schlüssel"
        self.add_description("Ein kleiner Schlüssel", "Ein kleiner Messingschlüssel mit einem winzigen Bart.")
        self.key_secret = "herrenhaus.messing"
