import copy
import random

from classes.Dices import Dices
from classes.Player import Player
from classes.Penguin import Penguin


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
                    self.board[i - 1]['snails'].append(Penguin(color))
            if i == 7 or i == 11:
                self.board[i - 1]['type'] = 'grzyb'
            if i == 19:
                self.board[i - 1]['type'] = 'meta'

    def moveSnail(self, dice):
        color = dice.color
        position = dice.value
        for i, field in enumerate(self.board):
            for snail in field['snails']:
                if snail.color == color:

                    if position == 'snail':
                        position = 2
                    else:
                        self.dices.remove_dice(color)

                    x = i + position

                    if x >= 18:
                        x = 18

                    if x < 0:
                        x = 0

                    if (len(self.board[x]['snails']) != 0) and self.board[x]['type'] != 'grzyb':
                        self.currentPlayer.add_points(len(self.board[x]['snails']))
                        self.board[x - 1]['snails'] += self.board[x]['snails']
                        self.board[x]['snails'] = []

                    if self.board[x]['type'] == 'grzyb' or self.board[x]['type'] == 'meta':
                        self.currentPlayer.add_points(1)

                    self.board[x]['snails'].append(snail)
                    self.board[i]['snails'].remove(snail)

                    if x == 18:
                        self.endgame()
                        return True

                    self.dices.throw_dices()
                    self.nextPlayer()

                    return False

    def endgame(self):
        # adding points for players snails
        first = self.board[18]['snails']
        for i in range(17, -1, -1):
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
                    player.add_points(5)
        for snail in second:
            for player in self.players:
                if snail.color in player.snails:
                    player.add_points(2)
        for snail in last:
            for player in self.players:
                if snail.color in player.snails:
                    player.add_points(3)

        # calculating winner
        winning_players = sorted(self.players, key=lambda player: player.points, reverse=True)
        self.winner = [x for x in winning_players if x.points == winning_players[0].points]

        return

    def addPlayer(self, name, cpu=False):
        snails = self.pairs.pop(random.randint(0, len(self.pairs)-1))
        self.players.append(Player(name, snails, cpu))
        self.currentPlayer = self.players[0]

    def nextPlayer(self):
        self.currentPlayer = self.players[self.players.index(self.currentPlayer) - 1]
        return self.currentPlayer

    def cpu_next_move(self):

        dices_weights = []
        for dice in self.dices.current_dices:
            game = copy.deepcopy(self)
            player = game.currentPlayer
            game.moveSnail(dice)
            dice.weight = player.points
            dices_weights.append(dice)

        return sorted(dices_weights, key=lambda dice: dice.weight, reverse=True)[0]


