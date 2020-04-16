from Scenes import Scene
from main import Game, Clock
from Sprites.gui import Button, string, color
import pyglet
import transform
import texture
import pygame
from main import Clock

class btnCancel(Button):
    def on_click(self):
        from Scenes.Menu import Menu
        self.game.change_scene(Menu(self.game))

class btnPlay(Button):
    def on_click(self):
        from Scenes.Gaming import Gaming
        self.game.change_scene(Gaming(self.game, ('127.0.0.1', 5901)))

class btnCreate(Button):
    def on_click(self):
        self.text = "Creating..."

class btnDelete(Button):
    def on_click(self):
        self.text = "Are you sure you want to delete this world!"

class SelectWorld(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.blk = texture.gui.options_background
        self.scale = 2
        self.darkblk = texture.gui.options_background_dark
        self.size = (856, 484) if self.game.scale <= 1.2 else (1920, 1080)
        self.background = transform.PygameToGL(pygame.Surface((856, 484)))
        self.block_height = 16
        self.label_select_world = string(source=[{"text": "Select World", "color": 'white'}], x=self.size[0]/2, y=self.game.height)

        # Clocks
        self.auto_on_resize_clock = Clock()
        self.refresh_clock = Clock()
        self.btn_refresh_clock = Clock()
        self.draw_clock = Clock()
        # Button
        self.btn_cancel = btnCancel(self.game, 'Cancel', color=color.white, type=1)
        self.btn_create = btnCreate(self.game, "Create New World", color=color.white, type=1)
        self.btn_delete = btnDelete(self.game, "Delete", color=color.white, type=1)
        self.btn_play = btnPlay(self.game, "Play Selected World", color=color.white, type=1)

    def on_resize(self):
        background = pygame.Surface((self.size[0]//3, self.size[1]//3))
        blk = transform.GLtoPygame(self.blk)
        dark_blk = transform.GLtoPygame(self.darkblk)
        width = blk.get_width()
        height = blk.get_height()
        self.block_height = height
        scale = 1
        blk = pygame.transform.scale(blk, (int(width*scale*self.game.scale), int(height*scale*self.game.scale)))
        dark_blk = pygame.transform.scale(dark_blk, (int(width*scale*self.game.scale), int(height*scale*self.game.scale)))

        b_width = blk.get_width()
        b_height = blk.get_height()
        bg_size = background.get_size()

        for y in range(int(self.game.height//b_height)):
            for x in range(int(self.game.width//b_width)):
                background.blit(dark_blk, (int(x * b_width), int(y * b_height)))

        for x in range(int(self.game.width//b_width)):
            background.blit(blk, (int(x * b_width), 0))
            background.blit(blk, (int(x * b_width), bg_size[1] - b_height*1,))
            background.blit(blk, (int(x * b_width), bg_size[1] - b_height*2,))

        self.background = transform.PygameToGL(background)




    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            from Scenes.Menu import Menu
            self.game.change_scene(Menu(self.game))

    def on_update(self):
        if self.size != self.game.size:
            self.size = self.game.size
            self.on_resize()
        self.label_select_world.x = self.game.width / 2 - self.label_select_world.width * self.game.scale / 4
        self.label_select_world.y = self.game.height - self.block_height * self.game.scale * 2
        self.label_select_world.scale = self.game.scale * 2
        if self.refresh_clock.delay(0.1):
            self.label_select_world.reset()

        if self.auto_on_resize_clock.delay(0.5):
            self.on_resize()

        if self.game.mouse.y < self.block_height*5*self.game.scale or self.btn_refresh_clock.delay(0.07):
            # Buttons
            self.btn_cancel.scale = self.game.scale * 1.8
            self.btn_create.scale = self.game.scale * 1.8
            self.btn_delete.scale = self.game.scale * 1.8
            self.btn_play.scale = self.game.scale * 1.8
            self.btn_cancel.refresh()
            self.btn_create.refresh()
            self.btn_delete.refresh()
            self.btn_play.refresh()
            self.btn_cancel.position = (
                self.game.width / 2 + 10,
                self.block_height * self.game.scale * 0.5
            )
            self.btn_play.position = (
                self.game.width / 2 - self.btn_create.width - 10,
                self.block_height * self.game.scale * 0.5 + self.btn_create.height+5
            )
            self.btn_create.position = (
                self.game.width / 2 + 10,
                self.block_height * self.game.scale * 0.5 + self.btn_create.height + 5
            )
            self.btn_delete.position = (
                self.game.width / 2 - self.btn_create.width - 10,
                self.block_height * self.game.scale * 0.5
            )

    def on_draw(self):
        if self.draw_clock.delay(0.005):
            self.background.blit(0, 0, 0, self.size[0], self.size[1])
            self.label_select_world.draw()
            # Buttons

            self.btn_cancel.draw()
            self.btn_cancel.drawText()
            self.btn_create.draw()
            self.btn_create.drawText()
            self.btn_delete.draw()
            self.btn_delete.drawText()
            self.btn_play.draw()
            self.btn_play.drawText()
