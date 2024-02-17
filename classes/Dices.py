from classes.Dice import Dice


class Dices:
    colors = 'niebieski', 'żółty', 'fioletowy', 'zielony', 'czerwony'
    all_dices = []
    current_dices = []

    def __init__(self):
        self.current_dices = []
        for color in self.colors:
            self.current_dices.append(Dice(color))

    def __iter__(self):
        return self.current_dices

    def __next__(self):
        return self.current_dices

    def get_dice_by_color(self, color):
        for dice in self.current_dices:
            if dice.color == color:
                return dice

    def remove_dice(self, color):
        if len(self.current_dices) == 2:
            self.__init__()
            return
        self.current_dices.remove(self.get_dice_by_color(color))

    def throw_dices(self):
        for dice in self.current_dices:
            dice.get_value()
