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
        self.intro()
        self.action_look("")
        while self.looping:
            cmd = self.input()
            self.action(cmd)

    def intro(self):
        hi = """Hallo,
willkommen im Deep MUD dev viewer. Viel geht hier nicht, aber sieh dich ruhig
um. Der wichtigste Befehl ist "betrachte" (oder "b") um dich umzuschauen.
Bewegen kannst du dich mit dem Namen der Ausgänge, also z.B. "osten", "runter"
oder verkürzt "n", "nw", "r", etc.
Wenn du keine Lust mehr hast, kommst du mit "ende" hier raus.
"""
        self.out(hi)

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

    def action_move(self, cmd):
        if self.environment:
            if cmd in self.environment.exits:
                ex = self.environment.exits[cmd]
                dest = self.rooms.get_room(ex.path)
                self.environment = dest
                self.action_look("")
            else:
                self.out("Da geht es nicht weiter.")
        else:
            self.out("Du bist nirgends, da kannst du auch nicht weg.")

rooms = room.RoomTable()
r1 = rooms.get_room("/am_fluss/ufer")
viewer = Viewer(rooms=rooms)
viewer.environment = r1
viewer.loop()
exit()

starting_room = room.Room("/start")
starting_room.short = "Am Anfang"
starting_room.long = "Du bist dort, wo alles anfängt."
starting_room.add_exit("osten", "/zwei")
starting_room.add_exit("norden", "/am_fluss/ufer")
rooms.insert_room(starting_room)

room2 = room.Room("/zwei")
room2.short = "Daneben"
room2.long = "Hier gehts weiter"
room2.add_exit("westen", "/start")
rooms.insert_room(room2)
