from Scenes import Scene
from main import Game
import pyglet
from threading import Thread
import load
import time


class Initialization(Scene):

    def __init__(self, game: Game):
        super().__init__(game)
        self.bg = pyglet.sprite.Sprite(load.image("assets/minecraft/textures/gui/title/mojang.png"), x=128, y=64)
        self.thread = Thread(target=self.process, name="Initialization")
        self.draw_count = 0


    def process(self):
        time.sleep(0.1)
        from Scenes.Menu import Menu
        self.game.change_scene(Menu(self.game))

    def on_update(self):
        self.bg.position = (
            self.game.width / 2 - 256,
            self.game.height / 2 - 256
        )
        self.bg.scale = 2

    def on_draw(self):
        self.bg.draw()
        if self.draw_count == 2:
            from Scenes.Menu import Menu
            self.thread.start()
            self.draw_count = 3
        if self.draw_count <= 2:
            self.draw_count += 1
