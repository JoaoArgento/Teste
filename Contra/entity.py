import pygame
from settings import *
from os import walk 
from math import sin

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, path, groups, shoot):
		super().__init__(groups)
		self.import_assets(path)
		self.frame_index = 0
		self.status = 'right'

		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.old_rect = self.rect.copy()

		#posição
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2()
		self.speed = 400
		self.z = LAYERS['Level']

		self.shoot = shoot
		self.duck = False
		#bullet timer
		self.can_shoot = True 
		self.shoot_time = None
		self.cooldown = 200

		#health
		self.health = 3 

		self.is_vulnerable = True 
		self.hit_time = None 
		self.invul_duration = 500
		self.mask = pygame.mask.from_surface(self.image)

		self.hit_sound = pygame.mixer.Sound('audio/hit.wav')
		self.hit_sound.set_volume(0.2)
		self.shoot_sound = pygame.mixer.Sound("audio/bullet.wav")
		self.shoot_sound.set_volume(0.2)

	def blink(self):
		if not self.is_vulnerable:
			if self.wave_value():
				mask = pygame.mask.from_surface(self.image)
				white_surf = mask.to_surface()
				white_surf.set_colorkey((0,0,0))
				self.image = white_surf


	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: 
			return True 
		else:
			return False


	def damage(self):
		if self.is_vulnerable:
			self.health -= 1
			self.is_vulnerable = False
			self.hit_time = pygame.time.get_ticks()
			self.hit_sound.play()

	def check_death(self):
		if self.health <= 0:
			self.kill()

	def shoot_timer(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()
			if current_time - self.shoot_time > self.cooldown:
				self.can_shoot = True


	def invul_timer(self):
		if not self.is_vulnerable:
			current_time = pygame.time.get_ticks()
			if current_time - self.hit_time > self.invul_duration:
				self.is_vulnerable = True

	def import_assets(self, path):
		self.animations = {}

		for index, folder in enumerate(walk(path)):
			if index == 0:
				for name in folder[1]:
					self.animations[name] = []

			else:
				for file_name in sorted(folder[2], key = lambda string: int(string.split('.')[0])):
					path = folder[0].replace('\\', '/') + '/' + file_name
					surf = pygame.image.load(path).convert_alpha()
					key = folder[0].split('\\')[1]
					self.animations[key].append(surf)

	def animate(self, dt):
		current_animation = self.animations[self.status]

		self.frame_index += 7 * dt

		if self.frame_index > len(current_animation):
			self.frame_index = 0

		self.image = current_animation[int(self.frame_index)]
		self.mask = pygame.mask.from_surface(self.image)
	def update(self,dt):
		pass

