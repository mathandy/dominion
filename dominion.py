"""Parses Dominion (dominion.games) log to get decks.

To use: create text file in your Downloads folder called "log.txt"
and copy/paste the log into that file.  Then run this script with python
"""
from collections import deque
import re
from pathlib import Path


LOG_PATH = Path().home() / 'Downloads' / 'log.txt'
SHOW_TRASH = False
SHOW_ORDERED_GANS = False


def parse_description_of_cards(cards_text):
    """Parses a text description of cards into a list of cards.
    E.g.
    Given '2 Coppers, a Gold and an Estate.', this function will return
    ['Copper', 'Copper', 'Gold', 'Estate']
    """
    card_removeables = ('.', ' a ', ' an ')
    card_descriptions = re.split(r',|\ and', cards_text)

    cards = []
    for card in card_descriptions:

        # clean up card description
        for r in card_removeables:
            card = card.replace(r, '')
        card = card.strip()

        # get count if there's a number at the beginning
        try:
            n = int(card.split(' ')[0])
            card = card[card.index(' ') + 1:].strip()
        except:
            n = 1

        cards += [card] * n

    # deal with plurals (in an overly simple way that probably won't work well)
    cards = [make_singular(card) for card in cards]
    return cards


def make_singular(card):
    """make a card name singular
    E.g. 'Coppers' -> 'Copper', or "Colonies" -> "Colony"
    """
    if card.endswith('ies'):
        return card[:-3] + 'y'
    elif card.endswith('s'):
        return card[:-1]
    return card


class Player:
    def __init__(self, name):
        self.name = name
        self.deck = ['Copper'] * 7 + ['Estate'] * 3
        self.hand = []
        self.exiled = []
        self.trashed = []
        self.discarded = []
        self.ordered_gains = []

    def show(self):
        print(self.name)

        print('\n\tDeck:')
        for card in sorted(list(set(self.deck))):
            print(f'\t\t{card}: {self.deck.count(card)}')

        print('\n\tExile:')
        for card in sorted(list(set(self.exiled))):
            print(f'\t\t{card}: {self.exiled.count(card)}')

        if SHOW_TRASH:
            print('\n\tTrash:')
            for card in sorted(list(set(self.trashed))):
                print(f'\t\t{card}: {self.trashed.count(card)}')

        if SHOW_ORDERED_GANS:
            print('\n\tTime-Ordered Gains:')
            for card in self.ordered_gains:
                print(f'\t\t{card}')

    def gain(self, description_of_cards):
        for card in parse_description_of_cards(description_of_cards):
            assert card
            self.deck.append(card)
            self.ordered_gains.append(card)

    def trash(self, description_of_cards):
        for card in parse_description_of_cards(description_of_cards):
            self.deck.remove(card)
            self.trashed.append(card)

    def exile_from_supply(self, description_of_cards):
        for card in parse_description_of_cards(description_of_cards):
            self.exiled.append(card)

    def exile_from_deck(self, description_of_cards):
        for card in parse_description_of_cards(description_of_cards):
            self.deck.remove(card)
            self.exiled.append(card)


class Game:
    def __init__(self, log):
        self.log = log.replace('\r', '')  # in case of windows line endings
        self.log_lines = self.log.split('\n')
        # get players
        token = " starts with "
        players = set(Player(line.split(token)[0])
                      for line in self.log_lines if token in line)
        self.player_dict = dict((p.name, p) for p in players)

        # get cards
        buy_token = ' buys and gains'
        gain_token = ' gains'
        exile_token = ' exiles'
        trash_token = ' trashes'
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

            elif trash_token in line:
                player, description_of_cards = line.split(trash_token)
                self.player_dict[player.strip()].trash(description_of_cards)

    def show(self):
        for player in self.player_dict.values():
            player.show()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Dominion (dominion.games) log parser.'
    )
    parser.add_argument('log_path', type=Path, nargs='?',
                        default=LOG_PATH,
                        help='Path to log file.')
    parser.add_argument('--show_trash', '-t', action='store_true',
                        help="Show players' trash piles.")
    parser.add_argument('--show_ordered_gains', '-o', action='store_true',
                        help="Show an ordered list of each players' gains")
    args = parser.parse_args()

    LOG_PATH = args.log_path
    SHOW_TRASH = args.show_trash
    SHOW_ORDERED_GANS = args.show_ordered_gains

    with LOG_PATH.open() as f:
        test_text = f.read()

    game = Game(log=test_text)
    game.show()
