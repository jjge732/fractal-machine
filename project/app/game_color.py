import pygame as pg
from boardpiece import BoardPiece
from gamebutton import GameButton
from image_editor import Image
from colortile import ColorTile
# from textfield import TextField
import pandas as pd 

# colors of board pieces 
WHITE          = pg.Color(255, 255, 255)
BLACK          = pg.Color(0, 0, 0)
GREY           = pg.Color(89, 89, 89)
SCREEN_COLOR   = BLACK
COLOR_INACTIVE = GREY
COLOR_ACTIVE   = WHITE

# other colors 
RANDOM       = pg.Color(255, 175, 50)
OTHER        = pg.Color(89, 89, 150)
BUTTON_COLOR = OTHER


# ---------------------------------------------------------------------
# SETTING UP THE COLORS 
# importing the color dataframe 
# RGB_Hex.xlsx was created by webscrap_forcolors.py

color_df = pd.read_excel('RGB_Hex.xlsx')

colors_list = []

for i in range((color_df.shape[0])):
    temp_color = str(color_df.iloc[i, 0])
    temp_color = temp_color.replace("(", "").replace(")", "")
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
    x_start_coord    = 300
    y_start_coord    = 175
    # to make it more centered when clicking between 3x3 and 4x4 
    if length == 3:
        x_start_coord = 350
        y_start_coord = 225
    for y in range(length):
        for x in range(length):
            # if you want a border to the rectangles, make x and y = 101, if not, 100
            sprites_to_board.add( BoardPiece( (x_start_coord + (x*101), y_start_coord + (y*101)) ) ) 
    return sprites_to_board

