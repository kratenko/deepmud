class Entity(object):
    """
    Base class for everything existing in mudlib.
    """
    kind = "singleton"

    def __init__(self):
        self._mlclass = None
        # environment: item this item is inside of.
        self.environment = None
        self.actions = None

    def add_action(self, command, callback):
        if self.actions is None:
            self.actions = []
        self.actions.append(Action(command, callback))

    def try_command(self, supplier, command):
        if self.actions:
            for action in self.actions:
                if action.matches(command.command):
                    # matches!
                    command.supplier = supplier
                    result = action.callback(command)
                    if result is not False:
                        return result
        return False

    def create(self):
        """
        Dummy create function; override it.
        :return:
        """
        pass


class Action(object):

    def unify(self, command):
        # TODO: nicht nur Deutsch unterstützen
        return command.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')

    def __init__(self, command, callback):
        if isinstance(command, str):
            self.command = command
            self.aliases = [self.unify(command)]
        else:
            self.command = None
            self.aliases = []
            for cmd in command:
                if self.command is None:
                    self.command = cmd
                self.aliases.append(self.unify(cmd))
        self.callback = callback

    def matches(self, command):
        return self.unify(command) in self.aliases