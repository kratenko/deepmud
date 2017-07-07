import importlib.util
import os
import logging
import inspect
import posixpath

logger = logging.getLogger(__name__)


class MudlibClass(object):
    """
    Classes for creating objects in mudlib (ML-Class or mlclass).

    A mudlib class is a definition of a thing (room, monster, weapon, ...) inside
    the mudlib. They are defined by python files and deepmud files. Mudlib classes
    are dynamically loaded by the driver and stored in a Mudlib instance.
    Everything in the mud has one of this as a basis.
    """
    def __init__(self, *, mudlib, path):
        self.mudlib = mudlib
        self.path = path
        self.pyclass = None
        self.dmclass = None
        self.instance = None
        self.instances = []
        self.kind = None

    def create(self):
        """
        Create and return instance from a singleton class.

        Only works if this mudlib class is instanceable and singleton.
        :return: the instance
        """
        logger.info("Creating " + self.path)
        if self.kind != "singleton":
            raise AssertionError("Create called for class of kind %s", self.kind)
        ob = self.pyclass()
        ob._mlclass = self
        # TODO: dm-file
        ob.create()
        self.instance = ob
        return ob

    def clone(self):
        logger.info("Cloning " + self.path)
        if self.kind != "cloneable":
            raise AssertionError("Clone called for class of kind %s", self.kind)
        ob = self.pyclass()
        ob._mlclass = self
        # TODO: dm-file
        ob.create()
        self.instances.append(ob)
        return ob


class Mudlib(object):
    """
    Container for the complete mudlib.

    Loads, caches, and organises mudlib classes and the contained
    python classes.
    """
    def __init__(self, *, mudlib_path, world):
        self.world = world
        self.mudlib_path = os.path.abspath(mudlib_path)
        logger.info("Creating Mudlib with base: '%s'", self.mudlib_path)
        self.classes = {}
        self.build_globals()

    def normpath(self, path):
        """
        Return normalised mudlib path.
        """
        # use posixpath here, because mudlib paths should always use
        # slashes, not backslashes, no matter what os the driver is run on.
        return posixpath.normpath(path)

    def os_path(self, path):
        """
        Return full os path for mudlib path.
        Ensures that the absolute path is prefixed with the mudlib folder.

        >>> ml = Mudlib(mudlib_path="/test", None)
        >>> ml.os_path("../foo")
        AssertionError: Mudlib paths must be absolute for loading
        >>> ml.os.path("/../../foo")
        /test/foo
        """
        path = os.path.normpath(path)
        if not path.startswith('/'):
            raise AssertionError("Mudlib paths must be absolute for loading")
        return os.path.join(self.mudlib_path, path[1:])

    def build_globals(self):
        """
        Create dict to inject into python modules as globals.
        """
        self._globals = {}

        def mlclass(path):
            # TODO: relative paths
            return self.get_mlclass(path=path)
        self._globals['mlclass'] = mlclass

        def pyclass(path):
            return mlclass(path).pyclass
        self._globals['pyclass'] = pyclass

        def clone(path):
            return self.world.clone(path)
        self._globals['clone'] = clone

        # TODO: make it possible to extend this dictionary via the MUDlib

    def inject_globals_to_module(self, mod):
        """
        Insert global variables needed to execute module.
        :param mod: the loaded, unexecuted module
        """
        for k, v in self._globals.items():
            setattr(mod, k, v)

    def find_class_in_mod(self, mod):
        """
        Find and return the python class for mlclass from a loaded mod.

        Currently returns the first class with a name that matches the
        base name of the path to load.
        :param mod: loaded python mod
        :return: the python class to use
        """
        mod_name = mod.__name__
        cls_name = posixpath.split(mod_name)[-1]
        for k in dir(mod):
            v = getattr(mod, k)
            if inspect.isclass(v) and k.lower() == cls_name.lower():
                return v
        raise AssertionError("Could not find class in " + repr(mod))

    def load_pyclass(self, path):
        """
        Load and return python class from mudlib .py file.
        :param path: absolute mudlib path of class to load (without .py)
        :return: the python class of the .py file
        """
        # file path
        py_path = self.os_path(path) + '.py'
        # modname:
        mod_name = '#mudlib:' + os.path.normpath(path)
        #mod_name = '#mudlib' + os.path.normpath(path).replace("\\", ".").replace("/", ".")
        logger.debug("Loading PY-Class: %s as %s.", py_path, mod_name)
        spec = importlib.util.spec_from_file_location(mod_name, py_path)
        foo = importlib.util.module_from_spec(spec)
        self.inject_globals_to_module(foo)
        spec.loader.exec_module(foo)
        pyclass = self.find_class_in_mod(foo)
        pyclass._mlpath = path
        # add logger to class
        pyclass.logger = logging.getLogger(mod_name)
        return pyclass

    def load_mlclass(self, path):
        """
        Load and return the mudlib class for path.
        :param path: absolute mudlib path (without extensions)
        :return: object representing the mudlib class
        """
        logger.debug("Loading ML-Class: %s", path)
        try:
            pyclass = self.load_pyclass(path)
        except FileNotFoundError:
            pyclass = None
        dm_path = self.os_path(path) + '.dm'
        try:
            with open(dm_path, 'rt') as f:
                dm_text = f.read()
        except FileNotFoundError:
            dm_text = None
        if pyclass is None and dm_text is None:
            raise AssertionError("No ML-Class definition found in {}".format(path))
        mlc = MudlibClass(mudlib=self, path=path)
        mlc.pyclass = pyclass
        mlc.kind = pyclass.kind
        mlc.dm_text = dm_text
        self.classes[path] = mlc
        logger.info("ML-Class %s loaded.", path)
        return mlc

    def unload(self, path):
        """
        Unload the mudlib class so that invoking methods such as clone
        need to load the class again.
        :param path: absolute mudlib path (without extensions)
        """
        try:
            del self.classes[self.normpath(path)]
        except KeyError:
            pass

    def reload(self, path, recursive=True):
        """
        Unload and load the mudlib class for the given path recursively,
        i.e. every mudlib class this class depends on will be reloaded as well.
        :param path: absolute mudlib path (without extensions)
        :param recursive: turn recursive reloading on or off
        :return: object representing the mudlib class
        """
        path = self.normpath(path)
        if path not in self.classes:
            return self.get_mlclass(path=path)
        cls = self.get_mlclass(path=path)

        if recursive:
            for parent in cls.pyclass.__bases__:
                if hasattr(parent, '_mlpath'):
                    self.reload(parent._mlpath)

        self.unload(path)
        return self.get_mlclass(path=path)

    def get_mlclass(self, *, path):
        """
        Return mudlib class for given absolute path.

        Loads the class if necessary, caches class for further usage.
        :param path: Uniform, absolute path to the class (without extensions)
        :return: The mudlib class.
        """
        path = self.normpath(path)
        if path not in self.classes:
            self.classes[path] = self.load_mlclass(path)
        return self.classes[path]

    def get_instance(self, *, path):
        """
        Get the instance of a singleton class. Create if necessary.
        :param path: mudlib path to class
        :return: the instance
        """
        mlclass = self.get_mlclass(path=path)
        if mlclass.instance is None:
            return mlclass.create()
        else:
            return mlclass.instance

    def clone(self, path):
        mlclass = self.get_mlclass(path=path)
        return mlclass.clone()
