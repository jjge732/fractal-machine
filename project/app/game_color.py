import pygame as pg
from boardpiece import BoardPiece
from gamebutton import GameButton
from image_editor import Image
from colortile import ColorTile
from routes.aws import API 
import pandas as pd 
import subprocess

# main colors of the game 
WHITE        = pg.Color(255, 255, 255)
BLACK        = pg.Color(0, 0, 0)
GREY         = pg.Color(89, 89, 89)
LIGHT_GREY   = pg.Color(175, 175, 175)
BUTTON_COLOR = pg.Color(89, 89, 150)
SCREEN_COLOR = BLACK

# other colors 
RANDOM       = pg.Color(255, 175, 50)

# ---------------------------------------------------------------------
# SETTING UP THE COLOR BOARD
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

# see if the user name the fractal, else fractal will be named something like " -4x4.svg"
def user_named_fractal(temp_string):
    unique_chars = list(set(list(temp_string)))
    return len(unique_chars) > 1 or (len(unique_chars) == 1 and " " not in unique_chars)

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

    # making the buttons: 
    button_x = 275
    button_y = 625

    # buttons that specify game functionality
    buttons           = pg.sprite.Group()
    three_by_three    = GameButton(         "3x3", BUTTON_COLOR,         button_x,             button_y) 
    four_by_four      = GameButton(         "4x4", BUTTON_COLOR, (button_x + 228),             button_y)
    invert_button     = GameButton(      "Invert", BUTTON_COLOR,         button_x,      (button_y + 55))
    clear_button      = GameButton(       "Clear", BUTTON_COLOR, (button_x + 228),      (button_y + 55))
    generate_button   = GameButton(  "Fractalify", BUTTON_COLOR, (button_x + 115),     (button_y + 110))
    exit_button       = GameButton(        "EXIT", SCREEN_COLOR,                0, (SCREEN_HEIGHT - 50))  

    # buttons that pop up once the user chooses a degree of fractilality 
    # name_fract_box is not really used as a button, just a box on the Screen 
    name_fract_box     = GameButton("Enter Name of Fractal:", GREY, 825, button_y)
    name_fract_button  = GameButton(" ", GREY, 1075, button_y)
    op_dwnload_buttton = GameButton("Open & Download", BUTTON_COLOR, 825, (button_y + 55))
    download_button   = GameButton("Download", BUTTON_COLOR, 1075, (button_y + 55))

    # special button that allows users to view most recent button
    view_recent_button = GameButton("View Recent Fractalization", BUTTON_COLOR, 825, 325)

    # change the font of the exit button to match the title 
    exit_button.change_font("Jelly Crazies.ttf")

    # add buttons to sprite group
    buttons.add( three_by_three  )
    buttons.add( four_by_four    )
    buttons.add( clear_button    )
    buttons.add( invert_button   )
    buttons.add( generate_button )
    buttons.add( exit_button     ) 

    # setting up extra variables 
    click_counter       = 0
    get_fractal_clicked = False
    color_picked        = "None"
    text_box_active     = False
    temp_string         = ""
    open_fractal = False
    
    # Giving the game a title
    pg.display.set_caption('Fractal Machine')

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
                            if button.get_button_function() == "Current Color": 
                                buttons.remove(button)
                            if button.get_button_function() == "Original B/W": 
                                buttons.remove(button)
                        buttons.add(chosen_color)
                        buttons.add(original_setting)
            			
                # Iterate over the sprites in the group.
                for sprite in sprites_to_board:
                    # Check if the sprite's rect collides with the mouse pos.
                    if sprite.rect.collidepoint(event.pos):
                        # Change the color.
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
                    # exit button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "EXIT"):
                        machine_running = False
                    # fractalify button
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function()[:len("Fractalify")] == "Fractalify"):
                        click_counter += 1
                        if click_counter == 1:
                            generate_button.update_function(F"Fractalify: {click_counter}")
                            buttons.add(download_button)
                            buttons.add(op_dwnload_buttton)
                            buttons.add(name_fract_box)
                            buttons.add(name_fract_button)
                        # where the limit is set 
                        if click_counter <= 5: 
                            generate_button.update_function(F"Fractalify: {click_counter}")
                        else:
                            click_counter = 0
                            generate_button.update_function(F"Fractalify")
                            buttons.remove(download_button)
                            buttons.remove(op_dwnload_buttton)
                            buttons.remove(name_fract_box)
                            buttons.remove(name_fract_button)
                    # get fract button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "Download" or button.get_button_function() == "Open & Download"):
                        get_fractal_clicked = True 
                        if button.get_button_function() == "Open & Download":
                            print("hello")
                            open_fractal = True
                        machine_running = False
                    # reset the colors to black and white 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "Original B/W"):
                        color_picked = WHITE
                        buttons.remove(original_setting)
                        buttons.remove(chosen_color)
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == " "):
                        text_box_active = True 
                        buttons.remove(button)
                        name_fract_button = GameButton(" ", LIGHT_GREY, 1075, button_y)
                        buttons.add(name_fract_button)
                    # the clear button 
                    elif button.rect.collidepoint(event.pos) and (button.get_button_function() == "Clear"):
                        for sprite in sprites_to_board:
                            sprite.change_color(WHITE)
                        click_counter = 0
                        generate_button.update_function(F"Fractalify")
                        temp_string = ""
                        for button in buttons:
                            if button in [download_button, name_fract_box, name_fract_button, op_dwnload_buttton]:
                                buttons.remove(button)

            elif event.type == pg.KEYDOWN:
                if text_box_active: 
                    if event.key == pg.K_BACKSPACE:
                        temp_string = temp_string[:-1]
                        name_fract_button.update_function(temp_string)
                    else:
                        temp_string += event.unicode
                        name_fract_button.update_function(temp_string)

        # sprites_to_board has to be updated before the screen.fill, also update buttons 
        sprites_to_board.update()
        colors_to_board.update()
        buttons.update()

        # setting up the display 
        screen.fill(SCREEN_COLOR)
        screen.blit(game_title, game_title_rect)
        pg.draw.rect(screen, GREY, (275,150,454,454)) # grid behind fract tiles 
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
        if user_named_fractal(temp_string):
            return [game_array, click_counter, temp_string, open_fractal]
        else:
            return [game_array, click_counter]
    else: 
        return "Not Activated" 

# ---------------------------------------------------------------------
# invoke main & pygame 
if __name__ == '__main__':
    pg.init()
    game_output = main()
    pg.quit()
#---------------------------------------------------------------------
# invoke Image_editor 
if isinstance(game_output, list):
    if len(game_output) == 4:
        image = Image.write_image(game_output[0], game_output[1], game_output[2])
        API.storeImage(image)
        if game_output[3]:
            subprocess.run(F'open -a "Google Chrome" ../images/{image}', shell=True)
    else: 
        image = Image.write_image(game_output[0], game_output[1])
        API.storeImage(image)

    
        # subprocess.run(F'open -a "Google Chrome" ../images/{image}', shell=True)


# WORKS 
# subprocess.run('open -a "Google Chrome" ../images/test-1-4x4.svg', shell=True)

