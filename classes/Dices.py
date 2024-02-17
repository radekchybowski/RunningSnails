from classes.Dice import Dice


class Dices:
    colors = 'niebieski', 'żółty', 'fioletowy', 'zielony', 'czerwony'
    allDices = []
    currentDices = []

    def __init__(self):
        self.currentDices = []
        for color in self.colors:
            self.currentDices.append(Dice(color))

    def __iter__(self):
        return self.currentDices

    def __next__(self):
        return self.currentDices

    def getDiceByColor(self, color):
        for dice in self.currentDices:
            if dice.color == color:
                return dice

    def removeDice(self, color):
        if len(self.currentDices) == 2:
            self.__init__()
            return
        self.currentDices.remove(self.getDiceByColor(color))

    def throwDices(self):
        for dice in self.currentDices:
            dice.rzut()
