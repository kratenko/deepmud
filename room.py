from collections import OrderedDict
import os

import parser

class Exit(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

class VItem(object):
    def __init__(self, item, parent=None):
        self.item = item
        self.parent = parent
        self.long = None
        self.short = None
        self.name = None
        self.alias = []

class Room(object):
    def __init__(self, path):
        self.path = path
        self.exits = OrderedDict()
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

    def add_exit(self, name, path):
        self.exits[name] = Exit(name, path)

    def exit_list(self):
        if self.exits:
            l = ", ".join([ex for ex in self.exits.keys()])
            return "    weiter: " + l
        else:
            return None

    def __repr__(self):
        return "<Room:\"{}\">".format(self.path)

    def from_dm(self, text):
        """
        Evaluate text of a dm-source for this room.
        """
        doc = parser.parse_document(text)
        self.dm_description(doc)
        self.dm_exits(doc)

    def dm_description(self, doc):
        """
        Find and evaluate the general room description.
        """
        if doc.sections:
            s1 = doc.sections[0]
            self.long = s1.text()
            self.short = s1.heading
            self.dm_vitems(s1)

    def dm_exits(self, doc):
        """
        Find and evaluate exit definitions.
        """
        for sec in doc.sections:
            if sec.heading == ":exits":
                for ex_def in sec.sections:
                    self.dm_exit(ex_def)

    def dm_exit(self, ex_def):
        """
        Evaluate a single exit definition.
        """
        parts = ex_def.heading.split(":", 1)
        if len(parts) == 2:
            self.add_exit(parts[0].strip(), parts[1].strip())

    def dm_vitems(self, main_sec):
        for sec in main_sec.sections:
            self.dm_vitem(sec, None)

    def dm_vitem(self, sec, parent):
        vitem = VItem(self, parent)
        vitem.long = sec.text()
        name = sec.heading.lower()
        vitem.name = name
        vitem.aliases = [name]
        for p in sec.properties:
            if p.heading == 'alias':
                al = [a.strip() for a in p.text().split(",")]
                vitem.aliases.extend(al)
                break
        self.vitems.append(vitem)

    def find(self, what):
        for v in self.vitems:
            if what in v.aliases:
                return v
        return None

class RoomTable(object):
    def __init__(self):
        self.rooms = {}

    def get_room(self, path):
        if path in self.rooms:
            return self.rooms[path]
        else:
            return self.load_room(path)

    def insert_room(self, room):
        self.rooms[room.path] = room

    def load_room(self, path):
        if path == '/void':
            room = self.create_void()
        else:
            room = self.load_dm(path)
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
        r = Room(path)
        p = "data" + path + '.dm'
        #p = os.path.join("data", path) + '.dm'
        # print("P", p)
        with open(p, "rt") as f:
            r.from_dm(f.read())
        return r

    def dm_exits(self, room, doc):
        pass
