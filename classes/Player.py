class Player:
    def __init__(self, name, snails, cpu):
        self.name = name
        self.points = 0
        self.snails = snails
        self.cpu = cpu

    def __repr__(self):
        return self.name

    def add_points(self, points):
        self.points += points
