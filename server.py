import socket
import selectors
import time
import logging
import re

from world import Command

logger = logging.getLogger(__name__)


class ClientException(Exception):
    pass


class Client(object):
    """
    Object representing a connection to a player in the server.
    """
    def __init__(self, server, id, socket, addr):
        # client identification:
        self.server = server
        self.id = id
        self.socket = socket
        self.addr = addr
        self.fd = socket.fileno()
        # state:
        self.state = "init"
        # stats:
        self.sent = 0
        self.read = 0
        # timestamps:
        self.created = time.time()
        self.last_sent = self.created
        self.last_read = self.created
        #
        self.buffer = bytearray()
        self.name = None
        self.anchor = None

    def _handle_line(self, line):
        """
        Handle a single completed line received from socket.
        :param line:
        :return:
        """
        if self.state == 'ask_name':
            name = line.strip()
            if re.match(r"^\w{3,15}$", name) and not re.match(".*\d.*", name):
                self.name = name
                self.state = "game"
                # attach to game object:
                self.anchor = self.server.driver.get_client_anchor(self, name)
            else:
                self.send("Sorry, that's not valid. Names, for now, must be 3 to 15 letters.\nTry again, please: ")
        elif self.state == 'game':
            if self.anchor:
                command = Command(self, line)
                self.anchor.handle_command(command)
            else:
                raise ClientException("No anchor to handle your input.")

    def _handle_bytes(self, data):
        """
        Handle data that has been received from socket.

        Adds bytes to the internal data buffer. Scans buffer for completed lines and handles them.
        :param data:
        :return:
        """
        self.buffer.extend(data)
        if len(self.buffer) > 1024 * 16:
            # Line too long
            raise ClientException("Buffer overfilled. Send some newlines!")
        start = 0
        end = self.buffer.find(b"\n")
        last_end = -1
        while end >= 0:
            # extract line (handle both "\n" and "\r\n"):
            if end > start and self.buffer[end - 1] == b"\r"[0]:
                line = self.buffer[start:end - 1].decode("utf-8")
            else:
                line = self.buffer[start:end].decode("utf-8")
            self._handle_line(line)
            last_end = end
            # look further
            start = end + 1
            end = self.buffer.find(b"\n", start)
        # clear handled data from buffer:
        if last_end >= 0:
            self.buffer = self.buffer[last_end + 1:]

    def recv(self):
        """
        Handle a pending data receive on this client.
        """
        data = self.socket.recv(1024)
        # TODO: kick flooding clients
        if not data:
            # socket closed from other side, most likely:
            raise ClientException("Socket broke")
        self.last_read = time.time()
        self.read += len(data)
        self._handle_bytes(data)

    def send(self, data):
        """
        Send text or data to the client.
        :param data: unicode or string object containing data
        :return:
        """
        """
        :param data: 
        :return: 
        """
        if type(data) == str:
            data = data.encode("utf-8")
        sent = self.socket.send(data)
        self.last_sent = time.time()
        self.sent += sent

    def disconnect(self, reason=None):
        """
        Gracefully disconnect and remove client from server.
        :param reason: Text explaining disconnection to client
        :return:
        """
        self.server.disconnect(self, reason)

    def close(self):
        """
        Close the socket connecting this client.
        """
        self.socket.close()

    def __str__(self):
        return "<Client#{}, fd:{}, to:{}, r:{}, s:{}>".format(
            self.id, self.fd, self.addr,
            self.read, self.sent,
        )

    def welcome(self):
        """
        Actions performed after client has been connected.
        :return:
        """
        self.send("Welcome. We need to go deeper!\n\nChoose a name: ")
        self.state = "ask_name"


class Server(object):
    def __init__(self, host, port, driver):
        logger.info("Creating server.")
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.selector = selectors.DefaultSelector()
        self.clients = {}
        self.last_client_id = 0
        self.driver = driver

    def next_client_id(self):
        self.last_client_id += 1
        return self.last_client_id

    def bind(self):
        logger.info("Binding server to %s:%d", self.host, self.port)
        self.socket.bind((self.host, self.port))

    def listen(self):
        logger.info("Start listening.")
        self.socket.listen(5)
        # self.socket.setblocking(False)
        self.selector.register(self.socket, selectors.EVENT_READ, (0, self.accept))

    def accept(self, _, key):
        """
        Callback for accepting a new connection.
        :param _: dummy
        :param key: key from selector
        :return: nothing
        """
        conn, addr = self.socket.accept()
        conn.setblocking(False)
        client_id = self.next_client_id()
        logger.info("Accepting #%d: %s from %s" % (client_id, conn, addr))
        self.selector.register(conn, selectors.EVENT_READ, (client_id, self.recv))
        client = Client(self, client_id, conn, addr)
        self.clients[client_id] = client
        # start greet - login - whatever:
        client.welcome()

    def disconnect(self, client, reason):
        """
        Close and remove connected client.

        Sends reason for closing to client, close socket, remove client from server.
        :param client: the client to close
        :param reason: text message explaining closing to client
        :return:
        """
        logger.info("Disconnecting client %s, reason: %s", client, reason)
        self.selector.unregister(client.fd)
        del self.clients[client.id]
        client.send("Closing connection: " + reason + "\n")
        client.close()

    def recv(self, client_id, key):
        """
        Callback for receiving data from client.

        Receives bytes and starts handling process in client. If client has an error or closes normally, an exception
        is raised.
        :param client_id: internal client id
        :param key: the key returned by selector
        :return: nothing
        """
        client = self.clients[client_id]
        try:
            client.recv()
        except ClientException as e:
            self.disconnect(client, e.args[0])

    def handle_incoming(self, timeout=None):
        """
        Handle pending incoming data.

        Handle incoming and errors on all monitored sockets. This means new connections on the server socket as well
        as incoming data on the clients' sockets. It will handle incomings on all sockets, but not necessarily all
        pendings on that socket.
        :param timeout:
        :return:
        """
        events = self.selector.select(timeout=timeout)
        for key, mask in events:
            client_id, callback = key.data
            callback(client_id, key)
