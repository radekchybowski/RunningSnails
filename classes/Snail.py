import random


class Snail:
    def __init__(self, color):
        self.id = random.choice(range(0, 100))
        self.color = color
        self.position = 0

    def __repr__(self):
        return "Ślimak (%s)" % self.color
