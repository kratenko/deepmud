import importlib.util
import os


def mlclass(path):
    return object


def load_class(path):
    base_path = "/home/kratenko/PycharmProjects/deepmud/old_world"
    p = os.path.join(base_path, path) + '.py'
    spec = importlib.util.spec_from_file_location("MUDLIB.name", p)
    foo = importlib.util.module_from_spec(spec)
    foo.mlclass = mlclass
    foo.theone = 16
    spec.loader.exec_module(foo)
    key = None
    print(dir(foo))
    for k in dir(foo):
        if not k.startswith("__"):
            key = k
            break
    return getattr(foo, k)


cl = load_class("base/room")
print(cl)
r = cl()
r.doit()
r.gotit()


class Nature(object):
    def __init__(self, *, world, path):
        self.world = world
        self.path = path
        self.methods = {}
        self.cloneable = False

    def call_method(self, item, method, *args, **kwargs):
        return self.methods[method](*args, **kwargs)


class Item(object):
    def __init__(self, *, id=None, nature=None):
        self.id = id
        self.nature = None
        self.environment = None
        self.contents = None
        self.values = {}


class Container(Item):
    def is_container(self):
        return self.contents is not None

    def insert(self, item):
        """
        Insert another item into this item.
        """
        # only containers may contain other items:
        if self.contents is None:
            raise AssertionError("Not a container")
        # check if self is contained within item:
        env = self.environment
        while env:
            if env == item:
                raise AssertionError("No cycles allowed in containment")
            env = env.environment
        # TODO: guards, etc.
        # insert object:
        self.contents.append(item)
        item.environment = self

    def remove(self, item):
        """
        Remove another item from this item.
        """
        if item.environment != self:
            raise AssertionError("Cannot remove item from this, this is not its environment")
        if item not in self.contents:
            raise AssertionError("Cannot remove item from this, it's not in here")
        self.contents.remove(item)
        item.environment = None


class World(object):
    def __init__(self):
        self.natures = {}
        self.items = {}
        self.last_item_id = 0

    def next_item_id(self):
        self.last_item_id += 1
        return self.last_item_id

    def load_nature(self, path):
        pass

    def get_nature(self, path):
        if path not in self.natures:
            self.load_nature(path)
        return self.natures[path]

    def create_item(self, path):
        nature = self.get_nature(path)
        if nature.cloneable:
            raise AssertionError("Cannot create cloneable")
        item = Item(id=self.next_item_id(), nature=nature)

    def clone_item(self, path):
        nature = self.get_nature(path)
        if not nature.cloneable:
            raise AssertionError("Cannot clone singleton")
