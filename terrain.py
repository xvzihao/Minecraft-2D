from PIL import Image
import logger as log
import math

chunkTmp = {
    "NORMAL": Image.open("terrian.png").load(),
}

cos = lambda n: math.cos(math.radians(n))
sin = lambda n: math.sin(math.radians(n))

NORMAL = "NORMAL"

class TerrainWorker:
    """a 16*256 chunk"""
    def __init__(self):
        self.content = [64 for i in range(8)]
        self.rot = None
        self.pos = (None, None)
        self.left = None
        self.right = None
        self.type = None

    def build(self, rot=30, pos=(0, 0), type=NORMAL):
        self.type = type
        if rot > 180:
            rot = 0
        if rot < 0:
            rot = 180
        x, y = pos
        for i in range(8):
            height = round(chunkTmp[type][round(x), round(y)][0]/2.2) - 28
            self.content[i] = height
            x += cos(rot)
            y += sin(rot)
            if round(x) >= 150:
                x = 1
            if round(y) >= 100:
                y = 1
            if x < 0:
                x = 145
            if y < 0:
                y = 95
        self.pos = (x, y)
        self.rot = rot

    def buildLeft(self):
        self.left = TerrainWorker()
        self.left.build(self.rot-30, self.pos, self.type)

    def buildRight(self):
        self.right = TerrainWorker()
        self.right.build(self.rot+30, self.pos, self.type)
