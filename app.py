from flask import Flask, render_template, request, redirect, session, flash, url_for
import random, copy, itertools, uuid

from classes.Game import Game

app = Flask(__name__)
app.secret_key = '1221'

games = {}
gameCodes = []


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
        print(gra.winner)
        return render_template('endgame.html', gra=gra)

    if request.method == 'POST':
        if isinstance(request.form['dice'], str):
            dice = gra.dices.get_dice_by_color(request.form.get('dice', False))
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
                dice = game.dices.get_dice_by_color(request.form.get('dice', False))
                game.moveSnail(dice.color, dice.value)

    return render_template('game.html', kostki=kostki, gra=game, player_name=me)

if __name__ == '__main__':
    app.run(debug=True)
