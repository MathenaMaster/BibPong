
import pygame, sys
from button import Button


window_height = 720
window_width = 1280

pc_shift_bot_display = 300


class PongMenu:

	def __init__(self):
		pygame.init()
		self.SCREEN = pygame.display.set_mode((window_height, window_width - pc_shift_bot_display))
		pygame.display.set_caption("Pong Menu")
		
		self.BG = pygame.Color("black")


	def get_font(self, size):
		#return pygame.font.Font(None, size)
		return pygame.font.SysFont("arialblack", size)
		
	
	def make_label(self, pos, label_text, color, size):
		TEXT = self.get_font(size).render(label_text, True, color)
		RECT = TEXT.get_rect(center=pos)
		self.SCREEN.blit(TEXT, RECT)


	def make_button(self, text_input, base_color, hovering_color, size, pos):
		BUTTON = Button(image=None, pos=pos, text_input=text_input, font=self.get_font(size), base_color=base_color, hovering_color=hovering_color)
		return BUTTON
		

	def nolist_buttons_update(self,MENU_MOUSE_POS, *buttons):
		for button in buttons:
			button.changeColor(MENU_MOUSE_POS)
			button.update(self.SCREEN)


	def buttons_update(self, MENU_MOUSE_POS, buttons):
		for button in buttons:
			button.changeColor(MENU_MOUSE_POS)
			button.update(self.SCREEN)
		
	def no_color_update(self, MENU_MOUSE_POS, buttons):
		for button in buttons:
			button.update(self.SCREEN)

		
	def menu_events(self, MENU_MOUSE_POS, func, buttons):
		pygame.init()
		for event in pygame.event.get():
			if func(event, MENU_MOUSE_POS, buttons):
				return True
		return False


pong_menu = PongMenu()

