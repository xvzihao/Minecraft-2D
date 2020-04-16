from Sprites import Base
from main import Game, Clock
from texture import gui
import pyglet

rgb = lambda code: tuple(int(code[i * 2:i * 2 + 2], 16) for i in range(3))


class color:
    dark_red = rgb("AA0000")
    red = rgb("FF5555")
    gold = rgb("FFAA00")
    yellow = rgb("FFFF55")
    dark_green = rgb("00AA00")
    green = rgb("55FF55")
    aqua = rgb("55FFFF")
    dark_aqua = rgb("00AAAA")
    dark_blue = rgb("0000AA")
    blue = rgb("5555FF")
    light_purple = rgb("FF55FF")
    dark_purple = rgb("AA00AA")
    white = rgb("FFFFFF")
    gray = rgb("AAAAAA")
    dark_gray = rgb("555555")
    black = rgb("000000")


COLOR = {
    "dark_red": color.dark_red,
    "red": color.red,
    "gold": color.gold,
    "yellow": color.yellow,
    "dark_green": color.dark_green,
    "green": color.green,
    "aqua": color.aqua,
    "dark_aqua": color.dark_aqua,
    "dark_blue": color.dark_blue,
    "blue": color.blue,
    "light_purple": color.light_purple,
    "dark_purple": color.dark_purple,
    "white": color.white,
    "gray": color.gray,
    "dark_gray": color.dark_gray,
    "black": color.black,
}


class string:
    def __init__(self, source, x, y, scale=1):
        """
        an object for displaying text

        <source> :
            str: display <source: str> by default:
                [{"text": source,
                "color": "white",
                "bold": False,
                "italic": False,
                "underline": False,
                "shade": False}]
            dict: display <source: dict>
            list[dict]: display each <element: dict> of <source: list[dict]>
        """
        if type(source) == str:
            self.source = [{"text": source}]

        elif type(source) == dict:
            self.source = [source]

        elif type(source) == list:
            self.source = source

        else:
            raise TypeError("Unexpected type of source")

        self.fontObjects = []
        self.x = x
        self.y = y
        self.scale = scale
        self.width = None
        self.height = None

        self.reset()

    def reset(self):
        text = ''
        color = COLOR['white']
        bold = False
        italic = False
        shade = False
        fontObjects = []
        width = 0
        for js in self.source:
            if 'text' in js:
                text = js['text']
            if 'color' in js:
                color = COLOR[js['color']]
            if 'bold' in js:
                bold = js['bold']
            if 'italic' in js:
                italic = js['italic']
            if 'shade' in js:
                shade = js['shade']
            if shade:
                fontObjects += \
                    [
                        pyglet.text.Label(
                            font_name="Minecraftia",
                            text=text,
                            color=(60, 60, 60, 200),
                            bold=bold,
                            italic=italic,
                            font_size=self.scale * 6,
                            x=self.x + self.scale + width,
                            y=self.y - self.scale
                        ),
                    ]

            fontObjects += \
                [
                    pyglet.text.Label(
                        font_name="Minecraftia",
                        text=text,
                        color=color + (255,),
                        bold=bold,
                        italic=italic,
                        font_size=self.scale * 6,
                        x=self.x + width,
                        y=self.y,
                    )
                ]

            width += fontObjects[-1].content_width

        self.fontObjects = fontObjects
        self.width = width
        self.height = self.fontObjects[0].content_height

    def draw(self):
        for obj in self.fontObjects:
            obj.draw()


class Button(Base):
    def __init__(self, game: Game, text: str, color=color.white, type=0):
        self.type = type
        img = gui.button if self.type else gui.button_half
        self.game = game
        self.text = text
        self.t_color = color
        self.__draw_text = None
        self.__draw_text_deep = None
        self.__clicking = False
        self.clock = Clock()
        super().__init__(img)

    def drawText(self):
        self.__draw_text_deep.draw()
        self.__draw_text.draw()

    def on_click(self):
        pass

    def refresh(self):
        if self.touch(self.game.mouse.pos):
            self.image = gui.button_highlight if self.type else gui.button_half_highlight
            if self.game.mouse.left and not self.__clicking:
                self.on_click()
                self.__clicking = True
        else:
            self.image = gui.button if self.type else gui.button_half
        if self.game.mouse.left == False:
            self.__clicking = False
        self.__draw_text = pyglet.text.Label(
            text=self.text,
            font_name="Minecraftia",
            font_size=self.scale * 6,
            color=(self.t_color + (255,)) if self.image in (gui.button, gui.button_half) else (255, 255, 100, 255),
            x=self.x + self.width / 2 - len(self.text) * 2.5 * self.scale,
            y=self.y + self.height / 2 - 3.2 * self.scale,
        )
        self.__draw_text_deep = pyglet.text.Label(
            text=self.text,
            font_name="Minecraftia",
            font_size=self.scale * 6,
            color=(60,) * 3 + (200,),
            x=self.x + self.width / 2 - len(self.text) * 2.5 * self.scale + self.scale * 1,
            y=self.y + self.height / 2 - 3.2 * self.scale - self.scale * 1,
        )
