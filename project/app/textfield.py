import pygame as pg

# needed for pg.font.Font 
pg.init()

# the following source was referenced: 
# https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
WHITE        = pg.Color(255, 255, 255)
GREY         = pg.Color(89, 89, 89)
COLOR_INACTIVE = GREY
COLOR_ACTIVE = WHITE
FONT = pg.font.Font(None, 32)


class TextField:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def set_active(self):
        self.active = True
        self.color = COLOR_ACTIVE
    
    def set_inactive(self):
        self.active = False
        self.color = COLOR_INACTIVE
    
    def get_active_status(self):
        return self.active
    
    def user_typing(self, event):
        if event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode
        # render the text every time someone types something 
        self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

pg.quit()