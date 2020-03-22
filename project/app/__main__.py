from image_editor import Image
from game import main as game_main
import pygame as pg



pg.init()
game_array = game_main()
pg.quit()

Image.write_image(game_array)

#print( Image.encode_square(game_array) )