import room
import textwrap

std_exits = {
    "norden", "nordosten", "osten", "südosten",
    "süden", "südwesten", "westen", "nordweseten",
    "hoch", "runter",
}
alias_def = {
        "norden": ("nord", "n"),
        "nordosten": ("nordost", "no"),
        "osten": ("ost", "o"),
        "südosten": ("südost", "so", "suedosten", "suedost"),
        "süden": ("süd", "s", "sued"),
        "südwesten": ("südwest", "sw", "suedwesten", "suedwest"),
        "westen": ("west", "w"),
        "nordwesten": ("nordwest", "nw"),
        "hoch": ("rauf", "hinhauf", "herauf", "aufwaerts", "aufwärts", "h"),
        "runter": ("hinunter", "herunter", "herab", "abwärts", "abwaerts", "r"),
}
aliases = {}
for cmd, al in alias_def.items():
    for alias in al:
        if alias not in aliases:
            aliases[alias] = cmd

class Viewer(object):
    def __init__(self, rooms=None):
        self.environment = None
        self.rooms = rooms

    def out(self, text):
        if text is None:
            return
        lines = []
        for parts in text.split("\n"):
            lines.extend(textwrap.wrap(parts, 79))
        print("\n".join(lines))

    def input(self):
        return input().lstrip()

    def loop(self):
        self.looping = True
        while self.looping:
            cmd = self.input()
            self.action(cmd)

    def intro(self):
        hi = """Hallo,
willkommen im Deep MUD dev viewer. Viel geht hier nicht, aber sieh dich ruhig
um. Der wichtigste Befehl ist "betrachte" (oder "b") um dich umzuschauen.
Bewegen kannst du dich mit den Namen der Ausgänge, also z.B. "osten", "runter"
oder verkürzt "n", "nw", "r", etc.
Mit "rieche", "lausche" und "fühle" kannst du noch mehr erfahren.
Wenn du keine Lust mehr hast, kommst du mit "ende" hier raus.
"""
        self.out("\n")
        self.out("\n")
        self.out(hi)
        self.out("\n")

    def action(self, line):
        if " " in line:
            cmd, parm_line = line.split(" ", 1)
        else:
            cmd, parm_line = line, ""
        # check for aliases
        if cmd in aliases:
            cmd = aliases[cmd]
        if cmd == "":
            pass
        elif cmd == 'b' or cmd == 'betrachte':
            self.action_look(parm_line)
        elif cmd in ['ende', 'exit', 'quit']:
            self.out("Bis bald!")
            self.looping = False
        elif cmd in std_exits:
            self.action_move(cmd)
        elif cmd in ['riech', 'rieche']:
            self.action_rieche(parm_line)
        elif cmd in ['lausch', 'lausche', 'hoer', 'hoere', 'hör', 'höre']:
            self.action_lausche(parm_line)
        elif cmd in ['tast', 'taste', 'fühl', 'fühle', 'fuehl', 'fuehle']:
            self.action_taste(parm_line)
        else:
            self.out("Wie bitte?")

    def action_look(self, line):
        if self.environment:
            if line:
                ob = self.environment.find(line)
                if ob:
                    self.out(ob.long)
                else:
                    self.out(line + " nicht gefunden.")
            else:
                self.out(self.environment.long)
                self.out(self.environment.exit_list())
        else:
            self.out("Whoops! Du bist nirgends. Nix zu sehen...")

    def action_rieche(self, what):
        sense = self.find_sense("geruch", what)
        if sense is None:
            self.out(what + " nicht gefunden")
        elif sense is False:
            self.out("Du riechst nichts.")
        else:
            self.out(sense.text)

    def action_taste(self, what):
        sense = self.find_sense("gefühl", what)
        if sense is None:
            self.out(what + " nicht gefunden")
        elif sense is False:
            self.out("Du fühlst nichts.")
        else:
            self.out(sense.text)

    def action_lausche(self, what):
        sense = self.find_sense("geräusch", what)
        if sense is None:
            self.out(what + " nicht gefunden")
        elif sense is False:
            self.out("Du hörst nichts.")
        else:
            self.out(sense.text)

    def find_sense(self, channel, what):
        if what:
            ob = self.environment.find(what)
        else:
            ob = self.environment
        if ob:
            if channel in ob.senses:
                return ob.senses[channel]
            else:
                return False
        else:
            return None

    def action_move(self, cmd):
        if self.environment:
            if cmd in self.environment.exits:
                ex = self.environment.exits[cmd]
                try:
                    dest = self.rooms.get_room(ex.path)
                except Exception as ex:
                    self.out("Whoops! Da ist was schief gelaufen...")
                    self.out("["+ex.__str__()+"]")
                    return
                self.enter_room(dest)
            else:
                self.out("Da geht es nicht weiter.")
        else:
            self.out("Du bist nirgends, da kannst du auch nicht weg.")

    def enter_room(self, room):
        self.environment = room
        self.out("[" + room.path + "]")
        self.action_look("")

rooms = room.RoomTable()
r1 = rooms.get_room("/kreuzung/kreuzung")
viewer = Viewer(rooms=rooms)
viewer.intro()
viewer.enter_room(r1)
viewer.loop()
