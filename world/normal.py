from main import Game
from world import World, Region, Chunk
from block import minecraft as block
from main import Clock
import logger as log
from terrain import TerrainWorker

class NormalWorld(World):
    """A normal World"""
    def build(self):
        worker = TerrainWorker()
        log.info("Building Terrain")
        worker.build()
        for i in range(256):
            # Fill the height
            for y in range(len(worker.content)):
                for j in range(worker.content[y]):
                    if j == worker.content[y]-1:
                        blk = block.GrassBlock()
                    elif worker.content[y]-5 < j:
                        blk = block.Dirt()
                    else:
                        blk = block.Stone()
                    self.setBlock(i*8+y-1024, j, blk)

            worker.buildRight()
            raw = worker
            worker = worker.right
            del raw