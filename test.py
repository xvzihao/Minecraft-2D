from world.superflat import SuperFlat
from block.data import block_data
from main import binReader, toBin, toInt
import pygame
import time

if __name__ == '__main__':
    from block.minecraft import Stone
    from world import World
    world = World(None)
    with open("Superflat world.world", 'rb') as f:
        world.fromBytes(f.read())
    img = world.regions[250].chunks[0].export_image()
    pygame.image.save(img, "image.png")