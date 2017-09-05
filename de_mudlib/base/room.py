import logging
import collections

logger = logging.getLogger(__name__)


def build_lookup(d):
    lookup =  {}
    for clear, short_list in d.items():
        for short in short_list:
            lookup[short] = clear
    return lookup

STANDARD_DIRECTION_DEFINITIONS = {
    'norden': ['norden', 'nord', 'n'],
    'nordosten': ['nordosten', 'nordost', 'no'],
    'osten': ['osten', 'ost', 'o'],
    'suedosten': ['suedosten', 'südosten', 'suedost', 'südost', 'so'],
    'sueden': ['sueden', 'süden', 'sued', 'süd', 's'],
    'suedwesten': ['suedwesten', 'südwesten', 'suedwest', 'südwest', 'sw'],
    'westen': ['westen', 'west', 'w'],
    'nordwesten': ['nordwesten', 'nordwest', 'nw'],
    'hoch': ['hoch', 'rauf', 'hinauf', 'h'],
    'runter': ['runter', 'hinab', 'r'],
}
STANDARD_DIRECTIONS = STANDARD_DIRECTION_DEFINITIONS.keys()
STANDARD_DIRECTIONS_LOOKUP = build_lookup(STANDARD_DIRECTION_DEFINITIONS)


class Room(pyclass("/base/container")):

    def __init__(self):
        super().__init__()
        self.exits = collections.OrderedDict()

    def add_exit(self, direction, destination):
        self.exits[direction] = destination

    def try_command(self, supplier, command):
        cmd = command.command.lower()
        is_standard = False
        if cmd in STANDARD_DIRECTIONS_LOOKUP:
            cmd = STANDARD_DIRECTIONS_LOOKUP[cmd]
            is_standard = True
        if cmd in self.exits:
            return "Let's try"
        if is_standard:
            return "Da geht's nicht weiter."
        return super().try_command(supplier, command)

    def get_description(self, context: dict):
        desc = super().get_description(context)
        if self.exits:
            exit_list = ",".join(self.exits.keys())
            desc['long'] += ("\n  Ausgänge: " + exit_list)
        return desc

