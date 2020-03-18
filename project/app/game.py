import pygame as pg
from boardpiece import BoardPiece
from gamebutton import GameButton

# colors of board pieces 
WHITE  = pg.Color(255, 255, 255)
BLACK  = pg.Color(0, 0, 0)
RANDOM = pg.Color(255, 175, 50)

# ---------------------------------------------------------------------
# UTILS 

# Create the BoardPieces and add them to the sprites_to_board group.
def makeBoard(length):
    sprites_to_board = pg.sprite.Group()

    if length == 3: # to make it more centered when clicking between 3x3 and 4x4 
                x_start_coord = 250
                y_start_coord = 180
    else: # to make it more 
        x_start_coord = 200 
        y_start_coord = 180

    for y in range(length):
        for x in range(length):
            

            # if you want a border to the rectangles, make x and y = 101, if not, 100
            sprites_to_board.add( BoardPiece( (x_start_coord + (x*101), y_start_coord + (y*101)) ) ) 
    return sprites_to_board

# matches RGB values to string values used for image processing 
def get_color_str(color):
    color      = str(color)
    color_dict = {   
    "(255, 255, 255, 255)" : "000", 
    "(0, 0, 0, 255)"       : "FFF"  }
    return color_dict.get(color)

# returns a 2-D array of the board, "000" for white, "FFF" for black 
def get_board_array(sprites, board_length):
    # colors are either (0, 0, 0, 255) or (255, 255, 255, 255)
    board_array = []
    inner_array = []
    counter     = 1
    for sprite in sprites:
        inner_array.append( get_color_str(sprite.get_piece_color()) )
        if (counter % board_length == 0 ):
            board_array.append(inner_array)
            inner_array = []
        counter += 1
    return board_array

# ---------------------------------------------------------------------
# MAIN

# Sets up the screen and runs the main game loop 
def main():

    # setting up the names needed for the display 
    screen = pg.display.set_mode((800, 800))
    font = pg.font.Font("Jelly Crazies.ttf", 35) 
    text = font.render('FRACTAL MACHINE', True, WHITE)
    textRect = text.get_rect() 
    textRect.center = (400, 100) 

    # creating the board 
    board_length     = 4
    sprites_to_board = makeBoard(board_length)

    # making the buttons 
    # the weird x values are to make one pixel of space between each button 
    # when making new  buttons, subtract 101 from the previous button 
    button_x = 650 
    button_y = 650 

    buttons         = pg.sprite.Group()
    three_by_three  = GameButton(     "3x3", RANDOM, (button_x - 404), button_y) 
    four_by_four    = GameButton(     "4x4", RANDOM, (button_x - 303), button_y)
    invert_button   = GameButton(  "Invert", RANDOM, (button_x - 202), button_y)
    clear_button    = GameButton(   "Clear", RANDOM, (button_x - 101), button_y)
    generate_button = GameButton("Generate", RANDOM,         button_x, button_y)
    buttons.add(three_by_three)
    buttons.add(four_by_four)
    buttons.add(clear_button)
    buttons.add(invert_button)
    buttons.add(generate_button)

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
                        if str(sprite.get_piece_color()) == "(255, 255, 255, 255)":
                                sprite.change_color(BLACK)
                        elif str(sprite.get_piece_color()) == "(0, 0, 0, 255)":
                            sprite.change_color(WHITE)

                for button in buttons:
                    # creating the invert button 
                    if button.rect.collidepoint(event.pos) and (button.get_button_function() == "Invert"):
                        for sprite in sprites_to_board:
                            if str(sprite.get_piece_color()) == "(255, 255, 255, 255)":
                                sprite.change_color(BLACK)
                            elif str(sprite.get_piece_color()) == "(0, 0, 0, 255)":
                                sprite.change_color(WHITE)
                    # the 3 by 3 button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "3x3"):
                        sprites_to_board = makeBoard(3)
                        board_length = 3 #reset the number to get correct dimensions for the 2-D array (game_array)
                    # the 4 by 4 button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "4x4"):
                        sprites_to_board = makeBoard(4)
                        board_length = 4
                    # the clear button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "Clear"):
                        for sprite in sprites_to_board:
                            sprite.change_color(WHITE)

        # sprites_to_board has to be updated before the screen.fill, also update buttons 
        sprites_to_board.update()
        buttons.update()

        # setting up the display 
        screen.fill((100, 100, 130))
        screen.blit(text, textRect) 
        sprites_to_board.draw(screen)
        buttons.draw(screen)

        # updates the whole display 
        pg.display.flip()

    # game_array is produced once the main game loop has ended
    game_array = get_board_array(sprites_to_board, board_length)

    for item in game_array:
        print(item)

# ---------------------------------------------------------------------
# invoke main & pygame 
pg.init()
main()
pg.quit()

