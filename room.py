from collections import OrderedDict
import os

import dml

class Exit(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path

class Sense(object):
    def __init__(self, parent, channel=None):
        self.parent = parent
        self.channel = channel
        self.text = None
        self.message = None

    def from_dm(self, property):
        self.channel = property.argument
        self.text = property.text()
        msg = property.find_property('message')
        if msg:
            self.message = msg.text()

class VItem(object):
    def __init__(self, item, parent=None):
        self.item = item
        self.parent = parent
        self.long = None
        self.short = None
        self.name = None
        self.alias = []
        self.senses = {}


class Room(object):
    def __init__(self, path):
        self.path = path
        self.exits = OrderedDict()
        self.senses = {}
        self.name = None
        self.long = None
        self.short = None
        self.content = []
        self.vitems = []

    def get_long(self):
        return self.long

    def get_short(self):
        return self.short

    def _relative_path(self, path):
        if path.startswith("/"):
            # is absolute path, this object's path irrelevant
            return os.path.normpath(path)
        else:
            # relative path:
            self_dir = os.path.dirname(self.path)
            return os.path.normpath(os.path.join(self_dir, path))

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
        #doc = parser.parse_document(text)
        doc = dml.Document()
        doc.parse(text)
        self.dm_description(doc)
        self.dm_exits(doc)

    def dm_description(self, doc):
        """
        Find and evaluate the general room description.
        """
        if doc.main_section:
            s1 = doc.main_section
            self.long = s1.text()
            self.short = s1.title
            self.dm_vitems(s1)
            for sense_def in doc.main_section.find_properties('sense'):
                sense = Sense(self)
                sense.from_dm(sense_def)
                if sense.channel not in self.senses:
                    self.senses[sense.channel] = sense

    def dm_exits(self, doc):
        """
        Find and evaluate exit definitions.
        """
        for sec in doc.sections:
            if sec.title == ":exits":
                for ex_def in sec.sections:
                    self.dm_exit(ex_def)

    def dm_exit(self, ex_def):
        """
        Evaluate a single exit definition.
        """
        parts = ex_def.title.split(":", 1)
        if len(parts) == 2:
            direction = parts[0].strip()
            path = self._relative_path(parts[1].strip())
            self.add_exit(direction, path)

    def dm_vitems(self, main_sec):
        for sec in main_sec.sections:
            self.dm_vitem(sec, None)

    def dm_vitem(self, sec, parent):
        vitem = VItem(self, parent)
        vitem.long = sec.text()
        name = sec.title.lower()
        vitem.name = name
        vitem.aliases = [name]
        alias_def = sec.find_property('alias')
        if alias_def:
            al = [a.strip() for a in alias_def.text().split(",")]
            vitem.aliases.extend(al)
        for sense_def in sec.find_properties('sense'):
            sense = Sense(vitem)
            sense.from_dm(sense_def)
            if sense.channel not in vitem.senses:
                vitem.senses[sense.channel] = sense
        self.vitems.append(vitem)

    def find(self, what):
        for v in self.vitems:
            if what in v.aliases:
                return v
        return None

class RoomTable(object):
    def __init__(self):
        self.rooms = {}
        self.base_dir = "data"

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
        p = os.path.join(self.base_dir, path[1:]) + '.dm'
        #p = "data" + path + '.dm'
        #p = os.path.join("data", path) + '.dm'
        # print("P", p)
        with open(p, "rt") as f:
            r.from_dm(f.read())
        return r
