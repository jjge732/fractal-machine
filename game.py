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

# class to make buttons 
class GameButton(pg.sprite.Sprite):

    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((100, 50)) # size of the buttons 
        self.color = RANDOM # color of board piece 
        self.image.fill(self.color)
        # the following options:
        # top, left, bottom, right,topleft, bottomleft, topright, bottomright, midtop, midleft, midbottom, midright, center
        self.rect  = self.image.get_rect(topright = position)

# Create the BoardPieces and add them to the sprites_to_board group.
def makeBoard(length):
    sprites_to_board = pg.sprite.Group()

    for y in range(length):
        for x in range(length):
            # if you want a border to the rectangles, make x and y = 101
            sprites_to_board.add( BoardPiece( (x*101, y*101) ) ) 

    return sprites_to_board

def makeButton(position):
    button = pg.sprite.Group()
    button.add( GameButton(position))

# matches RGB values to string values used for image processing 
def get_color_str(color):

    color = str(color)

    color_dict = {

        "(255, 255, 255, 255)" : "000",
        "(0, 0, 0, 255)"       : "FFF" 
    }

    return color_dict.get(color)

# returns a 2-D array of the board, "000" for white, "FFF" for black 
def get_board_array(sprites, board_length):

    # colors are either (0, 0, 0, 255) or (255, 255, 255, 255)
    board_array, inner_array = [], []
    counter = 1
    for sprite in sprites:
        inner_array.append( get_color_str(sprite.get_piece_color()) )
        if (counter % board_length == 0 ):
            board_array.append(inner_array)
            inner_array = []
        counter += 1

    return board_array

# Sets up the screen and runs the main game loop 
def main():

    # Setting up the screen
    screen = pg.display.set_mode((800, 800))

    board_length = 4 

    sprites_to_board = makeBoard(board_length)

    # MAIN GAME LOOP 
    machine_running = True
    while machine_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                machine_running = False

            # If a mouse button was pressed.
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Iterate over the sprites in the group.
                for sprite in sprites_to_board:
                    # Check if the sprite's rect collides with the mouse pos.
                    if sprite.rect.collidepoint(event.pos):
                        # Finally change the color.
                        sprite.change_color(BLACK)


        sprites_to_board.update()
        screen.fill((100, 100, 130))

        # button = makeButton((700, 700))
        # button.draw(screen)
        sprites_to_board.draw(screen)


        pg.display.update()

    game_array = get_board_array(sprites_to_board, board_length)

    for item in game_array:
        print(item)

# -----------------------------------------
# invoke main 
main()




