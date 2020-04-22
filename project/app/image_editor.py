import os
from typing import List

from fpdf import FPDF
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")


class Image:
    """Class for writing images to files, encoding and decoding image_codes, and converting image types."""

    @staticmethod
    def write_image(color_list: List[List[str]], degrees_of_fractility: int = 1, file_name: str = "fractal") -> None:
        """Writes an image in the svg format using data from user input in the GUI

            Args:
                color_list: List of lists in the form a 3 x 3 or 4 x 4 square
                degrees_of_fractility: The number of times to fractalate the square
                file_name: The name to give the svg file

            Returns:
                An svg file of the fractal with the given name

        """
        if "." in file_name:
            file_name = file_name.split('.')[0]
        count = 0
        print(f"Attempting to create the fractal.")
        square_side_length = len(color_list)
        file_name = f"{file_name}-{square_side_length}x{square_side_length}"
        while True:
            try:
                name = f"{ROOT}/project/images/{f'{file_name}-{count}' if count != 0 else file_name}.svg"
                image = open(name, "x")
                break
            except Exception:
                count += 1
        image_str = Image.fractalate([color_list], [degrees_of_fractility], square_side_length)
        image.write(image_str)
        if image is not None:
            image.close()
            print(f"Image successfully written as {name.split('/')[-1]}")
        
        return name.split('/')[-1]

    @staticmethod
    def fractalate(color_list_list: List[List[List[str]]], degrees_of_fractility_list: List[int], square_side_length: int = None) -> str:
        """Method for creating the new fractal

            Args:
                color_list_list: List of lists of square fractal, the last list will always be the original square fractal
                degrees_of_fractility_list: List of the number of times to fractalate, the first int is the remaining
                    times to fractalate and the last is the total number of fractalations
                square_side_length: The side length of the square

            Returns:
                A string representation of the svg file (from create_svg_image_str)

        """
        new_square_side_length = square_side_length ** degrees_of_fractility_list[-1]
        new_color_list = [[[] for _ in range(new_square_side_length)] for _ in range(new_square_side_length)]

        for x, color_sub_list in enumerate(new_color_list):
            for y in range(len(color_sub_list)):
                for i in range(len(color_list_list)):
                    denominator = square_side_length ** (degrees_of_fractility_list[i] - 1)
                    if color_list_list[i][int(x / denominator)][int(y / denominator)] in ["FFF", "FFFFFF"]:
                        color = "FFF"
                        break
                    else:
                        color = color_list_list[-1][x % square_side_length][y % square_side_length]
                new_color_list[x][y] = color

        if degrees_of_fractility_list[0] > 2:
            return Image.fractalate([new_color_list, *color_list_list], [degrees_of_fractility_list[0] - 1, *degrees_of_fractility_list], square_side_length)
        return Image.create_svg_image_str(square_side_length, new_color_list, degrees_of_fractility_list[-1])

    @staticmethod
    def create_svg_image_str(square_side_length: int, color_list: List[List[str]], degrees_of_fractility: int) -> str:
        """Writes an image representation of the string using the final color list from the fractalate method

            Args:
                square_side_length: The number of side in the original square fractal
                color_list: The final color list to be turned into an svg image
                degrees_of_fractility: The total number of times fractalation has occurred

            Returns:
                A string representation of the svg file

        """
        new_square_side_length = 500 * square_side_length
        image_str = f'<svg width="{new_square_side_length}" height="{new_square_side_length}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" style="fill:#FFF"/>'

        for x, color_sub_list in enumerate(color_list):
            for y, color in enumerate(color_sub_list):
                if color in ["FFF", "FFFFFF"]:
                    continue
                for z in range(degrees_of_fractility):
                    dimensions = 500 / (square_side_length ** z)
                    x_index = x * dimensions
                    y_index = y * dimensions
                    image_str += f'<rect width="{dimensions}" height="{dimensions}" x="{x_index}" y="{y_index}" opacity="{.5}" style="fill:#{color};stroke-width:3;stroke:#FFF"/>'

        return f"{image_str}</svg>"

    @staticmethod
    def convert_svg(file_name: str = "complex-3x3.svg", file_format: str = "pdf") -> None:
        """Method for converting the given svg file to a different file format

        Args:
            file_name: The name of the file to convert to pdf
            file_format: The type of file to output

        """
        new_file_name = f"{file_name.split('.')[0]}.{file_format}"
        print(f"Attempting to convert {file_name} to {new_file_name}")
        file = open(f"{ROOT}/project/images/{file_name}", "r")
        drawing = svg2rlg(file)
        if file_format.lower() == "pdf":
            renderPDF.drawToFile(drawing, f"{ROOT}/project/images/{new_file_name}")
        else:
            renderPM.drawToFile(drawing, f"{ROOT}/project/images/{new_file_name}", fmt=file_format.upper())
        file.close()
        print(f"Successfully converted {file_name} to {new_file_name}")