#create a color board 
def makeColorBoard(color_list):
    colors_to_board = pg.sprite.Group()
    x_start_coord   = 50
    y_start_coord   = 150
    count = 0 
    for y in range(15):
        for x in range(5):
            colors_to_board.add( ColorTile( (x_start_coord + (x*35), y_start_coord + (y*35)), color_list[count]) ) 
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

    # setting up the names needed for the display 
    SCREEN_WIDTH  = 1400
    SCREEN_HEIGHT = 900
    screen   = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font     = pg.font.Font("Jelly Crazies.ttf", 25) 
    game_title             = font.render('FRACTAL MACHINE', True, WHITE)
    game_title_rect        = game_title.get_rect() 
    game_title_rect.center = ((SCREEN_WIDTH / 2), 50) 

    # creating the board 
    board_length     = 4
    sprites_to_board = makeBoard(board_length)
    colors_to_board  = makeColorBoard(colors_list)

    # making the buttons 
    button_x = 275
    button_y = 625

    # buttons that specify game functionality
    buttons           = pg.sprite.Group()
    three_by_three    = GameButton(         "3x3", BUTTON_COLOR,         button_x,             button_y) 
    four_by_four      = GameButton(         "4x4", BUTTON_COLOR, (button_x + 228),             button_y)
    invert_button     = GameButton(      "Invert", BUTTON_COLOR,         button_x,      (button_y + 52))
    clear_button      = GameButton(       "Clear", BUTTON_COLOR, (button_x + 228),      (button_y + 52))
    generate_button   = GameButton(  "Fractalify", BUTTON_COLOR,         button_x,     (button_y + 104))
    fractal_buttton   = GameButton("Get Fractal!", BUTTON_COLOR, (button_x + 228),     (button_y + 104))
    exit_button       = GameButton(        "EXIT", SCREEN_COLOR,                0, (SCREEN_HEIGHT - 50))  
    
    # not really a button, but a box on the Screen 
    save_fract_button = GameButton("Save Fractal As: ", SCREEN_COLOR, 750, 175)    


    # change the font of the exit button to match the title 
    exit_button.change_font("Jelly Crazies.ttf")

    # add buttons to sprite group
    buttons.add( three_by_three  )
    buttons.add( four_by_four    )
    buttons.add( clear_button    )
    buttons.add( invert_button   )
    buttons.add( generate_button )
    buttons.add( exit_button     ) 
    buttons.add(save_fract_button)

    # making the text box 
    # file_name_text_box = TextField(900, 200, 140, 32)

    # setting up extra variables 
    click_counter       = 0
    get_fractal_clicked = False
    color_picked        = "None"
    text_box_active     = False
    user_input_text     = ""

    # MAIN GAME LOOP 
    machine_running = True
    while machine_running:
        for event in pg.event.get():

            if event.type == pg.QUIT:
                machine_running = False

            # If a mouse button was pressed.
            elif event.type == pg.MOUSEBUTTONDOWN:

                # trying to let the user pick their color
                for color_square in colors_to_board:
                    if color_square.rect.collidepoint(event.pos):
                        # save the user color choice 
                        color_picked = color_square.get_piece_color()
                        # making a seperate color button for the chosen color, to help user keep track of drawing color
                        chosen_color = GameButton("Current Color", color_picked, 50, (button_y + 52))
                        chosen_color.update_size(170,50)
                        # give user the option to go back to the original setting 
                        original_setting = GameButton("Original B/W", BLACK, 50, (button_y + 104))
                        original_setting.update_size(170,50)
                        # that way there aren't a bilion "Color" buttons in the sprite group at once
                        for button in buttons:
                            if button.get_button_function() == "Color":
                                buttons.remove(button)
                        buttons.add(chosen_color)
                        buttons.add(original_setting)
            			
                # Iterate over the sprites in the group.
                for sprite in sprites_to_board:
                    # Check if the sprite's rect collides with the mouse pos.
                    if sprite.rect.collidepoint(event.pos):
                        # Finally change the color.
                        if color_picked == "None" or color_picked == BLACK or color_picked == WHITE:
                            if str(sprite.get_piece_color()) == "(255, 255, 255, 255)" or color_picked == BLACK:
                                sprite.change_color(BLACK)
                            elif str(sprite.get_piece_color()) == "(0, 0, 0, 255)" or color_picked == WHITE:
                                sprite.change_color(WHITE)
                        else: 
                            # set the tile to the color of the user's choosing 
                            sprite.change_color(color_picked)

                # Iterate over the buttons in the group.
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
                        board_length = 3 # reset the number to get correct dimensions for the 2-D array (game_array)
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
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function()[:len("Fractalify")] == "Fractalify"):
                        click_counter += 1
                        if click_counter == 1:
                            generate_button.update_function(F"Fractalify: {click_counter}")
                            buttons.add(fractal_buttton)
                        # where the limit is set 
                        if click_counter <= 5: 
                            generate_button.update_function(F"Fractalify: {click_counter}")
                        else:
                            click_counter = 0
                            generate_button.update_function(F"Fractalify")
                            buttons.remove(fractal_buttton)
                    # get fract button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "Get Fractal!"):
                        get_fractal_clicked = True 
                        machine_running = False
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "Original B/W"):
                        color_picked = WHITE
                        buttons.remove(chosen_color)
                        buttons.remove(original_setting)

                # if file_name_text_box.rect.collidepoint(event.pos):
                #     file_name_text_box.set_active()
                # else: 
                #     file_name_text_box.set_inactive()
            elif event.type == pg.KEYDOWN:
                if text_box_active: 
                    temp_string += str(event.unicode)
                    print(temp_string)
            # elif event.type == pg.KEYDOWN:
            #     print("hey")
            #     # if file_name_text_box.get_active_status(): 
            #     #     print("hey - 2")
            #     file_name_text_box.user_typing(event)

        # sprites_to_board has to be updated before the screen.fill, also update buttons 
        sprites_to_board.update()
        colors_to_board.update()
        buttons.update()

        # setting up the display 
        screen.fill(SCREEN_COLOR)
        screen.blit(game_title, game_title_rect)
        pg.draw.rect(screen, GREY, (275,150,454,454)) 
        sprites_to_board.draw(screen)
        colors_to_board.draw(screen)
        buttons.draw(screen)


        # updates the whole display 
        pg.display.flip()

    # game_array is produced once the main game loop has ended
    game_array = get_board_array(sprites_to_board, board_length)

    for item in game_array:
        print(item)

    if get_fractal_clicked:
        return [game_array, click_counter]
    else: 
        return "Not Activated" 

# ---------------------------------------------------------------------
#invoke main & pygame 
if __name__ == '__main__':
    pg.init()
    game_output = main()
    pg.quit()
#---------------------------------------------------------------------
#invoke Image_editor 
if isinstance(game_output, list):
    Image.write_image(game_output[0], game_output[1])


