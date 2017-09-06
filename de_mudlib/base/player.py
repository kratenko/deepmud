import logging
logger = logging.getLogger(__name__)

class Player(pyclass("/base/container")):
    kind = "cloneable"

    def __init__(self):
        super().__init__()
        self.client = None
        self.name = "Spieler"
        self.add_action("hilfe", self.action_hilfe)
        self.add_action(["schau", "schaue", "betrachte", "b"], self.action_schau)
        self.add_action("shell", self.action_shell)
        self.add_action("ende", self.action_ende)
        self.add_action(["inventar", "i"], self.action_inventar)
        self.add_action(["nimm", "nehm", "nehme", "ni"], self.action_nimm)
        self.add_action(['leg', 'lege', 'le'], self.action_lege)

    def set_name(self, name):
        self.name = name
        self.add_description(name.capitalize(), name.capitalize() + " sieht ganz gewöhnlich aus.")

    def attach_client(self, client):
        self.client = client
        self.send("Mit 'hilfe' bekommst du soetwas ähnliches wie Hilfe.")

    def action_hilfe(self, command):
        self.send("""  = Hilfe =
Mit 'ende' kannst du das Spiel verlassen.
'schaue', 'schau', 'betrachte' oder 'b' um dich umzusehen.
'inventar' oder 'i' um zu sehen, was du bei dir hast.
'nimm' oder 'nehme' um etwas aufzuheben.
'lege' um etwas abzulegen.
""")
        return True

    def _schau_umgebung(self):
        self.send(self.environment.get_description(context={
            'spieler': self,
        })['long'])

    def action_schau(self, command):
        assert self.environment is not None
        if command.args:
            target = command.get_target()
            if target:
                self.send(target.get_description(context={
                    'spieler': self,
                })['long'])
            else:
                return command.arg_line + " nicht gefunden."
        else:
            # umgebung anschauen
            self._schau_umgebung()
        return True

    def action_nimm(self, command):
        if not command.args:
            return "Nimm was?"
        target = command.get_target()
        if not target:
            return command.arg_line + " nicht gefunden."
        if target is self:
            return "Du kannst dich nicht selbst aufheben."
        if target.environment is self:
            return "Das hast du schon bei dir."
        if isinstance(target, Player):
            return target.name.capitalize() + " hätte sicher was dagegen."
        if not target.takeable:
            return "Das kannst du nicht aufheben."
        target.move(to=self)
        self.send("Okay, du hebst das auf.")
        return True

    def action_lege(self, command):
        if not self.environment:
            return "Du bist nirgends."
        if not command.args:
            return "Lege was?"
        target = command.get_target()
        if not target:
            return command.arg_line + " nicht gefunden."
        if target is self:
            return "Das funktioniert so nicht."
        if target.environment is self:
            target.move(to=self.environment)
            self.send("Okay, du legst das hin.")
            return True
        else:
            return "Das hast du nicht bei dir."

    def action_inventar(self, command):
        kram = []
        for item in self.contents:
            kram.append(item.get_description(context={
                'spieler': self,
            })['short'])
        if kram:
            self.send("Du hast bei dir:\n"+"\n".join(kram))
        else:
            self.send("Du hast nichts bei dir.")
        return True

    def action_shell(self, command):
        shell = clone('/sys/shell')
        shell.set_player(self)
        self.client.attach_anchor(shell)
        return True

    def action_ende(self, command):
        self.send("Bis bald!")
        self.client.disconnect(reason="Player quit.")
        return True

    def action(self, command):
        """
        Try to execute command.

        Looks to match actions in self, environment, other contents in environment,
        items in inventory (in that order).
        :param command:
        :return:
        """
        # 1st: try self:
        result = self.try_command(self, command)
        if result:
            return result
        # 2nd: try environment:
        if self.environment:
            result = self.environment.try_command(self.environment, command)
            if result:
                return result
            # 3rd: try other entities in environment
            for item in self.environment.contents:
                if item is self:
                    # do not try self again:
                    continue
                result = item.try_command(item, command)
                if result:
                    return result
        # 4th: try inventory:
        for item in self.contents:
            result = item.try_command(item, command)
            if result:
                return result
        # well, we tried:
        return False

    def send(self, text, *, raw=False):
        if not raw:
            if not text.endswith("\n"):
                text += "\n"
        if self.client:
            self.client.send(text)

    def handle_command(self, command):
        result = self.action(command)
        if result is True:
            # Action wurde gefunden und Command erfolgreich ausgeführt
            # Hier muss nichts mehr ausgegeben werden, das macht das command selbst
            pass
        elif result is False:
            # Keine Action konnte zum Command gefunden werden
            self.send("Wie bitte?")
        else:
            # Action zum Command gefunden, aber es lief was schief. Fehlermeldung anzeigen.
            self.send(result)
