import logging
import re

import mudlib

logger = logging.getLogger(__name__)

space_matcher = re.compile(r"\s+")


class World(object):
    """
    The world containing everything in the mud.
    """
    def __init__(self, *, mudlib_path):
        logger.info("Creating world.")
        self.mudlib_path = mudlib_path
        self.mudlib = mudlib.Mudlib(mudlib_path=mudlib_path, world=self)
        self.last_item_id = 0
        self.singletons = {}
        self.clones = {}
        self.items = {}

    def next_item_id(self):
        self.last_item_id += 1
        return self.last_item_id

    def get_singleton(self, path):
        """
        Get instance of a singleton mudlib object.

        Returns the instance of a mudlib class that can be instantiated only once. Loads
        the class and creates the object if necessary, but returns the existing instance, if there is any.
        :param path:
        :return:
        """
        path = self.mudlib.normpath(path)
        if path in self.singletons:
            return self.singletons[path]
        else:
            item = self.mudlib.get_instance(path=path)
            item._id = self.next_item_id()
            self.singletons[path] = item
            self.items[item._id] = item
            return item

    def clone(self, path):
        """
        Get new instance of mudlib class.

        Creates a new instance of the given class and returns it. Loads the class if necessary.
        :param path:
        :return:
        """
        path = self.mudlib.normpath(path)
        item = self.mudlib.clone(path=path)
        item._id = self.next_item_id()
        if path not in self.clones:
            self.clones[path] = []
        self.clones[path].append(item)
        self.items[item._id] = item
        return item


class Command(object):
    """
    A command sent by a player to be executed in mud world.
    """
    def __init__(self, actor, line):
        self.supplier = None
        self.actor = actor
        self.line = line
        parts = space_matcher.split(line, 1)
        if len(parts) == 1:
            command, arg_line = parts[0], ""
        else:
            command, arg_line = parts
        if arg_line:
            args = space_matcher.split(arg_line)
        else:
            args = []
        # store in self:
        self.command = command
        self.arg_line = arg_line
        self.args = args
        #
        self.target = False

    def get_target(self):
        if self.target is False:
            self.target = self._find_target()
        return self.target

    def _find_target(self):
        # TODO: also - das hier kann noch so gut wie gar nichts...
        if self.args:
            target_name = self.args[0].lower()
            if target_name in ['ich', 'mich']:
                return self.actor
            if self.actor.environment:
                t = self.actor.environment.find(target_name)
                if t:
                    return t
            return self.actor.find(target_name)
        else:
            return None
