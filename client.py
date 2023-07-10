import os
import socket

SIZE = 1024
FORMAT = "utf"


class Client:
    def __init__(self, ip="127.0.0.1", port=1235):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_socket.connect((self.ip, self.port))

    def handle_command(self):
        command = input()
        self.client_socket.send(command.encode(FORMAT))
        command, filename = command.split()

        if command == "File":
            self.send_file(filename)
            self.get_result()

        if command == "Number":
            for _ in range(int(filename)):
                self.handle_command()

#        if command == "Upgrade":
#            self.send_file(filename)
#            self.get_result()

    def send_file(self, filename):
        file = open(f"data/{filename}", "r")
        data = file.read()
        self.client_socket.send(filename.encode(FORMAT))
        message = self.client_socket.recv(SIZE).decode(FORMAT)
        print(f"Server`s answer: {message}")
        self.client_socket.send(data.encode(FORMAT))
        file.close()

    def get_result(self):
        result = self.client_socket.recv(SIZE).decode(FORMAT)
        print(f"Result of file compilation: {result}")

    def close_connection(self):
        self.client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.connect()
    client.handle_command()
    client.close_connection()
