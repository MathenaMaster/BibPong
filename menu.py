import pygame, time

from pongmenu import pong_menu, window_height


class WinMenu():
	def __init__(self, base_screen):
		self.screen = base_screen
		self.font = pygame.font.SysFont("arialblack", 100)

	def draw_label_winner(self, lost):
		self.screen.fill("black")
		if lost == 0:
			pong_menu.make_label((window_height / 2, 200), "Game aborted", "white", 100)
		if lost == 1:
			pong_menu.make_label((window_height / 2, 200), "Bot won", "white", 100)
		if lost == 2:
			pong_menu.make_label((window_height / 2, 200), "Player won", "white", 100)
		pygame.display.flip()
		#pygame.display.update()
		
		time.sleep(3)
		
		#time.sleep(3)
		