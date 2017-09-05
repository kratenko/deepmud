
class Void(pyclass('/base/room')):

    def create(self):
        self.add_description(
                "Das Nichts",
                "Du befindest Dich im Nichts. Hier ist nichts."
        )

        self.add_description(
                "Das Nichts",
                "Du kannst das hier lesen weil du 'foo' heisst.",
                guard=self._spieler_heisst_foo
        )

        self.add_exit("osten", "/world/void")

    def _spieler_heisst_foo(self, *x, **y):
        return y['spieler'].name == 'foo'
