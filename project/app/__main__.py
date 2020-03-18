from image_editor import Image

# Image.write_image([
#     ["000", "000", "FFF"],
#     ["000", "FFF", "000"],
#     ["FFF", "000", "000"]
# ])

# Image.write_image([
#     ["000", "000", "000", "FFF"],
#     ["000", "000", "FFF", "000"],
#     ["000", "FFF", "000", "000"],
#     ["FFF", "000", "000", "000"],
# ])
# Image.color_code_to_pdf("000" "000" "FFF" "000" "FFF" "000" "FFF" "000" "000")


#get the GUI to generate this stuff

print(Image.encode_square([
    ["000", "000", "FFF"],
    ["000", "FFF", "000"],
    ["FFF", "000", "000"]
]))
