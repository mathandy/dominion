from collections import deque
import re


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

    def show(self):
        print(self.name)
        print('\tDeck:')
        for card in set(self.deck):
            print(f'\t\t{card}: {self.deck.count(card)}')
        print('\tExile:')
        for card in set(self.exile):
            print(f'\t\t{card}: {self.exile.count(card)}')

    def gain(self, description_of_cards):
        for card in parse_description_of_cards(description_of_cards):
            self.deck.append(card)

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
    with open('sample.txt') as f:
        test_text = f.read()

    game = Game(log=test_text)
    game.show()


