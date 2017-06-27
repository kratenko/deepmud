class Player(pyclass("/base/container")):
    kind = "cloneable"

    def __init__(self):
        super().__init__()
        self.client = None
        self.name = "Spieler"
        self.add_action("hilfe", self.action_hilfe)
        self.add_action("ende", self.action_ende)

    def attach_client(self, client):
        self.client = client
        self.send("Mit 'hilfe' bekommst du soetwas ähnliches wie Hilfe.")

    def action_hilfe(self, command):
        self.send("  = Hilfe =  \nMit 'ende' kannst du das Spiel verlassen.")
        return True, None

    def action_ende(self, command):
        self.send("Bis bald!")
        self.client.disconnect(reason="Player quit.")
        return True, ""

    def _try_action(self, supplier, command):
        message = None
        if supplier.actions:
            for cmd_def, callback in supplier.actions:
                if command.command in cmd_def:
                    success, message = callback(command=command)
                    if success:
                        return True, None
        return False, message

    def action(self, command):
        """
        Try to execute command.

        Looks to match actions in self, environment, other contents in environment,
        items in inventory (in that order).
        :param command:
        :return:
        """
        message = None
        # try self:
        success, msg = self._try_action(self, command)
        if success:
            return success, msg
        else:
            message = message or msg
        # try environment:
        if self.environment:
            success, msg = self._try_action(self.environment, command)
            if success:
                return success, msg
            else:
                message = message or msg
            # try stuff in environment:
            for item in self.environment.contents:
                if item is self:
                    continue
                success, msg = self._try_action(item, command)
                if success:
                    return success, msg
                else:
                    message = message or msg
        # try inventory:
        for item in self.contents:
            success, msg = self._try_action(item, command)
            if success:
                return success, msg
            else:
                message = message or msg
        return False, message

    def send(self, text, *, raw=False):
        if not raw:
            if not text.endswith("\n"):
                text += "\n"
        if self.client:
            self.client.send(text)

    def handle_command(self, command):
        success, message = self.action(command)
        if not success:
            if message:
                self.send(message)
            else:
                self.send("Wie bitte?")