from flask import Flask, render_template, request, redirect, session, flash, url_for
import random, copy, itertools, uuid

app = Flask(__name__)
app.secret_key = '1221'

games = {}
gameCodes = []

class Game:
    def __init__(self):
        self.colors = 'niebieski', 'żółty', 'fioletowy', 'zielony', 'czerwony'
        self.pairs = [['czerwony', 'żółty'], ['niebieski', 'czerwony'], ['żółty', 'zielony'], ['zielony', 'fioletowy'], [
            'fioletowy', 'niebieski']]
        self.board = []
        self.players = []
        self.currentPlayer = None
        self.winner = None
        self.dices = Dices()

        for i in range(1, 20):
            self.board.append({'type': "", 'value': i, 'snails': []})
            if i == 1:
                self.board[i - 1]['type'] = 'start'
                for color in self.colors:
                    self.board[i - 1]['snails'].append(Snail(color))
            if i == 7 or i == 11:
                self.board[i - 1]['type'] = 'grzyb'
            if i == 19:
                self.board[i - 1]['type'] = 'meta'

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

                    if x < 0:
                        x = 0

                    if (len(self.board[x]['snails']) != 0) and self.board[x]['type'] != 'grzyb':
                        self.currentPlayer.addPoints(len(self.board[x]['snails']))
                        self.board[x - 1]['snails'] += self.board[x]['snails']
                        self.board[x]['snails'] = []

                    if self.board[x]['type'] == 'grzyb':
                        self.currentPlayer.addPoints(1)

                    self.board[x]['snails'].append(snail)
                    self.board[i]['snails'].remove(snail)

                    if x == 18:
                        self.endgame()

                    self.dices.throwDices()
                    self.nextPlayer()

                    return

    def endgame(self):
        # adding points for players snails
        first = self.board[18]['snails']
        for i in range(17, -1, -1):
            print(i)
            if len(self.board[i]['snails']) != 0:
                second = self.board[i]['snails']
                break
        for i in range(0, 18):
            if len(self.board[i]['snails']) != 0:
                last = self.board[i]['snails']
                break

        for snail in first:
            for player in self.players:
                if snail.color in player.snails:
                    player.addPoints(5)
        for snail in second:
            for player in self.players:
                if snail.color in player.snails:
                    player.addPoints(2)
        for snail in last:
            for player in self.players:
                if snail.color in player.snails:
                    player.addPoints(3)

        # calculating winner
        score = (max([x.points for x in self.players]))
        for player in self.players:
            if player.points == score:
                self.winner = player.name

        return

    def addPlayer(self, name, cpu=False):
        snails = self.pairs.pop(random.randint(0, len(self.pairs)-1))
        self.players.append(Player(name, snails))
        self.currentPlayer = self.players[0]

    def nextPlayer(self):
        self.currentPlayer = self.players[self.players.index(self.currentPlayer) - 1]


class Player:
    def __init__(self, name, snails):
        self.name = name
        self.points = 0
        self.snails = snails

    def __repr__(self):
        return self.name

    def addPoints(self, points):
        self.points += points


class Snail:
    def __init__(self, color):
        self.id = random.choice(range(0, 100))
        self.color = color
        self.position = 0

    def __repr__(self):
        return "Ślimak (%s)" % (self.color)


class Dice:
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


def check():
    if 'key' not in session or 'games' not in globals():
        return True
    return False


@app.route('/')
def index():
    if 'key' not in session:
        session['key'] = uuid.uuid4()
    return render_template('index.html')


@app.route('/hotseat_players', methods=['POST', 'GET'])
def hotseatPlayers():
    if check(): return redirect('/')
    if request.method == 'POST':
        game = games[session['key']] = Game()
        names = request.form['players'].split(',')
        if len(names) > 5 or len(names[0]) == 0:
            flash('Liczba graczy musi mieścić się w zakresie 1-5!', 'warning')
            return redirect(url_for('hotseatPlayers'))
        for name in names:
            game.addPlayer(name.strip())

        return redirect('/snails_cards')

    return render_template('hotseat_players.html')

@app.route('/snails_cards')
def snailCards():
    if check() or session['key'] not in games: return redirect('/')
    gra = games[session['key']]
    return render_template('snails_cards.html', gra=gra)


@app.route('/hotseat', methods=['POST', 'GET'])
def hotseat():
    if check() or session['key'] not in games: return redirect('/')
    gra = games[session['key']]
    kostki = gra.dices
    if gra.winner:
        render_template('endgame.html', gra=gra)

    if request.method == 'POST':
        if isinstance(request.form['dice'], str):
            dice = gra.dices.getDiceByColor(request.form.get('dice', False))
            gra.moveSnail(dice.color, dice.value)

    return render_template('game.html', kostki=kostki, gra=gra)

@app.route('/new_online', methods=['POST', 'GET'])
def new_online():
    if check(): return redirect('/')

    if request.method == 'POST':
        call = request.form.get('submit_button', False)
        name = request.form.get('player-name', False)
        if name is None or name == "":
            flash('Wpisz proszę swoje imię.')
            return render_template('new_online.html')
        name = name.strip()
        session['player'] = name
        if call == 'new-room':
            game_code = random.choice([x for x in range(9999) if x not in gameCodes])
            session['online_game'] = str(game_code)
            games[session['online_game']] = [name]
        if call == 'join-room':
            session['online_game'] = str(request.form.get('game-code', False))
            if session['online_game'] not in games:
                flash('Nie znaleziono pokoju o takim kodzie, wpisz kod ponownie lub stwórz nowy pokój.')
                return render_template('new_online.html')
            if name in games[session['online_game']]:
                flash('Ta nazwa jest już zajęta przez innego gracza w tym pokoju, wybierz inną.')
                return render_template('new_online.html')
            games[session['online_game']].append(name)
        return redirect('lobby')

    return render_template('new_online.html')

@app.route('/lobby', methods=['POST', 'GET'])
def lobby():
    players = games[session['online_game']]
    if isinstance(players, Game):
        return redirect(url_for('online'))
    game_code = session['online_game']
    return render_template('lobby.html', players=players, game_code=game_code)

@app.route('/start_online')
def start_online():
    if not isinstance(games[session['online_game']], Game):
        players = copy.deepcopy(games[session['online_game']])
        game = games[session['online_game']] = Game()
        for player in players:
            game.addPlayer(player)

    return redirect('online')

@app.route('/online', methods=['POST', 'GET'])
def online():
    if check() or session['online_game'] not in games: return redirect('/')
    game = games[session['online_game']]
    me = session['player']
    kostki = game.dices
    if game.winner:
        return render_template('endgame.html', gra=game)

    if me == game.currentPlayer.name:
        if request.method == 'POST':
            if isinstance(request.form['dice'], str):
                dice = game.dices.getDiceByColor(request.form.get('dice', False))
                game.moveSnail(dice.color, dice.value)

    return render_template('game.html', kostki=kostki, gra=game)

if __name__ == '__main__':
    app.run(debug=True)
