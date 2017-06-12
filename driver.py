import logging

from server import Server
from world import World

logger = logging.getLogger(__name__)


class Driver(object):
    def __init__(self):
        self.server = Server("localhost", 6339, driver=self)
        self.world = World(mudlib_path="mudlib")

    def get_client_anchor(self, client, name):
        player_ob = self.world.clone("/base/player")
        player_ob.setup_player(client, name)
        return player_ob

    def run(self):
        self.server.bind()
        self.server.listen()
        while True:
            self.server.handle_incoming()


def run():
    logging.basicConfig(level=logging.DEBUG)
    driver = Driver()
    driver.run()


if __name__ == "__main__":
    run()
