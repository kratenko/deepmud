class Door(pyclass("/base/describable")):

    kind = "cloneable"

    def __init__(self):
        super().__init__()
        self.name = "tür"
        self.add_action("öffne", self.action_oeffne)
        self.add_action(["schließe", "schließ"], self.action_schliesse)
        self.add_action(["verschließe", "verschließ"], self.action_verschliesse)
        self.closed = True
        self.locked = False
        self.key_secret = None
        self.add_description("Eine Tür", "Eine Tür")
        self.takeable = False

    def action_oeffne(self, command):
        if not command.args:
            return "Öffne was?"
        if command.get_target() == self:
            if self.closed:
                if self.locked:
                    return "Die Tür ist verschlossen."
                command.actor.send("Du öffnest die Tür.")
                self.closed = False
                return True
            else:
                return "Die Tür ist bereits offen."
        return command.arg_line + " nicht gefunden."

    def action_schliesse(self, command):
        if not command.args:
            return "Schließe was (ab/auf/zu)?"
        target = command.get_target()
        if not target:
            return command.arg_line + " nicht gefunden."

        if target == self:
            if len(command.args) > 1:
                if command.args[-1].lower() == 'auf':
                    return self.aufschliessen(command)
                elif command.args[-1].lower() in ('zu', 'ab'):
                    return self.abschliessen(command)
            if self.closed:
                return "Die Tür ist bereits geschlossen."
            else:
                if self.locked:
                    return "Die Tür ist verschlossen."
                command.actor.send("Du schließt die Tür.")
                self.closed = True
                return True
        return command.arg_line + " nicht gefunden."

    def abschliessen(self, command):
        if self.closed:
            if self.locked:
                return "Die Tür ist bereits abgeschlossen."
            else:
                key = self.find_key(command.actor)
                if key:
                    self.locked = True
                    command.actor.send("Du schließt die Tür ab mit deinem " + key.name + ".")
                    return True
                else:
                    return "Du hast keinen passenden Schlüssel."
        else:
            return "Du solltest die Tür erstmal schließen."

    def aufschliessen(self, command):
        if self.closed:
            if self.locked:
                key = self.find_key(command.actor)
                if key:
                    self.locked = False
                    command.actor.send("Du schließt die Tür auf mit deinem " + key.name + ".")
                    return True
                else:
                    return "Du hast keinen passenden Schlüssel."
            else:
                return "Die Tür ist nicht abgeschlossen."
        else:
            return "Die Tür ist nicht mal geschlossen sondern steht offen."

    def action_verschliesse(self, command):
        if not command.args:
            return "Verschließe was?"
        target = command.get_target()
        if not target:
            return command.arg_line + " nicht gefunden."
        return self.abschliessen(command)


    def find_key(self, where):
        if not self.key_secret:
            return None
        for ding in where.contents:
            if hasattr(ding, "can_lock") and ding.can_lock(self.key_secret):
                return ding
        return None

    def create(self):
        pass