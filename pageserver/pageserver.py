__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

import os

"""
  A trivial web server in Python.

  Based largely on https://docs.python.org/3.9/howto/sockets.html
  This trivial implementation is not robust: We have omitted decent
  error handling and many other things to keep the illustration as simple
  as possible.
"""

import config  # Configure from .ini files and command line
import logging  # Better than print statements
import socket  # Basic TCP/IP communication on the internet
import _thread  # Response computation runs concurrently with main program
from typing import Callable

# Starter version only serves cat pictures.
CAT = """
     ^ ^
   =(   )=
"""

# HTTP response codes, as the strings we will actually send.
# See:  https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
# or    https://www.rfc-editor.org/rfc/rfc9110.html
STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"

# set up logger
for handler in logging.root.handlers[:]:  # make sure all handlers are removed
    logging.root.removeHandler(handler)

logging_level = logging.DEBUG
logging_format = logging.Formatter('%(asctime)s: %(levelname)s [%(name)s:%(funcName)s:%(lineno)d] - %(message)s')
logging.root.setLevel(logging_level)
h = logging.StreamHandler()
h.setFormatter(logging_format)
logging.root.addHandler(h)

log = logging.getLogger(__name__)


def listen(port_num: int):
    """
    Create and listen to a server socket.
    Args:
       port_num: Integer in range 1024-65535; temporary use ports
           should be in range 49152-65535.
    Returns:
       A server socket, unless connection fails (e.g., because
       the port is already in use).
    """

    # Internet, streaming socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to port and make accessible from anywhere that has our IP address
    server_socket.bind(('', port_num))
    server_socket.listen(1)  # A real server would have multiple listeners
    return server_socket


def serve(sock: socket, func: Callable):
    """
    Respond to connections on sock.
    Args:
       sock:  A server socket, already listening on some port.
       func:  a function that takes a client socket and does something with it
    Returns: nothing
    Effects:
        For each connection, func is called on a client socket connected
        to the connected client, running concurrently in its own thread.
    """
    while True:
        log.info(f"Attempting to accept a connection on {sock}")
        (client_socket, address) = sock.accept()
        _thread.start_new_thread(func, (client_socket,))


def respond(sock: socket):
    """
    Updated server response based on requirements.
    """
    request = sock.recv(1024)  # We accept only short requests
    request = str(request, encoding='utf-8', errors='strict')
    log.info("--- Received request ----")
    log.info(f"Request was {request}\n***\n")

    parts = request.split()

    # Check if it's a GET request
    if len(parts) > 1 and parts[0] == "GET":

        # Extracting the path from the request
        path = parts[1]

        # Check forbidden patterns
        forbidden_patterns = ['~', '//', '..']
        if any(pattern in path for pattern in forbidden_patterns):
            transmit(STATUS_FORBIDDEN, sock)
            transmit("Forbidden path detected.", sock)
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            return

        # Check if path ends with .html or .css
        if path.endswith(".html") or path.endswith(".css"):
            file_path = os.path.join("..", "pages", path[1:])  # Adjusting for the directory structure
            # Try to read the file
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    transmit(STATUS_OK, sock)
                    transmit(content, sock)
            except FileNotFoundError:
                transmit(STATUS_NOT_FOUND, sock)
                transmit("File not found.", sock)
        else:
            log.info(f"Unhandled request: {request}")
            transmit(STATUS_NOT_IMPLEMENTED, sock)
            transmit(f"\nI don't handle this request: {request}\n", sock)

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


def transmit(msg: str, sock: socket):
    """It might take several sends to get the whole message out"""
    sent = 0
    while sent < len(msg):
        buff = bytes(msg[sent:], encoding="utf-8")
        sent += sock.send(buff)


# Run from command line
def get_options():
    """
    Options from command line or configuration file.
    Returns namespace object with option value for port
    """

    # Defaults from configuration files; on conflict, the last value read has precedence
    # We want: PORT and DOCROOT
    options = config.configuration()

    if options.PORT <= 1000:
        log.warning(f"Port {options.port} selected. Ports 0..1000 are reserved by the operating system!")
    return options


def main():
    options = get_options()
    port = options.PORT
    if options.DEBUG:
        log.setLevel(logging.DEBUG)

    sock = listen(port)
    log.info(f"Listening on port {port}")
    log.info(f"Socket is {sock}")
    serve(sock, respond)


if __name__ == "__main__":
    main()
