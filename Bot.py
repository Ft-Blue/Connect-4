import random as rd
from Game import Game
from copy import deepcopy


class BasicBot:
	def __init__(self, turn):
		self.turn = turn


	@staticmethod
	def free_columns(board):
		""" Returns a list of free columns where a player can put a piece """
		return [j for j in range(len(board[0])) if board[0][j] == 0]


	def make_move(self, board):
		available_moves = self.free_columns(board)
		return rd.choice(available_moves)


class OneStepBot(BasicBot):
	def __init__(self, turn, step_forward):
		super().__init__(turn)
		self.step_forward = step_forward


	def make_move(self, board):
		states = self.generate_future_states(board)
		win_states = list(filter(lambda state: Game.check_win(state[1]), states))
		if win_states:
			return win_states[0][0]
		return super().make_move(board)


	def generate_future_states(self, board):
		available_moves = self.free_columns(board)
		states = [[None, deepcopy(board)] for _ in range(len(available_moves))]
		for i, move in enumerate(available_moves):
			bottom_free_row = max(filter(lambda row: board[row][move]==0, range(Game.nb_rows)))
			states[i][0] = move
			states[i][1][bottom_free_row][move] = self.turn
		
		return states