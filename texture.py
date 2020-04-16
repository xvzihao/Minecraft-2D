import load
import transform
import logger as log
import pygame
import time

log.info("Loading Resources")

class gui:
    background = load.image("assets/minecraft/textures/gui/title/background/panorama_0.png")
    background = transform.blur(transform.scale(background, 4, 0), 8)

    mojang = load.image("assets/minecraft/textures/gui/title/mojang.png")
    __raw_minecraft = load.pg.image("assets/minecraft/textures/gui/title/minecraft.png")
    # Re-make Minecraft LOGO
    try:
        __minecraft = pygame.Surface((274, 45), flags=pygame.SRCALPHA)
        __minecraft.blits([
            (__raw_minecraft.subsurface((0, 0, 155, 44)), (0, 0)),
            (__raw_minecraft.subsurface((0, 45, 119, 44)), (154, 0))
        ])
        minecraft = transform.PygameToGL(__minecraft)
    except Exception:
        minecraft = transform.PygameToGL(__raw_minecraft)



    widgets = load.pg.image("assets/minecraft/textures/gui/widgets.png")
    button = widgets.subsurface(0, 66, 200, 20)
    button_highlight = widgets.subsurface(0, 86, 200, 20)
    # Half Button
    button_half = pygame.Surface((75, 20))
    button_half.blits(
        [(button.subsurface((0, 0, 65, 20)), (0, 0)), (button.subsurface((190, 0, 10, 20)), (65, 0))]
    )
    # Half Button high light version
    button_half_highlight = pygame.Surface((75, 20))
    button_half_highlight.blits(
        [(button_highlight.subsurface((0, 0, 65, 20)), (0, 0)), (button_highlight.subsurface((190, 0, 10, 20)), (65, 0))]
    )
    # Convert
    button = transform.PygameToGL(button)
    button_highlight = transform.PygameToGL(button_highlight)
    button_half = transform.PygameToGL(button_half)
    button_half_highlight = transform.PygameToGL(button_half_highlight)

    options_background = transform.brightness(load.image("assets/minecraft/textures/gui/options_background.png"), 0.3)
    options_background_dark = transform.brightness(options_background, 0.4)


class blocks:
    pointing_at = pygame.Surface((16, 16), flags=pygame.SRCALPHA)
    for i in range(16):
        color = (0, 0, 0, 80)
        pointing_at.set_at((i, 0), color)
        pointing_at.set_at((i, 15), color)
        pointing_at.set_at((0, i), color)
        pointing_at.set_at((15, i), color)
    pointing_at = transform.PygameToGL(pointing_at)

    grassBlock = load.pg.image("assets/minecraft/textures/blocks/grass_side.png")
    dirt = load.pg.image("assets/minecraft/textures/blocks/dirt.png")
    bedRock = load.pg.image("assets/minecraft/textures/blocks/bedrock.png")
    stone = load.pg.image("assets/minecraft/textures/blocks/stone.png")