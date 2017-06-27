#!/usr/bin/env python
import logging
import configargparse

from server import Server
from world import World

logger = logging.getLogger(__name__)


def config():
    parser = configargparse.ArgParser(description='MUDs need to go deeper.')
    parser.add('-c', '--config', is_config_file=True, help="config file path", default="mud.ini")
    parser.add('-p', '--port', default=6339, help="port driver listens on")
    parser.add('-H', '--host', default="localhost", help="host/ip to bind driver to")
    parser.add('-l', '--mudlib', default="mudlib", help="path to mudlib")
    options = parser.parse_args()
    return options


class Driver(object):
    def __init__(self, options):
        # store config values:
        self.options = options
        self.host = options.host
        self.port = int(options.port)
        self.mudlib_path = options.mudlib
        # create the server object:
        self.server = Server(
            host=self.host,
            port=self.port,
            driver=self,
        )
        # create the world (contains the mudlib):
        self.world = World(
            mudlib_path=self.mudlib_path,
        )

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
    options = config()
    driver = Driver(options)
    driver.run()


if __name__ == "__main__":
    run()
