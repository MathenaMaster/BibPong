import sys
import pygame
from pygame.locals import * # for pygame key events
from menu import WinMenu
from enum import Enum
from threading import Thread, Lock
from returnthread import ReturnThread
import random

from pongmenu import pong_menu

BOT_BASE_SPEED = 30

UPGRADE = 5

HALF_BALL_SIZE = 10
DEFENDER_SIZE = 32

BASE_SPEED = 10

class VERTICAL_DIRECTION(Enum):
	TOP = 0
	DOWN = 1
	
	
class HORIZONTAL_DIRECTION(Enum):
	RIGHT = 0
	LEFT = 1
	
class PLAYER_TYPE(Enum):
	HUMAN = 0
	BOT = 1
	
class Orientation():
	def __init__(self, vert, horiz):
		self.vertical = vert
		self.horizontal = horiz
	
class Ball():
	
	def __init__(self, surfrect, ball_speed, clock):
		self.surfrect = surfrect
		self.ball_rect = pygame.Rect((0, 0), (20, 20))
		random_init = (random.random() * (self.surfrect.w / 2)) - (self.surfrect.w / 4)
		self.orientation = Orientation(VERTICAL_DIRECTION.TOP, HORIZONTAL_DIRECTION.RIGHT)
		self.ball_rect.center = ((self.surfrect.w / 2) + random_init, (self.surfrect.h / 2))
		self.ball_speed = ball_speed
		self.clock = clock
		self.__game_won = 0
		self.__win_lock = Lock()
		
	@property
	def game_won(self):
		with self.__win_lock:
			won = self.__game_won
		return won
	
	@game_won.setter
	def game_won(self, won):
		with self.__win_lock:
			self.__game_won = won
		
	def draw_itself(self, surface):
		surface.fill((255, 255, 255), self.ball_rect)

	
	def revert_horizon(self):
		if self.ball_rect.x <= 0:
			self.orientation.horizontal = HORIZONTAL_DIRECTION.RIGHT
		elif self.ball_rect.x >= self.surfrect.w - (2 * HALF_BALL_SIZE):
			self.orientation.horizontal = HORIZONTAL_DIRECTION.LEFT


	def revert_vertical(self, bot_rect, player_rect):
		player_collided = self.ball_rect.colliderect(player_rect)
		#bot_collided = self.ball_rect.colliderect(bot_rect)
		if self.ball_rect.y <=  DEFENDER_SIZE and player_collided:
			self.orientation.vertical = VERTICAL_DIRECTION.DOWN
		elif self.ball_rect.y <= DEFENDER_SIZE and not player_collided:
			return 1
		bot_collided = self.ball_rect.colliderect(bot_rect)
		if self.ball_rect.y > (self.surfrect.h - (DEFENDER_SIZE + (2 * HALF_BALL_SIZE)) - 1) and bot_collided:
			self.orientation.vertical = VERTICAL_DIRECTION.TOP
		elif self.ball_rect.y > (self.surfrect.h - (DEFENDER_SIZE + (2 * HALF_BALL_SIZE))) and not bot_collided:
			return 2
		return 0

		
	def ball_reorientation(self, player_rect, bot_rect):
		iswon = 0
		if self.orientation.horizontal == HORIZONTAL_DIRECTION.RIGHT:
			self.ball_rect.x += BASE_SPEED * self.ball_speed
		elif self.orientation.horizontal == HORIZONTAL_DIRECTION.LEFT:
			self.ball_rect.x -= BASE_SPEED * self.ball_speed
		if self.orientation.vertical == VERTICAL_DIRECTION.TOP:
			self.ball_rect.y -= BASE_SPEED * self.ball_speed
		elif self.orientation.vertical == VERTICAL_DIRECTION.DOWN:
			self.ball_rect.y += BASE_SPEED * self.ball_speed
		self.revert_horizon()
		iswon = self.revert_vertical(bot_rect, player_rect)
		return iswon
	


class Player:
	def __init__(self, player_type, center, ai_speed=1, ai_humanity=1):
		self.player_type = player_type
		self.rect = pygame.Rect((0, 0), (128,  32))
		self.rect.center = center
		self.bot_place = self.rect.w
		self.ai_speed = ai_speed
		self.ai_humanity = ai_humanity
	
	def draw_itself(self, surface):
		surface.fill((255, 255, 255), self.rect)
		
		
	def draw_bot(self, surface):
		self.rect.x = self.bot_place
		surface.fill((255, 255, 255), self.rect)

	def bot_move(self, ball_x):
		if self.bot_place > ball_x - ((BOT_BASE_SPEED + UPGRADE * self.ai_speed) / 2) and self.bot_place < ball_x + ((BOT_BASE_SPEED + UPGRADE * self.ai_speed) / 2):
			humanity = (((random.random() * 2) - 1) * (self.ai_humanity * BOT_BASE_SPEED)) #- ((BOT_BASE_SPEED * self.ai_humanity) / 2)
			self.bot_place = ball_x + humanity
		elif self.bot_place < ball_x - (BOT_BASE_SPEED + UPGRADE * self.ai_speed):
			self.bot_place += (BOT_BASE_SPEED + UPGRADE * self.ai_speed)
		elif self.bot_place > ball_x + (BOT_BASE_SPEED + UPGRADE * self.ai_speed):
			self.bot_place -= (BOT_BASE_SPEED + UPGRADE * self.ai_speed)


