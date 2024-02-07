from flask import Flask, render_template, request
import random, copy

app = Flask(__name__)



class Game():
    board = []
    colors = 'niebieski', 'żółty', 'fioletowy', 'zielony', 'czerwony'

    def __init__(self):
        self.gametype = "hotseat"
        self.dices = Dices()


        for i in range(1, 20):
            self.board.append({'type': "", 'value': i, 'snails': []})
            if i == 1:
                self.board[i-1]['type'] = 'start'
                for color in self.colors:
                    self.board[i-1]['snails'].append(Snail(color))
            if i == 7 or i == 11:
                self.board[i-1]['type'] = 'grzyb'
            if i == 19:
                self.board[i-1]['type'] = 'meta'

    def moveSnail(self, color, position):
        for i, field in enumerate(self.board):
            for snail in field['snails']:
                if snail.color == color:
                    if position == 'snail':
                        position = 2
                    else:
                        self.dices.removeDice(color)
                    x = i + position
                    if x >= 18:
                        x = 18
                        self.endgame()
                    if x < 0:
                        x = 0
                    print('i: ', i, 'position: ', position)
                    if (len(self.board[x]['snails']) != 0) and self.board[x]['type'] != 'grzyb':
                        self.board[x-1]['snails'] += self.board[x]['snails']
                        self.board[x]['snails'] = []

                    self.board[x]['snails'].append(snail)
                    self.board[i]['snails'].remove(snail)
                    self.dices.throwDices()
                    return

    def endgame(self):
        print('koniec gry')

    @app.route('/hotseat', methods=['POST', 'GET'])
    def gameHotseat(self):
        if request.method == 'POST':
            if request.form.get('submit_button', False) == 'throwDice':
                gra.dices.throwDices()
            elif request.form.get('dice', False) != False:
                dice = gra.dices.getDiceByColor(request.form.get('dice', False))
                gra.moveSnail(dice.color, dice.value)

        return render_template('hotseat.html', kostki=kostki, gra=gra)


class Player():
    def __init__(self, name):
        self.name = ""
        self.score = 0



class Snail():
    def __init__(self, color):
        self.id = random.choice(range(0, 100))
        self.color = color
        self.position = 0

    def __repr__(self):
        return "Ślimak (%s)" % (self.color)

class Dice():
    id
    color = None
    value = None
    fields = 'snail', 1, 2, 3, 4, 5

    def __init__(self, color):
        self.id = random.choice(range(0, 100))
        self.color = color
        self.rzut()

    def rzut(self):
        self.value = random.choice(self.fields)
        return self.value

class Dices():
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


@app.route('/', methods=['POST', 'GET'])
def index():
    gra = Game()

    if request.method == 'POST':
        if request.form.get('submit_button', False) == 'throwDice':
            gra.dices.throwDices()
        elif request.form.get('dice', False) != False:
            dice = gra.dices.getDiceByColor(request.form.get('dice', False))
            gra.moveSnail(dice.color, dice.value)

    return render_template('index.html', kostki=kostki, gra=gra)




if __name__ == '__main__':
    app.run(debug=True)