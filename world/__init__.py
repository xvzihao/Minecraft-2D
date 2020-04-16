from main import Game, toBin, toInt, binReader
from block import Block
from block import minecraft as block
from typing import List
from block.data import block_data
import logger as log
import pygame

class World:
    """The base class of world"""

    def __init__(self, game: Game):
        self.game = game
        self.seeds = 0
        self.regions = [Region(self) for i in range(256)]

    def setBlock(self, x:int, y:int, block:Block):
        """Set block at <x> <y>"""
        if not -1024 <= x <= 1024 or not 255 >= y >= 0:
            log.warn("Set Block Ignored: Attempted to set a block outside of the world")
            return
        if not issubclass(type(block), Block):
            raise TypeError("you have to set block as the 3rd argument")
        x += 1024
        x_region = int(x/8)
        x_real = x%8
        region = self.regions[x_region]
        y_chunk = int(y/8)
        y_real = y%8
        chunk = region.chunks[y_chunk]
        chunk.blocks[y_real][x_real] = block


    def toBytes(self) -> bytes:
        result = b''
        for region in self.regions:
            r_data = region.toBytes()
            result += toBin(len(r_data))
            result += r_data

        return result

    def fromBytes(self, data: bytes):
        reader = binReader(data)
        regions = []
        for i in range(256):
            length = toInt(reader.read(2))
            region = Region(self)
            region.fromBytes(reader.read(length))
            regions.append(region)
        self.regions = regions

class Region:
    """The base class of regions"""

    def __init__(self, world: World):
        self.world = world
        self.game = self.world.game
        self.chunks = [Chunk(self) for i in range(32)]

    def fromBytes(self, data: bytes):
        chunks = []
        reader = binReader(data)
        for i in range(32):
            length = toInt(reader.read(2))
            chunk = Chunk(self)
            chunk.fromBytes(reader.read(length))
            chunks.append(chunk)
        self.chunks = chunks

    def toBytes(self) -> bytes:
        result = b''
        for chunk in self.chunks:
            c_data = chunk.toBytes()
            result += toBin(len(c_data))
            result += c_data
        return result


    def on_draw(self):
        pass



class Chunk:
    """The base class of chunks"""

    def __init__(self, region: Region):
        self.region = region
        self.world = self.region.world
        self.game = self.world.game
        self.blocks = []
        for y in range(8):
            self.blocks.append([])
            for x in range(8):
                self.blocks[y].append(block.Air())

    def toBytes(self) -> bytes:
        # data:[blk,blk,blk]
        # blk: len info
        result = b''
        for y in range(8):
            for x in range(8):
                b_data = self.blocks[y][x].toBytes()
                result += toBin(len(b_data))
                result += b_data

        return result

    def fromBytes(self, data: bytes):
        reader = binReader(data)
        for y in range(8):
            for x in range(8):
                # !This is a chunk
                length = toInt(reader.read(2))
                pack = reader.read(length)
                type = pack[:2]
                self.blocks[y][x] = block_data[toInt(type)](data=pack[2:])


    def export_image(self) -> pygame.SurfaceType:
        img = pygame.Surface((128, 128), pygame.SRCALPHA)
        blits = []
        for y in range(8):
            for x in range(8):
                block = self.blocks[y][x]
                blits.append( (block.image, (x*16, 112-y*16)) )
        img.blits(blits)
        return img
