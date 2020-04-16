class Scene:
    """Scene class"""
    def __init__(self, game):
        self.game = game
        self.events = []
        self.run = True

    def on_key_press(self, symbol, modifiers):
        """Will be executed when key press"""
        pass

    def on_update(self):
        """Will be executed when update the data"""
        pass

    def on_draw(self):
        """Will be executed when drawing the screen"""
        pass