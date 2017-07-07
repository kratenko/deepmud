import re


class Login(object):
    """
    Klasse um den Loginprozess abzuwickeln.

    Diese Klasse stellt das erste Objekt, dass einem neuen Client als anchor
    zugewiesen wird. Sie regelt den Loginprozess und übergibt nach dem
    erfolgreichen Login den Client an ein neues Playerobjekt.
    """

    kind = "cloneable"
    greeting = """We need to go deeper.

Willkommen im Deep Mud!
Welcher Buchstabe kommt im griechischen Alphabet eigentlich vor Alpha?
In der Phase sind wir in etwa. Also erwarte nicht zu viel.

"""

    def __init__(self):
        self.state = "init"
        self.client = None

    def create(self):
        pass

    def handle_command(self, command):
        if self.state == 'name':
            name = command.command
        if re.match(r"^\w{3,15}$", name) and not re.match(r".*\d.*", name):
            self.logger.info("Logging in player %s", name)
            self.send("Hallo %s!\n" % name)
            body = self._mlclass.mudlib.clone("/base/player")
            body.name = name
            body.environment = single("/world/void")
            self.client.attach_anchor(body)
            self.client = None
        else:
            self.send("Tut mir leid, derzeit muss jeder Name aus 3-15 Buchstaben bestehen.\nBitte versuch's noch mal: ")

    def attach_client(self, client):
        self.client = client
        self.send(self.greeting)
        self.send("Bitte nenne deinen Namen: ")
        self.state = "name"

    def send(self, data):
        self.client.send(data)
