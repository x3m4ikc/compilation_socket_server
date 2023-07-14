import socket
import subprocess
import threading
import unittest
from unittest.mock import patch

from client import Client
from server import Server


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(ip='127.0.0.1', port=1235)
        self.server = Server(ip='127.0.01', port=1235)
        self.server_thr = threading.Thread(target=self.server.start)
        self.server_thr.start()

    def tearDown(self):
        self.client.close_connection()
        self.server.server_socket.close()

    @patch('builtins.input', lambda *args: 'File hi.py')
    def test_send_1_file(self):
        self.client.connect()
        self.client.handle_command()

        self.server_thr.join()
        self.assertEqual(self.server.output, b"Hello, World!\n")


if __name__ == "__main__":
    unittest.main()
