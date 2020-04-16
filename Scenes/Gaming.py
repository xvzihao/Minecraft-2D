from Scenes import Scene
from main import Game, toBin
from world import World
from Sprites.player import Camera
import pyglet
from threading import Thread
import load
import time
import pyglet
import socket


class Gaming(Scene):
    def __init__(self, game, address):
        super().__init__(game)
        self.server = socket.socket()
        self.server.connect(address)
        self.server.send(toBin(address[1]))
        self.world = World(self.game)
        self.camera = Camera(self.world, self.server)

    def on_draw(self):
        self.camera.draw()
