from main import Game
from world import World, Region, Chunk
from block import minecraft as block
from main import Clock
import logger as log


class SuperFlat(World):
    """Super Flat World"""

    def __init__(self, game: Game):
        super().__init__(game)

    def build(self):
        """Build this world"""
        log.info("Building SuperFlat World")

        # Build Regions
        log_clock = Clock()
        regions = []
        for i in range(256):
            if log_clock.delay(1):
                log.info(f"[{int(i/256*100)}%] Building World")
            # Build Chunks
            region = Region(self)
            chunks = []
            chunk = Chunk(region)
            for x in range(8):
                chunk.blocks[0][x] = block.BedRock()
                chunk.blocks[1][x] = block.Dirt()
                chunk.blocks[2][x] = block.Dirt()
                chunk.blocks[3][x] = block.GrassBlock()
            chunks.append(chunk)

            for j in range(31):
                chunks.append(Chunk(region))

            region.chunks = chunks
            regions.append(region)


        self.regions = regions
        log.info("[100%]Building finished")