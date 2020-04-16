import pygame
import pyglet
from PIL import ImageFilter, ImageEnhance
from PIL import Image
import time

from pyglet import gl

import logger as log
from threading import Thread
import os

rmlist = []

def remove(file):
    def __remove__(file):
        try:
            os.remove(file)
        except PermissionError:
            time.sleep(3)
            try:
                os.remove(file)
            except Exception as e:
                log.err(f"Failed to remove swap file \"{file}\"")

    Thread(target=__remove__, args=(file, ), name="Auto Remove File").start()

def PygameToGL(image: pygame.SurfaceType, mode=0) -> pyglet.image.AbstractImage:
    h = hash(image)
    path = f"swap/IMG_PYGAME_TO_GL_{h}.png"
    pygame.image.save(image, path)
    img = pyglet.image.load(path)
    if mode == 0:
        img = img.get_texture()
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    remove(path)
    return img

def PILtoPygame(image) -> pygame.SurfaceType:
    h = hash(image.tobytes())
    path = f"swap/IMG_PIL_TO_PYGAME_{h}.png"
    image.save(path)
    PG_image = pygame.image.load(path)
    remove(path)
    return PG_image


def PygameToPIL(surface):
    h = hash(surface)
    path = f"swap/IMG_PYGAME_TO_PIL_{h}.png"
    pygame.image.save(surface, path)
    img = Image.open(path)
    remove(path)
    return img


def GLtoPygame(image) -> pygame.SurfaceType:
    h = hash(image)
    path = f"swap/IMG_GL_TO_PYGAME_{h}.png"
    image.save(path)
    img = pygame.image.load(path)
    remove(path)
    return img

def GLtoPIL(image) -> Image.Image:
    h = hash(image)
    path = f"swap/IMG_GL_TO_PIL_{h}.png"
    image.save(path)
    img = Image.open(path)
    remove(path)
    return img

def PILtoGL(image, mode=0):
    h = hash(image.tobytes())
    path = f"swap/IMG_PIL_TO_GL_{h}.png"
    image.save(path)
    img = pyglet.image.load(f"swap/IMG_PIL_TO_GL_{h}.png")
    if mode == 0:
        img = img.get_texture()
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    remove(path)
    return img

def brightness(image, rate):
    return PILtoGL(
        ImageEnhance.Brightness(
            GLtoPIL(image)
        ).enhance(rate)
    )

def blur(image, radius=1):
    return PILtoGL(
        GLtoPIL(image).filter(ImageFilter.GaussianBlur(radius=radius))
    )

def scale(image, rate, mode=0):
    img = GLtoPygame(image)
    img = pygame.transform.scale(img, (img.get_width()*rate, img.get_height()*rate))
    return PygameToGL(img, mode=mode)

if __name__ == '__main__':
    import threading, load
    img = load.image("icon_32x32.png")
    threading.Thread(target=GLtoPygame, args=(img, )).start()