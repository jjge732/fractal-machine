from image_editor import Image
# from game import main as game_main
#import pygame as pg

Image.write_image([
  ["00F", "D60", "FFF"],
  ["0F0", "FFF", "D60"],
   ["FFF", "D60", "D60"]
], 5, "complex")

Image.write_image([
  ["00F", "D60", "FFF"],
  ["D60", "FFF", "D60"],
   ["FFF", "D60", "D60"]
], 5, "aesthetically_pleasing")


# Image.color_code_to_pdf("000" "000" "FFF" "000" "FFF" "000" "FFF" "000" "000")

# print(Image.encode_square([
#     ["000", "000", "FFF"],
#     ["000", "FFF", "000"],
#     ["FFF", "000", "000"]
# ]))

# game_output = game_main()
#
# Image.write_image(game_output[0], game_output[1])


