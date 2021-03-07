import socket
import pickle

HEADER_SIZE = 10
FORMAT = "utf-8"


class Network:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.id = self.connect()

    def connect(self):
        try:
            self.client.connect((self.host, self.port))
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            # send data
            d = pickle.dumps(data)
            d = bytes(f"{len(d):<{HEADER_SIZE}}", FORMAT) + d
            self.client.sendall(d)

            # receive and return data
            header = self.client.recv(HEADER_SIZE)
            d = self.client.recv(int(header))
            data = pickle.loads(d)
            return data
        except socket.error as e:
            print(e)
