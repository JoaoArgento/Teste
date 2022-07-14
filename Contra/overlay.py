import pygame

class Overlay:
	def __init__(self, player):
		self.player = player
		self.screen_surface = pygame.display.get_surface()
		self.health_surf = pygame.image.load('graphics/health.png').convert_alpha()
		self.health_width = self.health_surf.get_width()

	def display(self):
		
		for h in range(self.player.health):
			x_pos = (self.health_width + 4) * h + 10
			y_pos = 10
			self.screen_surface.blit(self.health_surf, (x_pos, y_pos))	