import pygame, sys
from pygame.locals import *
from random import randint, uniform


class Ship(pygame.sprite.Sprite):
	def __init__(self, groups):
		super().__init__(groups)
		self.image = pygame.image.load('sprites/ship.png').convert_alpha()

		self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

		#timer
		self.can_shoot = True
		self.shoot_time = None

		self.mask = pygame.mask.from_surface(self.image)

		self.laser_sound = pygame.mixer.Sound("sounds/laser.ogg")

	def laser_timer(self):
		if not self.can_shoot:
			current_time = pygame.time.get_ticks()

			if current_time - self.shoot_time > 500:
				self.can_shoot = True


	def input_position(self):
		pos = pygame.mouse.get_pos()
		self.rect.center = pos

	def laser_shoot(self):
		
		if pygame.mouse.get_pressed()[0] and self.can_shoot:
			self.can_shoot = False
			self.shoot_time = pygame.time.get_ticks()
			Laser(self.rect.midtop, laser_group)
			self.laser_sound.play()

	def meteor_collision(self):
		if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
			pygame.quit()
			sys.exit()


	def update(self):
		self.input_position()
		self.laser_shoot()
		self.laser_timer()
		self.meteor_collision()

class Laser(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)

		self.image = pygame.image.load("sprites/laser.png").convert_alpha()
		self.rect = self.image.get_rect(midbottom = pos)
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(0, -1)
		self.speed = 600
		self.mask = pygame.mask.from_surface(self.image)

		self.explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")

	def meteor_collision(self):
		if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
			self.kill()
			self.explosion_sound.play()

	def update(self):
		self.pos += self.direction * self.speed * dt 
		self.rect.topleft = (round(self.pos.x), round(self.pos.y))
		
		if self.rect.bottom < 0:
			self.kill()


		self.meteor_collision()

class Meteor(pygame.sprite.Sprite):
	def __init__(self, pos, groups):
		super().__init__(groups)
		#aleatorizando o tamanho do meteoro
		meteor_surf = pygame.image.load("sprites/meteor.png").convert_alpha()
		meteor_size = pygame.math.Vector2(meteor_surf.get_size()) * uniform(0.5, 1.5)
		self.scaled_surf = pygame.transform.scale(meteor_surf, (meteor_size))
		self.image = self.scaled_surf
		self.mask = pygame.mask.from_surface(self.image)

		self.rect = self.image.get_rect(center = pos)
		self.pos = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2(uniform(-0.5, 0.5),1)
		self.speed = randint(400, 600)

		#rotacionando os meteoros

		self.rotation = 0
		self.rotation_speed = randint(20,50)


	def rotate(self):
		self.rotation += self.rotation_speed * dt
		rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
		self.image = rotated_surf
		self.rect = self.image.get_rect(center = self.rect.center)
		self.mask = pygame.mask.from_surface(self.image)


	def update(self):
		self.pos += self.direction *self.speed * dt
		self.rect.topleft = (round(self.pos.x), round(self.pos.y))
		
		if self.rect.top > WINDOW_HEIGHT:
			self.kill()

		self.rotate()

class Score:
	def __init__(self):
		self.font = pygame.font.Font("sprites/subatomic.ttf", 50)

	def display(self):
		score_text = f'Score: {pygame.time.get_ticks() // 1000}'
		text_surf = self.font.render(score_text, True, (255,255,255))
		text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
		screen_surface.blit(text_surf, text_rect)
		pygame.draw.rect(screen_surface, ('white'), text_rect.inflate(30, 30), width = 8, border_radius = 5)


pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
screen_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space shooter")
clock = pygame.time.Clock()

#background 
bg_surf = pygame.image.load("sprites/background.png").convert_alpha()


#sprite groups
ship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()


#SPRITE CREATION
ship = Ship(ship_group)
score = Score()


meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 400)


#musica do jogo
bg_music = pygame.mixer.Sound("sounds/music.wav")
bg_music.play(loops = -1)
while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == meteor_timer:
			meteor_y_pos = randint(-150, -50)
			meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
			Meteor((meteor_x_pos, meteor_y_pos), meteor_group)

	dt = clock.tick() / 1000

	#desenhando o background 
	screen_surface.blit(bg_surf, (0,0))

	#desenhando os sprites
	ship_group.draw(screen_surface)
	ship_group.update()

	laser_group.draw(screen_surface)
	laser_group.update()

	meteor_group.draw(screen_surface)
	meteor_group.update()

	score.display()


	pygame.display.update()