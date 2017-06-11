import logging
from world import World

logging.basicConfig(level=logging.DEBUG)

world = World(mudlib_path="mudlib")
sr = world.get_singleton(path="/stuff/startroom")
r2 = world.get_singleton(path="/stuff/secondroom")
print(sr.description, sr.exits)
exit()
f1 = world.clone(path="/stuff/flower")
f2 = world.clone(path="/stuff/flower")
print(f1.description, f2.description)
print(f1, f2)
