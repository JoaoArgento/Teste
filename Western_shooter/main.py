import pygame
import sys
from pygame.locals import *
from settings import *
from player import Player
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet
from enemy import Coffin, Cactus

class AllSprites(pygame.sprite.Group):
	def __init__ (self):
		super().__init__()
		self.offset = pygame.math.Vector2()
		self.screen = pygame.display.get_surface()
		self.bg = pygame.image.load('graphics/other/bg.png').convert_alpha()

	def customize_draw(self, player):

		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT/ 2

		self.screen.blit(self.bg, -self.offset)
		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_rect = sprite.image.get_rect(center = sprite.rect.center)
			offset_rect.center -= self.offset
			self.screen.blit(sprite.image, offset_rect)

class Game:

	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Western Shooter')
		self.clock = pygame.time.Clock()

		self.bullet_surf = pygame.image.load("graphics/other/particle.png").convert_alpha()


		#groups 
		self.all_sprites = AllSprites()
		self.obstacles = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.monsters = pygame.sprite.Group()


		self.setup()
		self.music = pygame.mixer.Sound('sound/music.mp3')
		self.music.play(loops = -1)

	def create_bullets(self, pos, direction):
		Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets])
		


	def bullet_collision(self):

		for obstacle in self.obstacles.sprites():
			pygame.sprite.spritecollide(obstacle, self.bullets, True)

		for bullet in self.bullets.sprites():
			sprites = pygame.sprite.spritecollide(bullet, self.monsters, False, pygame.sprite.collide_mask)

			if sprites:
				bullet.kill()
				for sprite in sprites:
					sprite.damage()

		if pygame.sprite.spritecollide(self.player, self.bullets, True, pygame.sprite.collide_mask):
			self.player.damage()


	def setup(self):

		tmx_map = load_pygame('data/map.tmx')

		for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
			Sprite((x * 64,y * 64), surf, [self.obstacles, self.all_sprites])

		for obj in tmx_map.get_layer_by_name('Objects'):
			Sprite((obj.x, obj.y), obj.image, [self.obstacles, self.all_sprites])

		for obj in tmx_map.get_layer_by_name("Entities"):
			if obj.name == "Player":
				self.player = Player(pos = (obj.x,obj.y), 
					groups = self.all_sprites, 
					path = PATHS['player'], 
					collision_sprites = self.obstacles, 
					create_bullet = self.create_bullets)

			if obj.name == "Coffin":
				Coffin(pos = (obj.x,obj.y),
					   groups = [self.monsters,self.all_sprites], 
					   path = PATHS['coffin'], 
					   collision_sprites = self.obstacles, 
					   player = self.player
					)

			if obj.name == "Cactus":
				Cactus(pos = (obj.x, obj.y),
					   groups = [self.monsters,self.all_sprites],
					   path = PATHS['cactus'],
					   collision_sprites = self.obstacles,
					   player = self.player,
					   create_bullet = self.create_bullets)


	def run(self):
		while True:

			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

			dt = self.clock.tick() / 1000


			#update 
			self.bullet_collision()
			self.all_sprites.customize_draw(self.player)
			self.all_sprites.update(dt)

			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()
