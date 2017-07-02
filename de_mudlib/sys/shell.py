import sys
from code import InteractiveConsole
from io import StringIO

class PythonConsole(InteractiveConsole):

    def __init__(self, client, **kw):
        super(PythonConsole, self).__init__(**kw)
        self.client = client

    def runcode(self, code):
        out = StringIO()
        sys.stdout = out
        sys.stderr = out
        res = super(InteractiveConsole, self).runcode(code)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        self.write(out.getvalue())
        return res

    def write(self, data):
        self.client.send(data)


class Shell(object):

    kind = 'cloneable'

    def create(self):
        pass

    def set_player(self, player):
        self.player = player

    def prompt(self):
        self.client.send('>>> ')

    def handle_command(self, command):
        self.console.push(command.line)
        self.prompt()

    def exit_to_player(self):
        self.client.attach_anchor(self.player)

    def attach_client(self, client):
        console_locals = {
            'exit': self.exit_to_player,
        }
        console_locals.update(globals())
        self.console = PythonConsole(client, locals=console_locals)
        self.client = client
        self.client.send('loading shell...\n')
        self.prompt()
