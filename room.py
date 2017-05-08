from collections import OrderedDict
import os

class Exit(object):
    COMMONS = {
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
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.aliases = [name]
        self.common_aliases()

    def common_aliases(self):
        if self.name in self.COMMONS:
            self.aliases.extend(COMMONS[name])
        if self.name == "norden":
            self.aliases.extend("nord", "n")
        elif self.name ==

class Room(object):
    def __init__(self, path):
        self.path = path
        self.exits = []
        self.senses = []
        self.name = None
        self.long = None
        self.short = None
        self.content = []
        self.vitems = []

    def get_long(self):
        return self.long

    def get_short(self):
        return self.short

    def __repr__(self):
        return "<Room:\"{}\">".format(self.path)


class RoomTable(object):
    def __init__(self):
        self.rooms = {}

    def get_room(self, path):
        if path in self.rooms:
            return self.rooms[path]
        else:
            return self.load_room(path)

    def load_room(self, path):
        if path == '/void':
            room = self.create_void()
        else:
            raise Exception("Not yet.")
        self.rooms[path] = room
        return room

    def create_void(self):
        void = Room("/void")
        void.name = "nichts"
        void.description = "Hier ist nichts."
        void.short = "Im Nichts"
        void.exits = []
        return void

    def load_dm(self, path):
        p = os.path.join("data", path) + '.dm'
        with open(p, "rt") as f:
            s = f.read()



class Viewer(object):
    def __init__(self):
        self.environment = None

    def action(self, cmd):
        pass


rooms = RoomTable()
void = rooms.get_room('/void')
print(void)
