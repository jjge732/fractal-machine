import pygame as pg

	# class to make the board pieces as sprites 
class ColorTile(pg.sprite.Sprite):

	def __init__(self, position, color):
	    pg.sprite.Sprite.__init__(self)
	    self.image = pg.Surface((30, 30))
	    self.color = color 
	    self.image.fill(self.color)
	    self.rect  = self.image.get_rect(topleft = position)

	def get_piece_color(self):
		return self.color

