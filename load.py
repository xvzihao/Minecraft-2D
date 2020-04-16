import pyglet
from pyglet import gl
import logger as log
import pygame
import transform
import os

unknown = pygame.Surface((16, 16))
unknown.fill((0, 0, 0))
__blk = pygame.Surface((8, 8))
__blk.fill((210, 0, 210))
unknown.blit(__blk, (0, 0))
unknown.blit(__blk, (8, 8))


def image(file, mode=0) -> pyglet.image.ImageData:
    try:
        img = pyglet.image.load(file)
        if mode == 0:
            img = img.get_texture()
            gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
            gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        log.info(f"Loading texture: {file}")
        return img
    except FileNotFoundError as e:

        log.info(f"Failed to load texture: {file}")
        if mode:
            return transform.PygameToGL(unknown).get_texture()
        else:
            return transform.PygameToGL(unknown)

class pg:
    @staticmethod
    def image(file):
        try:
            img = pygame.image.load(file)
            log.info(f"Loading texture: {file}")
            return img
        except:
            log.err(f"Failed to load texture: {file}")
            return unknown

def font(file):
    try:
        pyglet.font.add_file(file)
    except FileNotFoundError:
        log.err(f"Failed to load font: {file}")