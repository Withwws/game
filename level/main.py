import pygame, sys
from settings import *
from level import Level
from menu import Menu


class Game: 
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.clock = pygame.time.Clock()
		self.menu = Menu()
		self.level = Level()

 
	def run(self):
		while True:
			self.menu.play()

if __name__ == '__main__':
	game = Game()
	game.run()