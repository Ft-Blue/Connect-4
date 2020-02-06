from Game import Game
from Bot import *
from RLAgent import DQNAgent
from Interface import Interface
import random as rd
import keras

STEP_FORWARD	= 1
DISCOUNT		= 0.9

HUMAN_TURN		= 0
alice			= OneStepBot(0, STEP_FORWARD)
blue			= DQNAgent(0, DISCOUNT)
blue.model              = keras.models.load_model('./bob.model')

if HUMAN_TURN == 1:
	alice		= OneStepBot(-1, STEP_FORWARD)
elif HUMAN_TURN == -1:
	alice		= OneStepBot(1, STEP_FORWARD)
else:
	alice		= OneStepBot(-1, STEP_FORWARD)
	blue		= DQNAgent(1, DISCOUNT)

MARGIN			= 20
RADIUS			= 35
game			= Game()
interface		= Interface(margin=MARGIN, radius=RADIUS)

WIDTH			= 7*(2*RADIUS+MARGIN)
COL_UNIT		= WIDTH/7
count_turn		= 0


while not game.gameover:
	interface.draw(game.board)
	event = interface.listen_event()
	
	if game.player_turn == HUMAN_TURN:
		valid_move = False
		while type(event) != tuple or not valid_move:
			event = interface.listen_event()
			valid_move = type(event)==tuple and int(event[0]/COL_UNIT) in game.free_columns


		move = int(event[0]//COL_UNIT)
	elif game.player_turn == alice.turn:
		move = alice.make_move(game.board)
	elif game.player_turn == blue.turn:
		move = blue.make_move(game.board)
	
	game.place_piece(move)

	if game.gameover:
		print(f"Game over after {count_turn} turns. the winner is {game.winner}")
		interface.draw(game.board)
	else:
		game.next_player()
		count_turn += 1

	print(*game.board, sep='\n', end="\n\n===================\n\n")
