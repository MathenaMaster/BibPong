import sys
import pygame
from pygame.locals import *
from menu import WinMenu
from enum import Enum
import random

from threading import Thread

from pongmenu import pong_menu

BOT_BASE_SPEED = 50

UPGRADE = 20

HALF_BALL_SIZE = 10
DEFENDER_SIZE = 32

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
	
	def __init__(self, surfrect, ball_speed):
		self.surfrect = surfrect
		self.ball_rect = pygame.Rect((0, 0), (20, 20))
		self.orientation = Orientation(VERTICAL_DIRECTION.TOP, HORIZONTAL_DIRECTION.RIGHT)
		self.ball_rect.center = (self.surfrect.w / 2, self.surfrect.h / 2)
		self.ball_speed = ball_speed
		
		
	def draw_itself(self, surface):
		surface.fill((255, 255, 255), self.ball_rect)

	
	def revert_horizon(self):
		if self.ball_rect.x <= (HALF_BALL_SIZE + DEFENDER_SIZE):
			self.orientation.horizontal = HORIZONTAL_DIRECTION.RIGHT
		elif self.ball_rect.x >= self.surfrect.w - (HALF_BALL_SIZE + DEFENDER_SIZE):
			self.orientation.horizontal = HORIZONTAL_DIRECTION.LEFT


	def revert_vertical(self, bot_rect, player_rect):
		if self.ball_rect.y <=  DEFENDER_SIZE and self.ball_rect.colliderect(player_rect):
			self.orientation.vertical = VERTICAL_DIRECTION.DOWN
		elif self.ball_rect.y <= DEFENDER_SIZE and not self.ball_rect.colliderect(player_rect):
			return 1
		if self.ball_rect.y >= self.surfrect.h - (DEFENDER_SIZE + (2 * HALF_BALL_SIZE)) and self.ball_rect.colliderect(bot_rect):
			self.orientation.vertical = VERTICAL_DIRECTION.TOP
		elif self.ball_rect.y >= self.surfrect.h - (DEFENDER_SIZE + (2 * HALF_BALL_SIZE)) and not self.ball_rect.colliderect(bot_rect):
			return 2
		return 0

		
	def ball_reorientation(self, player_rect, bot_rect):
		iswon = 0
		if self.orientation.horizontal == HORIZONTAL_DIRECTION.RIGHT:
			self.ball_rect.x += 10 * self.ball_speed
		elif self.orientation.horizontal == HORIZONTAL_DIRECTION.LEFT:
			self.ball_rect.x -= 10 * self.ball_speed
		if self.orientation.vertical == VERTICAL_DIRECTION.TOP:
			self.ball_rect.y -= 10 * self.ball_speed
		elif self.orientation.vertical == VERTICAL_DIRECTION.DOWN:
			self.ball_rect.y += 10 * self.ball_speed
		self.revert_horizon()
		iswon = self.revert_vertical(bot_rect, player_rect)
		return iswon
	


class Player:
	def __init__(self, player_type, center, ai_speed=1):
		self.player_type = player_type
		self.rect = pygame.Rect((0, 0), (128,  32))
		self.rect.center = center
		self.bot_place = self.rect.w
		self.ai_speed = ai_speed
	
	def draw_itself(self, surface):
		surface.fill((255, 255, 255), self.rect)
		
		
	def draw_bot(self, surface):
		self.rect.x = self.bot_place
		surface.fill((255, 255, 255), self.rect)

	def bot_move(self, ball_x):
		if self.bot_place < ball_x - (BOT_BASE_SPEED + UPGRADE * self.ai_speed):
			self.bot_place += (BOT_BASE_SPEED + UPGRADE * self.ai_speed)
		elif self.bot_place > ball_x + (BOT_BASE_SPEED + UPGRADE * self.ai_speed):
			self.bot_place -= (BOT_BASE_SPEED + UPGRADE * self.ai_speed)
		else:
			humanity = random.random() % (2 * BOT_BASE_SPEED) - BOT_BASE_SPEED
			self.bot_place = ball_x + humanity


class Pong():
	
	def __init__(self, ball_speed, ai_speed):
		pygame.init()
		# Resolution is ignored on Android
		self.surface = pong_menu.SCREEN
		self.clock = pygame.time.Clock()
		self.surfrect = self.surface.get_rect()
		self.player = Player(PLAYER_TYPE.HUMAN,  (self.surfrect.w / 2, DEFENDER_SIZE / 2))
		self.bot = Player(PLAYER_TYPE.BOT,  (self.surfrect.w / 2, self.surfrect.h - DEFENDER_SIZE / 2), ai_speed)
		self.ball = Ball(self.surfrect, ball_speed)
		
		
	def control_loop(self):
		for ev in pygame.event.get():
			if ev.type == QUIT:
				pygame.quit()
			elif ev.type == pygame.MOUSEBUTTONDOWN:
				if self.player.rect.collidepoint(ev.pos):
                	# This is the starting point
					pygame.mouse.get_rel()
					return True
			elif ev.type == pygame.MOUSEBUTTONUP:
				return False
			#elif ev.type == pygame.K_RIGHT:
				#return True
			#elif ev.type == pygame.K_LEFT:
				#return True
		return True
		
		
	def play(self):
		touched = False
		orientation = 0
		bot_ai = Thread(target=self.bot_job)
		bot_ai.start()
		while True:
			touched = self.control_loop()
			orientation = self.ball.ball_reorientation(self.player.rect, self.bot.rect)
			self.clock.tick(60)
			if touched:
				self.apply_move()
				#self.clock.tick(60)
			self.fill_pong_table()
			pygame.display.flip()
			if orientation > 0:
				return orientation
		return orientation
				
	def bot_job(self):
		while True:
			self.bot.bot_move(self.ball.ball_rect.x)
			self.apply_bot_move()
			self.clock.tick(60)
		

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
		self.bot.rect.move_ip((self.bot.bot_place, 0))
		self.bot.rect.top = self.surfrect.h
		self.bot.rect.clamp_ip(self.surfrect)



def pong_out_loop():
	while True:
		for ev in pygame.event.get():
			if ev.type == QUIT:
				pygame.quit()
				return False
			elif ev.type == pygame.MOUSEBUTTONDOWN:
				return True



def pong_main(ball_speed, ai_speed):
	continue_playing = True
	while continue_playing:
		pong_game = Pong(ball_speed, ai_speed)
		pong_winning_menu = WinMenu(pong_game.surface)
		lost_by = pong_game.play()
		pong_winning_menu.draw_label_winner(lost_by)
		pygame.display.update()
		continue_playing = pong_out_loop()
		

# next function allows a stand alone of the pong without menu

if __name__ == '__main__':
	playing = True
	while playing:
		#pong = Pong(ball_speed, ai_speed)
		pong = Pong(1, 2)
		pong_menu = WinMenu(pong.surface)
		lost = pong.play()
		pong_menu.draw_label_winner(lost)
		pygame.display.update()
		playing = pong_out_loop()
		




