import pyglet


class Base(pyglet.sprite.Sprite):
    """Base class of custom Sprite"""
    def __init__(self, img):
        super().__init__(img)

    def touch(self, *poses) -> bool:
        left, bottom = self.position
        right, top = left + self.width, bottom + self.height

        for pos in poses:
            x, y = pos
            if left <= x <= right and top >= y >= bottom:
                return True
        return False