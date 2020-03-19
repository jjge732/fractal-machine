import pygame as pg

# colors of board pieces 
WHITE  = pg.Color(255, 255, 255)
BLACK  = pg.Color(0, 0, 0)
RANDOM = pg.Color(255, 175, 50)


# class to make the board pieces as sprites 
class BoardPiece(pg.sprite.Sprite):

    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((100, 100)) # size of the a single board piece  
        self.color = WHITE # color of board piece 
        self.image.fill(self.color)
        # topleft made the most sense out of the following options:
        # top, left, bottom, right,topleft, bottomleft, topright, bottomright, midtop, midleft, midbottom, midright, center
        self.rect  = self.image.get_rect(topleft = position)

    # function to change the color of the sprite, used in game loop 
    def change_color(self, color): 
        self.color = color 
        self.image.fill(self.color)

    def get_piece_color(self):
        return self.color