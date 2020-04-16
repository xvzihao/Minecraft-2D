import socket
import threading
import time

import logger as log

toBin = lambda code: bytes([int(code / 256)]) + bytes([code - int(code / 256) * 256])  # to short type 0~65535
toInt = lambda code: int(code.hex(), 16)

class socketQueue(dict):

    def top(self) -> tuple:
        key = list(self.keys())[0]
        item = self[key]
        del self[key]
        return key, item

    def include(self, sign):
        return sign in self

    def get(self, k):
        item = super().get(k)
        del self[k]
        return item

    def add(self, sign:int, command:int, args):
        self[sign] = (command, args)

class Server:
    """Server class"""

    def __init__(self):
        self.socket = socket.socket()
        self.ip = '127.0.0.1'
        self.port = 5901
        self.maximum = 8
        self.is_running = False
        self.clients = []

    def run(self):
        self.is_running = True
        log.info("Starting Server")

        log.info(f"Binding address: {(self.ip, self.port)}")
        self.socket.bind((self.ip, self.port))

        log.info(f"Set Maximum player number: {self.maximum}")
        self.socket.listen(self.maximum)

        log.info(f"Server is online")
        while self.is_running:
            try:
                conn, addr = self.socket.accept()
                code = toInt(conn.recv(2))
                if code == self.port:
                    client = Client(self, conn, addr)
                    client.run()
                    self.clients.append(client)
                else:
                    log.warn(f"A strange connection from {addr} [err code: {code}]")
                    conn.send(b'["invalid connection"]')
                    conn.close()
            except socket.timeout:
                pass


class Client:
    def __init__(self, server: Server, connection: socket.socket, address: tuple):
        self.server = server
        self.socket = connection
        self.address = address
        self.requestQueue = socketQueue()
        self.responseQueue = socketQueue()

    def run(self):
        log.info(f"New connection from {self.address}")
        threading.Thread(
            target=self.clientNetworkResponseThread,
            name=f"clientNetworkResponseThread[{self.address}]").start()
        threading.Thread(
            target=self.clientNetworkRequestThread,
            name=f"clientNetworkRequestThread[{self.address}]").start()

    def clientNetworkRequestThread(self):  # server to client
        while self.server.is_running:
            time.sleep(0.02)
            if self.requestQueue:
                sign, pack = self.requestQueue.top()
                command, args = pack
                self.socket.send(toBin(sign))  # Send the sign
                self.socket.send(toBin(command))  # Send the command
                self.socket.send(toBin(len(args)))  # Send arg length
                for arg in args:
                    self.socket.send(toBin(arg))  # Send each arg

    def clientNetworkResponseThread(self):  # client to server
        while self.server.is_running:
            try:
                time.sleep(0.02)
                data_sign = self.socket.recv(2)
                if data_sign == b'':
                    break
                sign = toInt(data_sign)  # Get the sign
                if sign == 0:
                    continue
                size = toInt(self.socket.recv(2))  # Get package size
                pack = self.socket.recv(size)
                self.responseQueue[sign] = pack
            except ConnectionResetError:
                break
            except socket.timeout:
                pass
        log.info(f"{self.address} left")
        self.socket.close()
        self.server.clients.remove(self)



if __name__ == '__main__':
    server = Server()
    server.run()
