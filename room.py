from collections import OrderedDict
import os

import parser

class Exit(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path


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
        doc = parser.load_document(p)
        s1 = doc.sections[0]
        r.long = s1.text()
        return r
