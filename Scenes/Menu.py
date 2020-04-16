from Scenes import Scene
from main import Game, Clock
from Sprites.gui import Button
import pyglet


class SinglePlayer(Button):
    def __init__(self, game: Game, text: str):
        super().__init__(game, text, type=1)

    def on_click(self):
        from Scenes.SelectWorld import SelectWorld
        self.game.change_scene(SelectWorld(game=self.game))

class Menu(Scene):

    def __init__(self, game: Game):
        super().__init__(game)
        import texture
        self.bg = pyglet.sprite.Sprite(texture.gui.background, x=-24, y=-64)
        self.clock = Clock()
        self.rot_d = 0.01

        self.minecraft = pyglet.sprite.Sprite(texture.gui.minecraft)
        self.singlePlayer = SinglePlayer(self.game, "Singleplayer")

    def on_update(self):
        self.bg.scale = self.game.scale
        self.bg.x = -15 - self.game.scale*140
        rate = 1.7
        brate = rate * 1.2

        if self.game.width/856 > self.game.width/482:
            scale = self.game.scale

        else:
            scale = self.game.descale

        if scale > 3:
            scale = 3*rate
            brate = rate*1.3
        else:
            self.minecraft.scale = scale*rate
            self.singlePlayer.scale = scale*brate
        self.minecraft.position = (
            self.game.center[0] - self.minecraft.image.width/2*scale*rate,
            self.game.height - 64 - scale*40*rate
        )
        self.singlePlayer.position = (
            self.game.center[0] - 100*scale*brate,
            self.game.height - 64 - scale*85*rate - scale*20*brate
        )

        self.singlePlayer.refresh()
        if self.clock.delay(0.01):
            self.bg.rotation += self.rot_d
            if abs(self.bg.rotation) > 0.8:
                self.rot_d = - self.rot_d

    def on_draw(self):
        self.bg.draw()
        self.minecraft.draw()
        self.singlePlayer.draw()
        self.singlePlayer.drawText()