import pygame
from os import walk
import sys

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, collision_sprites):
		super().__init__(groups)
		self.import_assets()
		self.frame_index = 0
		self.status = 'down'
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.center)
		self.direction = pygame.math.Vector2()
		self.speed = 200
		self.collision_sprites = collision_sprites
		self.hitbox = self.rect.inflate(0, -self.rect.height /2)


	def collision(self, direction):

		if direction == "horizontal":
			for sprite in self.collision_sprites.sprites():
				if sprite.hitbox.colliderect(self.hitbox):

					if hasattr(sprite, 'name') and sprite.name == "car":
						pygame.quit()
						sys.exit()


					if self.direction.x > 0: #indo para a direita
						self.hitbox.right = sprite.hitbox.left
						self.pos.x = self.hitbox.centerx
						self.rect.centerx = self.hitbox.centerx
					if self.direction.x < 0: # indo para a esquerda
						self.hitbox.left = sprite.hitbox.right
						self.pos.x = self.hitbox.centerx
						self.rect.centerx = self.hitbox.centerx

		else:
			for sprite in self.collision_sprites.sprites():
				if sprite.hitbox.colliderect(self.hitbox):

					if hasattr(sprite, 'name') and sprite.name == "car":
						pygame.quit()
						sys.exit()
						

					if self.direction.y > 0: #indo para baixo
						self.hitbox.bottom = sprite.hitbox.top
						self.pos.y = self.hitbox.centery
						self.rect.centery = self.hitbox.centery

					if self.direction.y < 0: # indo para cima
						self.hitbox.top = sprite.hitbox.bottom
						self.pos.y = self.hitbox.centery
						self.rect.centery = self.hitbox.centery

	def import_assets(self):
		# path = "sprites/player/right/"
		# self.animation = [pygame.image.load(f'{path}{frame}.png').convert_alpha() for frame in range(4)]

		# for frame in range(4):
		# 	surf = pygame.image.load(f'{path}{frame}.png').convert_alpha()
		# 	self.animation.append(surf)

		#um import melhor 
		self.animations = {}

		for index, folder in enumerate(walk("sprites/player")):
			if index == 0:
				for name in folder[1]:
					self.animations[name] = []

			else:
				for file_name in folder[2]:
					path = folder[0].replace('\\', '/') + '/' + file_name
					surf = pygame.image.load(path).convert_alpha()
					key = folder[0].split('\\')[1]
					self.animations[key].append(surf)

	def move(self, dt):

		#normalize a vector  -> the length of the vector is going to be 1 
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()


		#horizontal movement + collision
		self.pos.x += self.direction.x * self.speed * dt
		self.hitbox.centerx = round(self.pos.x)
		self.rect.centerx = self.hitbox.centerx
		#horizontal collision.
		self.collision('horizontal')

		#vertical movement + collision
		self.pos.y += self.direction.y * self.speed * dt
		self.hitbox.centery = round(self.pos.y)
		self.rect.centery = self.hitbox.centery
		self.collision('vertical')

	def input(self):
		keys = pygame.key.get_pressed()


		if keys[pygame.K_a]:
			self.direction.x = -1
			self.status = 'left'

		elif keys[pygame.K_d]:
			self.direction.x = 1
			self.status = 'right'

		else:
			self.direction.x = 0

		if keys[pygame.K_w]:
			self.direction.y = -1
			self.status = 'up'

		elif keys[pygame.K_s]:
			self.direction.y = 1
			self.status = 'down'

		else:
			self.direction.y = 0

	def animate(self, dt):
		current_animation = self.animations[self.status]
		if self.direction.magnitude() != 0:
			self.frame_index += 10 * dt

			if self.frame_index >= len(current_animation):
				self.frame_index = 0 

		else:
			self.frame_index = 0

		self.image = current_animation[int(self.frame_index)]

	def restrict(self):
		if self.rect.left < 640:
			self.pos.x = 640 + self.rect.width /2
			self.hitbox.left = 640
			self.rect.left = 640

		if self.rect.right > 2560:
			self.pos.x = 2560 - self.rect.width /2
			self.hitbox.right = 2560
			self.rect.right = 2560

		if self.rect.bottom > 3500:
			self.pos.y = 3500 - self.rect.width /2
			self.rect.bottom = 3500
			self.hitbox.centery = self.rect.centery


	def update(self, dt):
		self.input()
		self.move(dt)
		self.animate(dt)
		self.restrict()
