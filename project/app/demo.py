from image_editor import Image

Image.write_image([
  ["000", "000", "FFF"],
  ["000", "FFF", "000"],
   ["FFF", "000", "000"]
], 1, "base")

Image.write_image([
    ["922247", "922247", "922247", "FFFFFF"],
    ["922247", "922247", "FFFFFF", "922247"],
    ["922247", "FFFFFF", "922247", "922247"],
    ["FFFFFF", "922247", "922247", "922247"],
], 1, "base")

Image.write_image([
  ["000", "000", "FFF"],
  ["000", "FFF", "000"],
   ["FFF", "000", "000"]
], 5)

Image.write_image([
    ["922247", "922247", "922247", "FFFFFF"],
    ["922247", "922247", "FFFFFF", "922247"],
    ["922247", "FFFFFF", "922247", "922247"],
    ["FFFFFF", "922247", "922247", "922247"],
], 4)