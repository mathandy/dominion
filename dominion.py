"""Parses Dominion (dominion.games) log to get decks.

To use: create text file in your Downloads folder called "log.txt"
and copy/paste the log into that file.  Then run this script with python
"""
from collections import deque
import re
from pathlib import Path


def parse_description_of_cards(cards_text):
    """Parses a text description of cards into a list of cards.
    E.g.
    Given '2 Coppers, a Gold and an Estate.', this function will return
    ['Copper', 'Copper', 'Gold', 'Estate']
    """
    card_removeables = ('.', ' a ', ' an ')
    card_descriptions = re.split(',|and', cards_text)

    cards = []
    for card in card_descriptions:

        # clean up card description
        for r in card_removeables:
            card = card.replace(r, '')
        card = card.strip()

        # get count if there's a number at the beginning
        try:
            n = int(card.split(' ')[0])
        except:
            n = 1

        cards += [card] * n
    return cards


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = ['Copper'] * 7 + ['Estate'] * 3
        self.hand = []
        self.discard_pile = []
        self.exile = []
        self.trash = []
        self.discarded = []
        self.ordered_gains = []

    def show(self):
        print(self.name)

        print('\n\tDeck:')
        for card in sorted(list(set(self.deck))):
            print(f'\t\t{card}: {self.deck.count(card)}')

        print('\n\tExile:')
        for card in sorted(list(set(self.exile))):
            print(f'\t\t{card}: {self.exile.count(card)}')

        print('\n\tTime-Ordered Gains:')
        for card in self.ordered_gains:
            print(f'\t\t{card}')

    def gain(self, description_of_cards):
        for card in parse_description_of_cards(description_of_cards):
            self.deck.append(card)
            self.ordered_gains.append(card)

    def exile_from_supply(self, description_of_cards):
        for card in parse_description_of_cards(description_of_cards):
            self.exile.append(card)

    def exile_from_deck(self, description_of_cards):
        for card in parse_description_of_cards(description_of_cards):
            self.deck.remove(card)
            self.exile.append(card)


class Game:
    def __init__(self, log):
        self.log = log.replace('\r', '')  # in case of windows line endings
        self.log_lines = self.log.split('\n')
        # get players
        token = " starts with "
        players = set(Player(line.split(token)[0]) for line in self.log_lines
                      if token in line)
        self.player_dict = dict((p.name, p) for p in players)

        # get cards
        buy_token = ' buys and gains'
        gain_token = ' gains'
        exile_token = ' exiles'
        for line in self.log.split('\n'):
            if buy_token in line:
                player, description_of_cards = line.split(buy_token)
                self.player_dict[player.strip()].gain(description_of_cards)

            elif gain_token in line:
                player, description_of_cards = line.split(gain_token)
                self.player_dict[player.strip()].gain(description_of_cards)

            elif exile_token in line:
                player, description_of_cards = line.split(exile_token)
                self.player_dict[player.strip()].exile_from_deck(description_of_cards)

    def show(self):
        for player in self.player_dict.values():
            player.show()


if __name__ == '__main__':
    log_path = Path().home() / 'Downloads' / 'log.txt'
    with log_path.open() as f:
        test_text = f.read()

    game = Game(log=test_text)
    game.show()


