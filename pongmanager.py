
import pygame, sys

from pongmenu import pong_menu, window_height

from pong import pong_main

MIN_HUMANITY_LEVEL = 1
MIN_LEVEL = 1
MAX_LEVEL = 5


ball_speed = 1
ai_speed = 2
ai_humanity = 1

this = sys.modules[__name__]

def play():
	pygame.display.set_caption("Play")
	while True:
		PLAY_MOUSE_POS = pygame.mouse.get_pos()
		pong_menu.SCREEN.fill("black")
		pong_menu.make_label((window_height / 2, 200), "This is the play screen.", "white", 45)
		
		LAUNCH_GAME = pong_menu.make_button("PLAY", "white", "green", 75, (window_height / 2, 400))
		
		pong_menu.make_label((window_height / 2, 500), "Ball speed: {}".format(this.ball_speed), "white", 45)
		
		pong_menu.make_label((window_height / 2, 550), "AI speed: {}".format(this.ai_speed), "white", 45)
		
		pong_menu.make_label((window_height / 2, 600), "Humanity range: {}".format(this.ai_humanity), "white", 45)
		
		PLAY_BACK = pong_menu.make_button("BACK", "white", "green", 75, (window_height / 2, 750))
		
		pong_menu.buttons_update(PLAY_MOUSE_POS, [PLAY_BACK, LAUNCH_GAME])
		
		if pong_menu.menu_events(PLAY_MOUSE_POS, play_events, [PLAY_BACK, LAUNCH_GAME]):
			return
		#pong_menu.menu_events(PLAY_MOUSE_POS, play_events, [PLAY_BACK, LAUNCH_GAME])
			
		pygame.display.update()
		#pygame.display.flip()
	
	
def play_events(event, mouse_pos, buttons):
	if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()
	if event.type == pygame.MOUSEBUTTONDOWN:
		if buttons[0].checkForInput(mouse_pos):
			return True
		if buttons[1].checkForInput(mouse_pos):
			pong_main(this.ball_speed, this.ai_speed, this.ai_humanity)
			#return True #attention
	return False
	
	
def options():
	pygame.display.set_caption("Options")
	while True:
		OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
		
		pong_menu.SCREEN.fill("white")
		pong_menu.make_label((window_height / 2, 200), "This is the OPTIONS screen.", "black", 45)
		
		pong_menu.make_label((window_height / 5, 250), "Ball speed:", "black", 30)
		
		BALL_SPEED_DOWN = pong_menu.make_button("<", "black", "green", 150, (window_height / 3, 300))
		pong_menu.make_label((window_height / 2, 300), str(this.ball_speed), "black", 100)
		BALL_SPEED_UP = pong_menu.make_button(">", "black", "green", 150, (window_height * 2 / 3, 300))
		
		pong_menu.make_label((window_height / 5, 400), "AI speed:", "black", 30)
		
		AI_SPEED_DOWN = pong_menu.make_button("<", "black", "green", 150, (window_height / 3, 450))
		pong_menu.make_label((window_height / 2, 450), str(this.ai_speed), "black", 100)
		AI_SPEED_UP = pong_menu.make_button(">", "black", "green", 150, (window_height * 2 / 3, 450))
		
		pong_menu.make_label((window_height / 5, 550), "Humanity range:", "black", 30)
		
		HUMANITY_SPEED_DOWN = pong_menu.make_button("<", "black", "green", 150, (window_height / 3, 600))
		pong_menu.make_label((window_height / 2, 600), str(this.ai_humanity), "black", 100)
		HUMANITY_SPEED_UP = pong_menu.make_button(">", "black", "green", 150, (window_height * 2 / 3, 600))
		
		OPTIONS_BACK = pong_menu.make_button("BACK", "black", "green", 75, (window_height / 2, 700))
		
		pong_menu.buttons_update(OPTIONS_MOUSE_POS, [OPTIONS_BACK])
		
		pong_menu.no_color_update(OPTIONS_MOUSE_POS, [BALL_SPEED_DOWN, BALL_SPEED_UP, AI_SPEED_DOWN, AI_SPEED_UP, HUMANITY_SPEED_DOWN, HUMANITY_SPEED_UP])

		if pong_menu.menu_events(OPTIONS_MOUSE_POS, options_events, [OPTIONS_BACK, BALL_SPEED_DOWN, BALL_SPEED_UP, AI_SPEED_DOWN, AI_SPEED_UP, HUMANITY_SPEED_DOWN, HUMANITY_SPEED_UP]):
			return
			
		pygame.display.update()
		#pygame.display.flip()


def options_events(event, mouse_pos, buttons):
	if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()
	if event.type == pygame.MOUSEBUTTONDOWN:
		if buttons[0].checkForInput(mouse_pos):
			return True
		if buttons[1].checkForInput(mouse_pos):
			if this.ball_speed > MIN_LEVEL:
				this.ball_speed -= 1
		if buttons[2].checkForInput(mouse_pos):
			if this.ball_speed < MAX_LEVEL:
				this.ball_speed += 1
		if buttons[3].checkForInput(mouse_pos):
			if this.ai_speed > MIN_LEVEL:
				this.ai_speed -= 1
		if buttons[4].checkForInput(mouse_pos):
			if this.ai_speed < MAX_LEVEL:
				this.ai_speed += 1
		if buttons[5].checkForInput(mouse_pos):
			if this.ai_humanity > MIN_HUMANITY_LEVEL:
				this.ai_humanity -= 1
		if buttons[6].checkForInput(mouse_pos):
			if this.ai_humanity < MAX_LEVEL:
				this.ai_humanity += 1
	return False


def do_menu_events(event, mouse_pos,buttons):
	if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()
	if event.type == pygame.MOUSEBUTTONDOWN:
		if buttons[0].checkForInput(mouse_pos):
			play()
		if buttons[1].checkForInput(mouse_pos):
			options()
		if buttons[2].checkForInput(mouse_pos):
			pygame.quit()
			sys.exit()
	return False


def main_menu():
	pygame.display.set_caption("Menu")
	while True:
		pong_menu.SCREEN.fill("black")
		MENU_MOUSE_POS = pygame.mouse.get_pos()
		pong_menu.make_label((window_height / 2, 100), "MAIN MENU", "#b68f40", 100)
		
		PLAY_BUTTON = pong_menu.make_button("PLAY", "#d7fcd4", "white", 75, (window_height / 2, 200))
		OPTIONS_BUTTON = pong_menu.make_button("OPTIONS", "#d7fcd4", "white", 75, (window_height / 2, 400))
		QUIT_BUTTON = pong_menu.make_button("QUIT", "#d7fcd4", "white", 75, (window_height / 2, 600))
		
		pong_menu.buttons_update(MENU_MOUSE_POS, [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON])
		
		pong_menu.menu_events(MENU_MOUSE_POS, do_menu_events, [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON])
		
		pygame.display.update()
		#pygame.display.flip()
	
	
	