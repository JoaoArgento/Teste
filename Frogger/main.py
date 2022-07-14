import pygame, sys
from pygame.locals import *
from settings import *
from player import Player
from car import Car
from random import choice, randint
from sprite import SimpleSprite, LongSprite

class AllSprites(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.offset = pygame.math.Vector2()
		self.bg = pygame.image.load("sprites/main/map.png").convert_alpha()
		self.fg = pygame.image.load("sprites/main/overlay.png").convert_alpha()

	def customize_draw(self):
		#mudando o offset 
		self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
		self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

		screen.blit(self.bg, -self.offset)

		for sprite in sorted(self.sprites(), key = lambda sprite:sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			screen.blit(sprite.image, offset_pos)

		screen.blit(self.fg, -self.offset)

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("I'm noob")
clock = pygame.time.Clock()

all_sprites = AllSprites()
obstacle_sprites = pygame.sprite.Group()

player = Player((2062, 3274), all_sprites, obstacle_sprites)

font = pygame.font.Font(None, 50)
text_surf = font.render(f'You won', True, (255,255,255))
text_rect = text_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))


#music 
music = pygame.mixer.Sound('audio/music.mp3')
music.play(loops = -1)

#timers 
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
pos_list = []

#sprite setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
	path = f'sprites/objects/simple/{file_name}.png'
	surf = pygame.image.load(path).convert_alpha()
	for pos in pos_list:
		SimpleSprite(surf, pos, [obstacle_sprites, all_sprites])

for file_name, pos_list in LONG_OBJECTS.items():
	path = f'sprites/objects/long/{file_name}.png'
	surf = pygame.image.load(path).convert_alpha()
	for pos in pos_list:
		LongSprite(surf, pos, [obstacle_sprites, all_sprites])	

while True:

	screen.fill((0,0,0))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == car_timer:
			random_pos = choice(CAR_START_POSITIONS)
			if random_pos not in pos_list:
				pos_list.append(random_pos)
				pos = (random_pos[0], random_pos[1] + randint(-8, 8))

				car = Car(pos, [obstacle_sprites,all_sprites])

			if len(pos_list) > 5:
				del pos_list[0]

	dt = clock.tick() / 1000

	if player.pos.y >= 1180:
		all_sprites.customize_draw()
		all_sprites.update(dt)

	else:
		screen.fill('teal')
		screen.blit(text_surf, text_rect)


	pygame.display.update()