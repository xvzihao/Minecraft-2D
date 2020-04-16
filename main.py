import pyglet
from Scenes import Scene
import time
import load
import logger as log
import os

# Global Variables
version = '0.5'

class binReader:
    def __init__(self, data:bytes):
        self.data = data
        self.index = 0

    def read(self, length=-1):
        if length == -1 or self.index + length > len(self.data):
            length = len(self.data)-self.index

        data = self.data[self.index:self.index+length]
        self.index += length
        return data

class Clock:
    def __init__(self):
        self.__goal = 0

    def delay(self, sec: float):
        if self.__goal + sec < time.time():
            self.__goal = time.time() + sec
            return True
        return False


toBin = lambda code: bytes([int(code / 256)]) + bytes([code - int(code / 256) * 256]) # to short type 0~65535

toInt = lambda code: int(code.hex(), 16)


class Mouse:
    def __init__(self):
        self.pos = (0, 0)
        self.x = 0
        self.y = 0
        self.left = False
        self.right = False

    def __str__(self):
        return f"<Mouse ({self.x}, {self.y}) {self.left}| {self.right}>"


class Game(pyglet.window.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scene = None
        # openGL initialization
        #
        pyglet.gl.glClearColor(1, 1, 1, 1)

        # Window Initialization
        self.frame_rate = 1 / 60
        self.fps = 0
        self.scale = 1
        self.descale = 1

        # Game initialization
        self.center = (0, 0)
        self.size = (856, 482)
        self.mouse = Mouse()
        self.run = True
        self.keys = []

    def change_scene(self, scene: Scene):
        self.scene.run = False
        old = self.scene
        self.scene = scene
        del old

    def update(self, dt):
        self.center = self.size[0] // 2, self.size[1] // 2
        self.size = self.get_size()

        if self.size[0] / 856 < self.size[1] / 482:
            self.scale = self.size[1] / 482
            self.descale = self.size[0] / 856
        else:
            self.scale = self.size[0] / 856
            self.descale = self.size[1] / 482

        # Other's turn
        self.scene.on_update()

    def cal_fps(self, dt):
        self.fps = int(pyglet.clock.get_fps())
        self.fps_text = pyglet.text.Label(
            text=f"FPS: {int(self.fps)}",
            font_name="Minecraftia",
            color=(50, 150, 50, 255),
            x=0,
            y=self.height,
            anchor_y='top',
        )

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.pos = x, y
        self.mouse.x = x
        self.mouse.y = y

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.F11:
            if not self.fullscreen:
                self.set_fullscreen(True)
            else:
                self.set_fullscreen(False)
        self.scene.on_key_press(symbol=symbol, modifiers=modifiers)
        self.keys.append(symbol)

    def on_key_release(self, symbol, modifiers):
        self.keys.remove(symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse.pos = x, y
        self.mouse.x = x
        self.mouse.y = y
        if button == 1:
            self.mouse.left = True
        elif button == 4:
            self.mouse.right = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse.pos = x, y
        self.mouse.x = x
        self.mouse.y = y
        if button == 1:
            self.mouse.left = False
        elif button == 4:
            self.mouse.right = False

    def on_draw(self):
        # self.clear()
        # Main Part
        self.scene.on_draw()
        # Display FPS
        self.fps_text.draw()


if __name__ == '__main__':
    # Initialization
    pyglet.resource.path.append('.')
    load.font("assets/minecraft/Minecraftia.ttf")
    #
    window = Game(width=856, height=482, caption=f"Minecraft 2D v{version}", resizable=True)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.clock.schedule_interval(window.cal_fps, 0.5)
    from Scenes.Initialization import Initialization

    window.set_minimum_size(128, 128)
    window.set_icon(load.image("assets/minecraft/textures/blocks/crafting_table_side.png"))
    window.scene = Initialization(window)
    try:
        pyglet.app.run()
    except Exception as e:
        log.err(f"Fatal Error: {e}")
        raise e

    log.info("Stopping Game")

    window.run = False
    log.info("Cleaning swap folder")
    for name in os.listdir("swap"):
        os.remove(f"swap/{name}")
    log.info("Game is stopped")