class Pong():
	
	def __init__(self, ball_speed, ai_speed, humanity):
		#pygame.init()
		# Resolution is ignored on Android
		self.surface = pong_menu.SCREEN
		self.clock = pygame.time.Clock()
		self.surfrect = self.surface.get_rect()
		self.player = Player(PLAYER_TYPE.HUMAN,  (self.surfrect.w / 2, DEFENDER_SIZE / 2))
		self.bot = Player(PLAYER_TYPE.BOT,  (self.surfrect.w * random.random(), self.surfrect.h - DEFENDER_SIZE / 2), ai_speed, humanity)
		self.ball = Ball(self.surfrect, ball_speed, self.clock)
		
		
	def control_loop(self):
		for ev in pygame.event.get():
			if ev.type == QUIT:
				pygame.quit()
				sys.exit()
			elif ev.type == pygame.MOUSEBUTTONDOWN:
				if self.player.rect.collidepoint(ev.pos):
                	# This is the starting point
					pygame.mouse.get_rel()
					return True, False
			elif ev.type == pygame.MOUSEBUTTONUP:
				return False, False
			#elif ev.type == pygame.K_RIGHT:
				#return True
			#elif ev.type == pygame.K_LEFT:
				#return True
			elif ev.type == pygame.K_ESCAPE or ev.type == pygame.K_AC_BACK:
				return False, True
		return True, False
		
		
	def play(self):
		orientation = 0
		player_th = Thread(target=self.player_job)
		bot_ai = Thread(target=self.bot_job)
		ball_th = ReturnThread(target=self.ball_job)
		player_th.start()
		bot_ai.start()
		ball_th.start()
		while orientation == 0:
			self.fill_pong_table()
			#pygame.display.flip()
			pygame.display.update()
			if not ball_th.is_alive():
				orientation = ball_th.join()
			if orientation > 0:
				self.ball.game_won = orientation # to do before both join to end their loop
				bot_ai.join()
				player_th.join()
				return orientation
		return orientation
		
	def player_job(self):
		while self.ball.game_won == 0:
			touched, quit_game = self.control_loop()
			if quit_game:
				return 
			if touched:
				self.apply_move()
			self.clock.tick(60)
				
	def bot_job(self):
		while self.ball.game_won == 0:
			self.bot.bot_move(self.ball.ball_rect.x)
			self.apply_bot_move()
			self.clock.tick(60)
			
	def ball_job(self):
		reorientation = 0
		while reorientation == 0:
			reorientation = self.ball.ball_reorientation(self.player.rect, self.bot.rect)
			self.clock.tick(60)
		return reorientation
		

	def fill_pong_table(self):
		self.surface.fill((0, 0, 0))
		self.bot.draw_bot(self.surface)
		self.player.draw_itself(self.surface)
		self.ball.draw_itself(self.surface)

	
	def apply_move(self):
		mouse_rel = pygame.mouse.get_rel()
		self.player.rect.move_ip(mouse_rel)
		self.player.rect.top = 0
		self.player.rect.clamp_ip(self.surfrect)


	def apply_bot_move(self):
		self.bot.rect.move_ip((self.bot.bot_place, self.surfrect.h - DEFENDER_SIZE))
		self.bot.rect.clamp_ip(self.surfrect)



def pong_out_loop():
	#while True:
	for ev in pygame.event.get():
		if ev.type == QUIT:
			pygame.quit()
			sys.exit()
			#return False
		elif ev.type == pygame.MOUSEBUTTONDOWN:
			return True
		elif ev.type == pygame.K_ESCAPE or ev.type == pygame.K_AC_BACK:
			return False



def pong_main(ball_speed, ai_speed, humanity):
	continue_playing = True
	while continue_playing:
		pong_game = Pong(ball_speed, ai_speed, humanity)
		lost_by = pong_game.play()
		pong_winning_menu = WinMenu(pong_game.surface)
		pong_winning_menu.draw_label_winner(lost_by)
		#pygame.display.update()
		pygame.display.flip()
		continue_playing = pong_out_loop()
		

# next function allows a stand alone of the pong without menu

if __name__ == '__main__':
	playing = True
	while playing:
		#pong = Pong(ball_speed, ai_speed, ai_humanity)
		pong = Pong(1, 2, 0)
		lost = pong.play()
		pong_menu = WinMenu(pong.surface)
		pong_menu.draw_label_winner(lost)
		#pygame.display.update()
		pygame.display.flip()
		playing = pong_out_loop()
		
		




