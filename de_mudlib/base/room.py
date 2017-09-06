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
        abs_path = self._mlclass.relative_path(destination)
        self.exits[direction] = abs_path

    def _move_through_exit(self, whom, direction):
        destination_path = self.exits[direction]
        try:
            destination = single(destination_path)
        except Exception as e:
            return "Ups! Da ist wohl was schief gelaufen: " + str(e)
        whom.move(to=destination)
        whom._schau_umgebung()
        return True


    def try_command(self, supplier, command):
        cmd = command.command.lower()
        is_standard = False
        if cmd in STANDARD_DIRECTIONS_LOOKUP:
            cmd = STANDARD_DIRECTIONS_LOOKUP[cmd]
            is_standard = True
        if cmd in self.exits:
            return self._move_through_exit(command.actor, cmd)
        if is_standard:
            return "Da geht's nicht weiter."
        return super().try_command(supplier, command)

    def get_description(self, context: dict):
        desc = super().get_description(context).copy()
        if self.exits:
            exit_list = ", ".join(self.exits.keys())
            desc['long'] += ("\n  Ausgänge: " + exit_list + "\n")
        if self.contents:
            viewer = context['spieler']
            items = []
            for item in self.contents:
                if item is viewer:
                    # nicht selbst auflisten:
                    continue
                items.append(item.get_description(context)['short'])
            if items:
                desc['long'] += "Du siehst hier:\n  " + "\n  ".join(items) + "\n"
        return desc

