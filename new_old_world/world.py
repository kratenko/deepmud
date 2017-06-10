import importlib.util
import os
import logging

logger = logging.getLogger(__name__)


class MudLibClass(object):
    def __init__(self, *, mudlib, path):
        self.path = path
        self.mudlib = mudlib
        self.pyclass = None
        self.dm = None
        self.last_instance_id = 0
        self.singleton = False
        self.instances = []

    def clone(self):
        # TODO: later
        if self.singleton:
            raise AssertionError("ML-Class not cloneable.")
        ob = self.pyclass()
        ob._mlclass = self
        self.last_instance_id += 1
        ob._instance_id = self.last_instance_id
        self.instances.append(ob)
        logger.info("Cloned " + ob.identifier())
        return ob

    def create(self):
        logger.info("Creating " + self.path)
        ob = self.pyclass()
        ob._mlclass = self
        ob.create()
        return ob


class MudLib(object):
    def __init__(self, *, mudlib_path):
        # absolute path of mudlib directory:
        self.mudlib_path = os.path.abspath(mudlib_path)
        logger.info("Creating MudLib at '%s'" % self.mudlib_path)
        # dict to store loaded mlclasses:
        self.mlclasses = {}
        self.pyclasses = {}
        self._build_globals()

    def _build_globals(self):
        self._globals = {}
        def mlclass(s):
            return object
        def pyclass(path):
            return object
        self._globals['mlclass'] = mlclass
        self._globals['pyclass'] = pyclass

    def full_path(self, path):
        path = os.path.normpath(path)
        if not path.startswith('/'):
            raise AssertionError("Mudlib paths must be absolute for loading")
        return os.path.join(self.mudlib_path, path[1:])

    def load_pyclass(self, path):
        # file path
        py_path = self.full_path(path) + '.py'
        # modname:
        mod_name = os.path.normpath(path).replace("\\", ".").replace("//", ".")
        print(mod_name, py_path)
        spec = importlib.util.spec_from_file_location(mod_name, py_path)
        foo = importlib.util.module_from_spec(spec)
        print(foo)
        self.inject_globals_to_module(foo)
        spec.loader.exec_module(foo)
        key = None
        print(dir(foo))
        for k in dir(foo):
            if not k.startswith("_"):
                key = k
                break
        pyclass = getattr(foo, k)
        pyclass._mlpath = path
        return pyclass

    def load_mlclass(self, path):
        logger.info("Loading ML-Class: %s", path)
        try:
            pyclass = self.load_pyclass(path)
        except FileNotFoundError:
            pyclass = None
        dm_path = self.full_path(path) + '.dm'
        try:
            with open(dm_path, 'rt') as f:
                dm_text = f.read()
        except FileNotFoundError:
            dm_text = None
        if pyclass is None and dm_text is None:
            raise AssertionError("No ML-Class definition found")
        mlc = MudLibClass(mudlib=self, path=path)
        mlc.pyclass = pyclass
        mlc.dm_text = dm_text
        self.mlclasses[path] = mlc
        return mlc

    def get_mlclass(self, path):
        if path in self.mlclasses:
            return self.mlclasses[path]
        else:
            return self.load_mlclass(path)

    def inject_globals_to_module(self, mod):
        for k, v in self._globals.items():
            setattr(mod, k, v)

    def create(self, path):
        mlclass = self.get_mlclass(path)
        return mlclass.create()


class World(object):
    def __init__(self, *, mudlib_path):
        self.mudlib_path = os.path.normpath(mudlib_path)


logging.basicConfig(level=logging.INFO)
mudlib = MudLib(mudlib_path="../mudlib")
r1 = mudlib.create("/base/item")
print(r1.__class__._mlpath)
exit()

I = mudlib.load_pyclass("/base/itemi")
print(I)
i = I();
print(i.test_me())

exit()
world = World(mudlib_path="../mudlib")
R = world.load_class("/base/room")
print(R)
r = R()
r.doit()
r.gotit()

