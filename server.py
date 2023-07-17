import argparse
import os
import socket
import subprocess
import sys

SIZE = 1024
FORMAT = "utf"


class Server:
    def __init__(self, port, ip):
        self.port = port
        self.ip = ip
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))

    def get_client_connection(self):
        client_socket, client_address = self.server_socket.accept()
        return client_socket, client_address

    def start(self):
        """Start server"""
        self.server_socket.listen()
        print(f"Server is listening on port {self.port}")
        while True:
            client_socket, client_address = self.get_client_connection()
            print(f"New connection from {client_address}")
            self.handle_client_command(client_address, client_socket)

    def handle_client_command(self, client_address, client_socket):
        """Receive and exec command from client"""
        try:
            command = self.get_data_from_client(client_socket)
            print(command)
            command, filename = command.split()
        except ValueError:
            print(f"Client {client_address} interrupted connection")

        if command == "File":
            self.get_file(filename, client_socket)
            self.compile_file(filename, client_socket)
            client_socket.close()
            print(f"{client_address} disconnected")

        if command == "Number":
            for _ in range(int(filename)):
                command, filename = self.get_data_from_client(client_socket).split()
                self.get_file(filename, client_socket)
                self.compile_file(filename, client_socket)

            client_socket.close()
            print(f"{client_address} disconnected")

        if command == "Upgrade":
            self.get_file(filename, client_socket)
            if self.compile_file(filename):
                self.send_answer("Successfully upgraded", client_socket)
                self.restart_server(filename)

            else:
                self.send_answer("Server is not upgraded", client_socket)

            client_socket.close()
            print(f"{client_address} disconnected")

    def get_file(self, filename, client_socket):
        """Receive file from client"""
        with open(filename, "w") as file:
            while True:
                data = self.get_data_from_client(client_socket)
                if data == "END":
                    break
                file.write(data)
                self.send_answer("Data received", client_socket)

        print(f"File {filename} is received")
        self.send_answer("Whole file is received", client_socket)

    def compile_file(self, filename, client_socket):
        """Exec file from client"""
        command = ["python", f"{filename}"]
        try:
            output = subprocess.run(command, capture_output=True, text=True, timeout=10)
            output.check_returncode()
            self.send_answer(f"File {filename} compilation is Ok", client_socket)
            print(f"File {filename} is ok")
        except subprocess.TimeoutExpired:
            self.send_answer(f"File {filename} compilation is Ok", client_socket)
            print(f"File {filename} is ok")
            return True
        except subprocess.CalledProcessError as ex:
            self.send_answer(ex.stderr, client_socket)

    def restart_server(self, filename):
        """Restart server"""
        argv = [sys.executable, filename]
        print("Server is updated")
        os.execve(sys.executable, argv, os.environ)

    def get_data_from_client(self, client_socket):
        data = client_socket.recv(SIZE).decode(FORMAT)
        return data

    def send_answer(self, message, client_socket):
        client_socket.send(message.encode(FORMAT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--host", help="Server address", default="127.0.0.1")
    parser.add_argument("-p", "--port", help="Server port", type=int, default=1238)
    args = parser.parse_args()
    server = Server(ip=args.host, port=args.port)
    while True:
        server.start()
