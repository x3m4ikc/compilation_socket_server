import socket
import subprocess
import sys

SIZE = 1024
FORMAT = "utf"

"""New version"""


class Server:
    def __init__(self, port=1235, ip="127.0.0.1"):
        self.__client_socket = None
        self.__client_address = None
        self.port = port
        self.ip = ip
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))

    def start(self):
        self.server_socket.listen()
        print(f"New server is listening on port {self.port}")
        while True:
            self.__client_socket, self.__client_address = self.server_socket.accept()
            print(f"New server got new connection from {self.__client_address}")
            self.handle_client()

    def handle_client(self):
        command = self.__client_socket.recv(SIZE).decode(FORMAT)
        print(command)
        command, filename = command.split()

        if command == "File":
            self.get_file()
            self.compile_file(filename)
            self.__client_socket.close()
            print(f"{self.__client_address} disconnected")

        if command == "Number":
            for _ in range(int(filename)):
                command, filename = (
                    self.__client_socket.recv(SIZE).decode(FORMAT).split()
                )
                self.get_file()
                self.compile_file(filename)

        if command == "Upgrade":
            self.get_file()
            command = ["python", f"{filename}"]
            result = subprocess.call(command)
            if result == 0:
                sys.exit()

    def get_file(self):
        filename = self.__client_socket.recv(SIZE).decode(FORMAT)
        print(f"File {filename} is received")
        file = open(filename, "w")
        self.__client_socket.send("File is received".encode(FORMAT))

        data = self.__client_socket.recv(SIZE).decode(FORMAT)
        file.write(data)
        file.close()

    def compile_file(self, filename):
        command = ["python", f"{filename}"]
        try:
            output = subprocess.run(command, capture_output=True, text=True)
            output.check_returncode()
            self.__client_socket.send("Ok".encode(FORMAT))
            return 1
        except subprocess.CalledProcessError as ex:
            self.__client_socket.send(f"{ex.stderr}".encode(FORMAT))


if __name__ == "__main__":
    server = Server()
    server.start()
