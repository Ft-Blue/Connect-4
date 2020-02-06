class Game:
	nb_rows = 6
	nb_cols = 7

	def __init__(self, initial_board=None, player_turn=1):
		if initial_board==None:
			self.board = [[0 for _ in range(self.nb_cols)] for __ in range(self.nb_rows)]
		else:
			self.board = initial_board

		self.player_turn = player_turn


	@property
	def free_columns(self):
		""" Returns a list of free columns indexes where a player can put a piece """
		return [j for j in range(self.nb_cols) if self.board[0][j]==0]


	def place_piece(self, col_index):
		""" Places a piece at the bottom of the grid if the place is available. Raises an exception if not
		Params:
		=======
			col_index: int, the index to the column where to place the piece
		"""
		if col_index in self.free_columns:
			bottom_free_row = max(filter(lambda row: self.board[row][col_index]==0, range(self.nb_rows)))
			self.board[bottom_free_row][col_index] = self.player_turn
		else:
			raise


	def next_player(self):
		""" Changes the value of player_turn """
		self.player_turn *= -1

	@staticmethod
	def check_diag_1(board):
		""" Checks the lower-right (and upper-left) diagonal of each position to see if four are connected
		Params:
		=======
			board: list of 1D-lists, contains the game board positions
		Return:
		=======
			Boolean value: True if any of the three winning conditions is verified, else False
		"""
		for i in range(Game.nb_rows-3):
			for j in range(Game.nb_cols-3):
				is_over = True
				m = board[i][j]
				for k in range(4):
					if board[i+k][j+k] != m: is_over = False
				if m != 0 and is_over: return True
		return False

	@staticmethod
	def check_diag_2(board):
		""" Checks the upper-right (and lower-left) diagonal of each position to see if four are connected
		Params:
		=======
			board: list of 1D-lists, contains the game board positions
		Return:
		=======
			Boolean value: True if any of the three winning conditions is verified, else False
		"""
		for i in range(Game.nb_rows-3):
			for j in range(3, Game.nb_cols):
				is_over = True
				m = board[i][j]
				for k in range(4):
					if board[i+k][j-k] != m: is_over = False
				if m != 0 and is_over: return True
		return False

	@staticmethod
	def check_verticals(board):
		""" Checks below (and above) each position to see if four are connected
		Params:
		=======
			board: list of 1D-lists, contains the game board positions
		Return:
		=======
			Boolean value: True if any of the three winning conditions is verified, else False
		"""
		for i in range(Game.nb_rows-3):
			for j in range(Game.nb_cols):
				is_over = True
				m = board[i][j]
				for k in range(4):
					if board[i+k][j] != m: is_over = False
				if m != 0 and is_over: return True
		return False

	@staticmethod
	def check_horizontals(board):
		""" Checks right (and left) side of each position to see if four are connected
		Params:
		=======
			board: list of 1D-lists, contains the game board positions
		Return:
		=======
			Boolean value: True if any of the three winning conditions is verified, else False
		"""
		for i in range(Game.nb_rows):
			for j in range(Game.nb_cols-3):
				is_over = True
				m = board[i][j]
				for k in range(4):
					if board[i][j+k] != m: is_over = False
				if m != 0 and is_over: return True
		return False

	@staticmethod
	def check_win(board):
		""" Check all three winning conditions (horizontally, vertically and diagonally)
		Params:
		=======
			board: list of 1D-lists, contains the game board positions
		Return:
		=======
			Boolean value: True if any of the three winning conditions is verified, else False
		"""

		return any([Game.check_diag_1(board), Game.check_diag_2(board), Game.check_verticals(board), Game.check_horizontals(board)])

	@property
	def gameover(self):
		return any([self.free_columns == [], self.check_win(self.board)])

	@property
	def winner(self):
		if self.gameover:
			# if a player won the game, return its number
			if self.check_win(self.board):
				return self.player_turn
			# if the grid is full, it s a draw
			return 0
		# if it s not game over, return None
		return None
