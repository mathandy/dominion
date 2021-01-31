LINE_END_TOKEN = '\n'

# class Player:
# 	def __init__(self, na):

def get_players(text):
	token = " starts with "
	return set(line.split(token)[0] for line in text.split(LINE_END_TOKEN) if token in line)

def get_decks(text, players=None):
	if players is None:
		players = get_players(text)

	buy_token = ' buys and gains'
	gain_token = 'gains '
	card_removeables = ('.', ' a ', ' an ')

	decks = dict((p, []) for p in players)
	for line in text.split(LINE_END_TOKEN):
		buy_token = ' buys and gains'
		gain_token
		if buy_token in line:
			player, card = line.split(buy_token)
			for r in card_removeables:
				card = card.replace(r, '')
			decks[player].append(card)
	return decks


def show_decks(text):
	decks = get_decks(text)
	for player, deck in decks.items():
		print(player)
		for card in set(deck):
			print(f'\t{card}: {deck.count(card)}')


if __name__ == '__main__':
	with open('sample.txt') as f:
		test_text = f.read()

	players = get_players(test_text)
	print('players:', players, '\n')

	decks = get_decks(test_text)
	print('decks:', decks, '\n')

	show_decks(test_text)


