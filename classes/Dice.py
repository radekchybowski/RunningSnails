import random


class Dice:
    color = None
    value = None
    fields = 'snail', 1, 2, 3, 4, 5

    def __init__(self, color):
        self.id = random.choice(range(0, 100))
        self.color = color
        self.get_value()

    def get_value(self):
        self.value = random.choice(self.fields)
        return self.value
