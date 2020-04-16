import pyglet
from random import randint
import logger as log
from world import World
from world import Region, Chunk
from Sprites.gui import string
from communicate import sign
from main import toInt, toBin, Clock
import transform
import pygame
from pyglet.window import key
import socket
import time
import threading
from texture import blocks

def cvt_chunk(x, y):
    return int(x/8), int(y/8)

class socketQueue(dict):

    def top(self) -> tuple:
        key = list(self.keys())[0]
        item = self[key]
        del self[key]
        return key, item

    def include(self, sign: str):
        return sign in self

    def get(self, k):
        item = super().get(k)
        del self[k]
        return item

    def add(self, sign:str, command:str, args:tuple):
        self[sign] = (command, args)


class Camera:
    """Class Camera"""
    def __init__(self, world:World, server:socket.socket):
        self.x = 5
        self.y = 0
        self.world = world
        self.server = server
        self.server.settimeout(2)
        self.game = world.game
        self.unloaded = [[
            True for chunk in range(32)
        ] for region in range(256)]
        self.chunkImgs = [
            [None for y in range(32)] for x in range(256)
        ]



        # Queues
        self.requestQueue = socketQueue()
        self.responseQueue = socketQueue()

        # Display
        self.info = string("test", 5, 10, 6)

        # OP initialize
        self.op_clock = Clock()
        self.mouse = [0, 0]
        self.pointing = [0, 0]

        # GL initialize
        pyglet.gl.glClearColor(0.7, 0.8, 1, 1)
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # Run Threads
        threading.Thread(target=self.networkRequestThread, name="Camera-NetworkRequestThread").start()
        threading.Thread(target=self.networkResponseThread, name="Camera-NetworkResponseThread").start()

        #
    def getImage(self, x, y):
        if self.unloaded[x][y]:
            self.get

    def draw(self):
        pass

    def networkRequestThread(self):
        while self.game.run:
            time.sleep(0.02)
            try:
                if self.requestQueue:
                    sign, pack = self.requestQueue.top()
                    command, args = pack
                    self.server.send(toBin(sign)) # Send the sign
                    self.server.send(toBin(command)) # Send the command
                    self.server.send(toBin(len(args))) # Send arg length
                    for arg in args:
                        self.server.send(toBin(arg)) # Send each arg
            except socket.timeout:
                pass

    def networkResponseThread(self):
        while self.game.run:
            try:
                time.sleep(0.02)
                sign = toInt(self.server.recv(2)) # Get the sign
                if sign == 0:
                    continue
                size = toInt(self.server.recv(2)) # Get package size
                pack = self.server.recv(size)
                self.responseQueue[sign] = pack
            except socket.timeout:
                pass
