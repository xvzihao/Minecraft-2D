from block import Block
from texture import blocks
from block import data
import pygame


class Air(Block):
    def init(self):
        self.doStick = False
        self.standable = False
        self.light = False
        self.washable = False
        self.stackCapacity = 0
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)


data.block_data.append(Air)


class GrassBlock(Block):

    def init(self):
        self.image = blocks.grassBlock


data.block_data.append(GrassBlock)


class BedRock(Block):
    def init(self):
        self.image = blocks.bedRock
        self.hardness = 32678


data.block_data.append(BedRock)


class Dirt(Block):
    def init(self):
        self.image = blocks.dirt


data.block_data.append(Dirt)

class Stone(Block):
    def init(self):
        self.image = blocks.stone
        self.hardness = 10

data.block_data.append(Stone)
