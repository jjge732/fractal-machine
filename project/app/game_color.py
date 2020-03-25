import pygame as pg
from boardpiece import BoardPiece
from gamebutton import GameButton
from image_editor import Image
from colortile import ColorTile
import pandas as pd 

# colors of board pieces 
WHITE        = pg.Color(255, 255, 255)
BLACK        = pg.Color(0, 0, 0)
RANDOM       = pg.Color(255, 175, 50)
OTHER        = pg.Color(175, 175, 175)
SCREEN_COLOR = pg.Color(100, 100, 130)

# ---------------------------------------------------------------------
# SETTING UP THE COLORS 
# importing the color dataframe 
# RGB_Hex.xlsx was created by webscrap_forcolors.py

color_df = pd.read_excel('RGB_Hex.xlsx')

colors_list = []

for i in range(color_df.shape[0]):
    temp_color = str(color_df.iloc[i, 0])
    temp_color = temp_color.replace("(", "")
    temp_color = temp_color.replace(")", "")
    temp_list  = temp_color.split(",")
    temp_rgb   = pg.Color(int(temp_list[0]), int(temp_list[1]), int(temp_list[2]))
    colors_list.append(temp_rgb)

color_dict = dict()
for color, i in zip(colors_list, range(color_df.shape[0])):
    temp_hex = str(color_df.iloc[i, 1])
    color_dict[str(color)] = temp_hex

# ---------------------------------------------------------------------
# UTILS 


# Create the BoardPieces and add them to the sprites_to_board group.
def makeBoard(length):
    sprites_to_board = pg.sprite.Group()
    x_start_coord    = 200 
    y_start_coord    = 180
    # to make it more centered when clicking between 3x3 and 4x4 
    if length == 3:
        x_start_coord = 250
    for y in range(length):
        for x in range(length):
            # if you want a border to the rectangles, make x and y = 101, if not, 100
            sprites_to_board.add( BoardPiece( (x_start_coord + (x*101), y_start_coord + (y*101)) ) ) 
    return sprites_to_board

#create a color board 
def makeColorBoard(color_list):
    colors_to_board = pg.sprite.Group()
    x_start_coord    = 650
    y_start_coord    = 180
    count = 0 
    for y in range(10):
        for x in range(10):
            colors_to_board.add( ColorTile( (x_start_coord + (x*25), y_start_coord + (y*25)), color_list[count]) ) 
            count+=1
    return colors_to_board

# matches RGB values to string values used for image processing 
def get_color_str(color, color_dict):
    color      = str(color)
    return color_dict.get(color)

# returns a 2-D array of the board, "000" for white, "FFF" for black 
def get_board_array(sprites, board_length):
    # colors are either (0, 0, 0, 255) or (255, 255, 255, 255)
    board_array = []
    inner_array = []
    counter     = 1
    for sprite in sprites:
        inner_array.append( get_color_str(sprite.get_piece_color(), color_dict) )
        if (counter % board_length == 0 ):
            board_array.append(inner_array)
            inner_array = []
        counter += 1
    return board_array

# ---------------------------------------------------------------------
# MAIN

# Sets up the screen and runs the main game loop 
def main():

    pg.init()

    # setting up the names needed for the display 
    screen   = pg.display.set_mode((1000, 800))
    font     = pg.font.Font("Jelly Crazies.ttf", 35) 
    text     = font.render('FRACTAL MACHINE', True, WHITE)
    textRect = text.get_rect() 
    textRect.center  = (400, 100) 

    # creating the board 
    board_length     = 4
    sprites_to_board = makeBoard(board_length)
    colors_to_board  = makeColorBoard(colors_list)

    # making the buttons 
    # the weird x values are to make one pixel of space between each button 
    # when making new  buttons, subtract 101 from the previous button 
    button_x = 650 
    button_y = 650 

    buttons         = pg.sprite.Group()
    three_by_three  = GameButton(        "3x3",       RANDOM, (button_x - 404),         button_y) 
    four_by_four    = GameButton(        "4x4",       RANDOM, (button_x - 303),         button_y)
    invert_button   = GameButton(     "Invert",       RANDOM, (button_x - 202),         button_y)
    clear_button    = GameButton(      "Clear",       RANDOM, (button_x - 101),         button_y)
    exit_button     = GameButton(       "EXIT", SCREEN_COLOR, (button_x - 530), (button_y + 100))
    number_button   = GameButton(          "1", SCREEN_COLOR,  (button_x + 51),         button_y)
    generate_button = GameButton( "Fractalify",       RANDOM,         button_x,         button_y)
    fractal_buttton = GameButton("GET FRACTAL", SCREEN_COLOR, (button_x + 130), (button_y + 100))

    exit_button.change_font("Jelly Crazies.ttf")
    fractal_buttton.change_font("Jelly Crazies.ttf")
    number_button.update_size(50,50)
    fractal_buttton.update_size(295,50)

    buttons.add( three_by_three  )
    buttons.add( four_by_four    )
    buttons.add( clear_button    )
    buttons.add( invert_button   )
    buttons.add( generate_button )
    buttons.add( exit_button     ) 

    # counter for the generate buttton
    click_counter = 0
    get_fractal_clicked = False

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
                    # exit button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "EXIT"):
                        machine_running = False
                    # fractalify button
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "Fractalify"):
                        click_counter += 1
                        if click_counter == 1:
                            buttons.add(number_button)
                            buttons.add(fractal_buttton)
                        # where the limit is set 
                        if click_counter <= 5: 
                            number_button.update_function(str(click_counter))
                        else:
                            click_counter = 0
                            buttons.remove(number_button)
                            buttons.remove(fractal_buttton)
                    # get fract button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "GET FRACTAL"):
                        get_fractal_clicked = True 
                        machine_running = False


        # sprites_to_board has to be updated before the screen.fill, also update buttons 
        sprites_to_board.update()
        colors_to_board.update()
        buttons.update()

        # setting up the display 
        screen.fill(SCREEN_COLOR)
        screen.blit(text, textRect) 
        sprites_to_board.draw(screen)
        colors_to_board.draw(screen)
        buttons.draw(screen)

        # updates the whole display 
        pg.display.flip()

    # game_array is produced once the main game loop has ended
    game_array = get_board_array(sprites_to_board, board_length)

    for item in game_array:
        print(item)

    pg.quit()

    if get_fractal_clicked:
        return [game_array, click_counter]
    else: 
        return "Not Activated" 

# ---------------------------------------------------------------------
#invoke main & pygame 
game_output = main()

#---------------------------------------------------------------------
#invoke Image_editor 
if isinstance(game_output, list):
    Image.write_image(game_output[0], game_output[1])


