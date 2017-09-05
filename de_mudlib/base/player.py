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

    def attach_client(self, client):
        self.client = client
        self.send("Mit 'hilfe' bekommst du soetwas ähnliches wie Hilfe.")

    def action_hilfe(self, command):
        self.send("  = Hilfe =  \nMit 'ende' kannst du das Spiel verlassen.")
        return True

    def action_schau(self, command):
        assert self.environment is not None
        self.send(self.environment.get_description(context={
            'spieler': self,
        })['long'])
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
        logger.info("ENV; %s", self.environment)
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
            pass
        elif result is False:
            self.send("Wie bitte?")
        else:
            self.send(result)
