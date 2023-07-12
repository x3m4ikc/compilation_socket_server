import socket
import subprocess
import os
import sys

SIZE = 1024
FORMAT = "utf"


class Server:
    def __init__(self, port=1233, ip="127.0.0.1"):
        self.__client_socket = None
        self.__client_address = None
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
        command = self.__client_socket.recv(SIZE).decode(FORMAT)
        print(command)
        command, filename = command.split()

        if command == "File":
            self.get_file(filename)
            self.compile_file(filename)
            self.__client_socket.close()
            print(f"{self.__client_address} disconnected")

        if command == "Number":
            for _ in range(int(filename)):
                command, filename = (
                    self.__client_socket.recv(SIZE).decode(FORMAT).split()
                )
                self.get_file(filename)
                self.compile_file(filename)

            self.__client_socket.close()
            print(f"{self.__client_address} disconnected")

#        if command == "Upgrade":
#            self.get_file()
#            if self.compile_file(filename):
#                self.__client_socket.send("Successfully upgraded".encode(FORMAT))
#                 self.__client_socket.close()
#                print(f"{self.__client_address} disconnected")
#                self.restart_server(filename)
#            else:
#                self.__client_socket.send("Server not updated".encode(FORMAT))
#                self.__client_socket.close()
#                print(f"{self.__client_address} disconnected")

        if command == "Upgrade":
            self.get_file(filename)
            if self.compile_file(filename):
                self.__client_socket.send("Successfully upgraded".encode(FORMAT))
                self.restart_server(filename)
            else:
                self.__client_socket.send("Server is not upgraded".encode(FORMAT))

    def get_file(self, filename):
        """Receive file from client"""
        print("start of getting a file")

        with open(filename, "w") as file:
            while True:
                data = self.__client_socket.recv(SIZE).decode(FORMAT)
                if data == "END":
                    break
                file.write(data)
                self.__client_socket.send("Data received".encode(FORMAT))

        print(f"File {filename} is received")
        self.__client_socket.send("Whole file is received".encode(FORMAT))

    def return_compilation_result(self, output, filename):
        output.check_returncode()
        self.__client_socket.send("Ok".encode(FORMAT))
        print(f"File {filename} is ok")
        return True

    def compile_file(self, filename):
        """Exec file from client"""
        command = ["python", f"{filename}"]
        try:
            output = subprocess.run(command, capture_output=True, text=True, timeout=10)
            output.check_returncode()
            self.__client_socket.send("Ok".encode(FORMAT))
            print(f"File {filename} is ok")
            return True
        except subprocess.TimeoutExpired:
            self.__client_socket.send("Ok".encode(FORMAT))
            print(f"File {filename} is ok")
            return True
        except subprocess.CalledProcessError as ex:
            self.__client_socket.send(f"{ex.stderr}".encode(FORMAT))

    def restart_server(self, filename):
        """Restart server"""
        argv = [sys.executable, filename]

        print("Server is updated")
        os.execve(sys.executable, argv, os.environ)


if __name__ == "__main__":
    server = Server()
    while True:
        server.start()
