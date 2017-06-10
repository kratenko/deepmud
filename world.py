import logging

import mudlib

logger = logging.getLogger(__name__)

class World(object):
    def __init__(self, *, mudlib_path):
        logger.info("Creating world.")
        self.mudlib_path = mudlib_path
        self.mudlib = mudlib.Mudlib(mudlib_path=mudlib_path, world=self)
        self.last_item_id = 0
        self.singletons = {}

    def next_item_id(self):
        self.last_item_id += 1
        return self.last_item_id

    def get_singleton(self, *, path):
        path = self.mudlib.normpath(path)
        if path in self.singletons:
            return self.singletons[path]
        else:
            item = self.mudlib.get_instance(path=path)
            item._id = self.next_item_id()
            self.singletons[path] = item
            return item
