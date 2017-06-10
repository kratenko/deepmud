import logging
from world import World

logging.basicConfig(level=logging.DEBUG)

world = World(mudlib_path="mudlib")
sr = world.get_singleton(path="/stuff/startroom")
r2 = world.get_singleton(path="/stuff/secondroom")

print(sr.description, sr.exits)