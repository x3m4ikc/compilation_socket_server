import socket

SIZE = 1024
FORMAT = "utf"


class Client:
    def __init__(self, ip="127.0.0.1", port=1233):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connect to server"""
        self.client_socket.connect((self.ip, self.port))

    def handle_command(self):
        """Get command with files from user"""
        command = input()
        self.client_socket.send(command.encode(FORMAT))
        command, filename = command.split()

        if command == "File":
            self.send_file(filename)
            self.get_result()
            self.get_result()

        if command == "Number":
            for _ in range(int(filename)):
                self.handle_command()

        if command == "Upgrade":
            self.send_file(filename)
            self.get_result()

#        if command == "Upgrade":
#            self.send_file(filename)
#            self.get_result()
#            result = self.client_socket.recv(SIZE).decode(FORMAT)
#            print(result)

    def send_file(self, filename):
        """Send file to server"""
        print("start sending")

        with open(f"data/{filename}", "r") as file:
            while True:
                data = file.read(SIZE)
                if not data:
                    data = "END"
                    self.client_socket.send(data.encode(FORMAT))
                    break
                self.client_socket.send(data.encode(FORMAT))
                message = self.client_socket.recv(SIZE).decode(FORMAT)
                print(message)

    def get_result(self):
        """Get message of compilation result"""
        result = self.client_socket.recv(SIZE).decode(FORMAT)
        print(f"Server`s answer: {result}")

    def close_connection(self):
        """Close connection with server"""
        self.client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.connect()
    client.handle_command()
    client.close_connection()
