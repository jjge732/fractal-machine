import pygame as pg

# colors of board pieces 
WHITE  = pg.Color(255, 255, 255)
BLACK  = pg.Color(0, 0, 0)
RANDOM = pg.Color(255, 175, 50)

# class to make buttons 
class GameButton(pg.sprite.Sprite):

    def __init__(self, text, choose_color, x_pos, y_pos):
        pg.sprite.Sprite.__init__(self)
        self.width    = 100
        self.height   = 50 
        self.x_pos    = x_pos
        self.y_pos    = y_pos
        self.text     = text 
        self.font     = pg.font.SysFont("Arial", 25)
        self.textSurf = self.font.render(self.text, True, (255,255,255))
        self.image    = pg.Surface((self.width , self.height)) # size of the buttons 
        self.color    = choose_color # color of board piece 
        self.image.fill(self.color)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])
        pg.draw.rect(self.image, self.color, [self.x_pos , self.y_pos, self.width, self.height])
        self.rect = self.image.get_rect(topright = (self.x_pos, self.y_pos))

    def get_button_function(self):
        return self.text

    def update_size(self, width, height):
        self.width    = width
        self.height   = height
        self.image    = pg.Surface((self.width , self.height))
        self.image.fill(self.color)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])
        pg.draw.rect(self.image, self.color, [self.x_pos , self.y_pos, self.width, self.height])
        self.rect = self.image.get_rect(topright = (self.x_pos, self.y_pos))

    def update_function(self, new_text):
        self.text     = new_text    
        self.textSurf = self.font.render(self.text, True, (255,255,255))
        self.image    = pg.Surface((self.width , self.height)) # size of the buttons 
        self.image.fill(self.color)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])
        pg.draw.rect(self.image, self.color, [self.x_pos, self.y_pos, self.width, self.height])
        self.rect = self.image.get_rect(topright = (self.x_pos, self.y_pos))


    def change_font(self, font):
        self.font     = pg.font.Font("Jelly Crazies.ttf", 20) 
        self.textSurf = self.font.render(self.text, True, (255,255,255))
        self.image    = pg.Surface((self.width , self.height)) # size of the buttons 
        self.image.fill(self.color)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])
        pg.draw.rect(self.image, self.color, [self.x_pos , self.y_pos, self.width, self.height])
        self.rect = self.image.get_rect(topright = (self.x_pos, self.y_pos))


    def update_color(self, color):
        self.color    = choose_color # color of board piece 
        self.image.fill(self.color)
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.width/2 - W/2, self.height/2 - H/2])
        pg.draw.rect(self.image, self.color, [self.x_pos , self.y_pos, self.width, self.height])
        self.rect = self.image.get_rect(topright = (self.x_pos, self.y_pos))

