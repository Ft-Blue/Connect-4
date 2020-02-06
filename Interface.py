import pygame
import sys

pygame.init()


class Interface:
	black = 0, 0, 0
	blue  = 0, 0, 255
	red   = 255, 0, 0
	green = 0, 255, 0
	player_clr = {0: black, 1: green, -1: red}

	def __init__(self, margin=20, radius=35):
		""" Initilize GUI by giving a margin (default 20px) and a radius for the circles (default 35) """
		self.margin         = margin
		self.radius         = radius
		self.header_offset  = 2*radius
		self.width          = 7*(2*radius+margin)
		self.height         = 6*(2*radius+margin)+self.header_offset
		self.screen         = pygame.display.set_mode((self.width, self.height))


	def draw(self, board):
		self.screen.fill(self.blue)
		header = pygame.Rect(0, 0, self.width, self.header_offset)
		pygame.draw.rect(self.screen, self.black, header)

		for i in range(len(board)):
			for j in range(len(board[i])):
				x = self.radius+self.margin/2 + j*(2*self.radius+self.margin)
				y = self.header_offset + self.radius+self.margin/2 + i*(2*self.radius+self.margin)
				x, y = int(x), int(y)
				if not 0 <= x <= self.width or not 0 <= y <= self.height: print(f"j {j} x {x} i {i} y {y}")
				#print("color", self.player_clr[board[i][j]])
				pygame.draw.circle(self.screen, self.player_clr[board[i][j]], (x, y), self.radius)

		pygame.display.flip()
		pygame.time.wait(500)

	def listen_event(self):
		""" Listen to game events """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				return None
			if event.type == pygame.MOUSEBUTTONUP:
				return pygame.mouse.get_pos()
		return None

	def close(self):
		pygame.quit()
