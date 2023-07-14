import multiprocessing
import unittest
from unittest.mock import patch

from client import Client
from server import Server


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(ip='127.0.0.1', port=1235)
        self.server = Server(ip='127.0.0.1', port=1235)
        self.server_process = multiprocessing.Process(target=self.server.start)
        self.server_process.start()

    def tearDown(self):
        self.client.close_connection()
        self.server.server_socket.close()

    @patch('builtins.input', lambda *args: 'File hi.py')
    def test_send_1_file(self):
        self.client.connect()
        self.client.handle_command()
        self.server_process.terminate()

    # @patch('builtins.input', lambda *args: 'File hello.py')
    # @patch('builtins.input', lambda *args: 'File hi.py')
    # @patch('builtins.input', lambda *args: 'Number 2')
    # def test_send_2_files(self):
    #     self.client.connect()
    #     self.client.handle_command()
    #
    #     self.server_process.terminate()
    #
    # @patch('builtins.input', lambda *args: 'File hello.py')
    # @patch('builtins.input', lambda *args: 'File hi.py')
    # @patch('builtins.input', lambda *args: 'Number 2')
    # def test_send_2_broken_files(self):
    #     self.client.connect()
    #     self.client.handle_command()
    #
    # @patch('builtins.input', lambda *args: 'Upgrade s.py')
    # def test_send_1_upgrade_file(self):
    #     self.client.connect()
    #     self.client.handle_command()


if __name__ == "__main__":
    unittest.main()
