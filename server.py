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

    def start(self):
        """Start server"""
        self.server_socket.listen()
        print(f"Server is listening on port {self.port}")
        while True:
            self.__client_socket, self.__client_address = self.server_socket.accept()
            print(f"New connection from {self.__client_address}")
            self.handle_client_command()

    def handle_client_command(self):
        """Receive and exec command from client"""
        try:
            command = self.get_data_from_client()
            print(command)
            command, filename = command.split()
        except ValueError:
            print(f"Client {self.__client_address} interrupted connection")

        if command == "File":
            self.get_file(filename)
            self.compile_file(filename)
            self.__client_socket.close()
            print(f"{self.__client_address} disconnected")

        if command == "Number":
            for _ in range(int(filename)):
                command, filename = self.get_data_from_client().split()
                self.get_file(filename)
                self.compile_file(filename)

            self.__client_socket.close()
            print(f"{self.__client_address} disconnected")

        if command == "Upgrade":
            self.get_file(filename)
            if self.compile_file(filename):
                self.send_answer("Successfully upgraded")
                self.restart_server(filename)

            else:
                self.send_answer("Server is not upgraded")

            self.__client_socket.close()
            print(f"{self.__client_address} disconnected")

    def get_file(self, filename):
        """Receive file from client"""
        with open(filename, "w") as file:
            while True:
                data = self.get_data_from_client()
                if data == "END":
                    break
                file.write(data)
                self.send_answer("Data received")

        print(f"File {filename} is received")
        self.send_answer("Whole file is received")

    def compile_file(self, filename):
        """Exec file from client"""
        command = ["python", f"{filename}"]
        try:
            output = subprocess.run(command, capture_output=True, text=True, timeout=10)
            output.check_returncode()
            self.send_answer(f"File {filename} compilation is Ok")
            print(f"File {filename} is ok")
        except subprocess.TimeoutExpired:
            self.send_answer(f"File {filename} compilation is Ok")
            print(f"File {filename} is ok")
            return True
        except subprocess.CalledProcessError as ex:
            self.send_answer(ex.stderr)

    def restart_server(self, filename):
        """Restart server"""
        argv = [sys.executable, filename]

        print("Server is updated")
        os.execve(sys.executable, argv, os.environ)

    def get_data_from_client(self):
        data = self.__client_socket.recv(SIZE).decode(FORMAT)
        return data

    def send_answer(self, message):
        self.__client_socket.send(message.encode(FORMAT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--host", help="Server address", default="127.0.0.1")
    parser.add_argument("-p", "--port", help="Server port", type=int, default=1238)
    args = parser.parse_args()
    server = Server(ip=args.host, port=args.port)
    while True:
        server.start()
