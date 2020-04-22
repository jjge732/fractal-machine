import os
from typing import List

from fpdf import FPDF

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
    def color_code_to_pdf(colored_square_code: str, output_file_name: str = "fractal") -> None:
        """Method for converting a color code to a pdf file

            Args:
                colored_square_code: The encoded colored square.
                    Encoded using hex color codes in 9 chunks each of length 3 or 6
                    Obtained from the database.
                output_file_name: The name of the file that as which the image is saved

            Returns:
                File is output to images directory with the given file name

        """
        if "." in output_file_name:
            output_file_name = output_file_name.split('.')[0]

        colored_square_list = Image.decode_square(colored_square_code)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_xy(0, 0)
        for i in colored_square_list:
            for j in range(9):
                pdf.set_fill_color(r=i["red"], g=i["green"], b=i["blue"])
                pdf.rect(x=i["index"][0] * 20, y=i["index"][1] * 20, w=20, h=20, style='F')

        pdf.output(name=f"{ROOT}/images/{output_file_name}.pdf")
        print(f"File output to {output_file_name}.pdf")

    # TODO: make working for all fractal sizes
    @staticmethod
    def decode_square(colored_square_code: str) -> List:
        """Method for decoding the colored square

            Args:
                colored_square_code: The encoded colored square.
                    Encoded using hex color codes in 9 chunks each of length 3 or 6

            Returns:
                List of each color code

        """
        if len(colored_square_code) == 27:
            return [{
                "index": (i % 3, int(i / 3)),
                "red": int(colored_square_code[i * 3] * 2, 16),
                "green": int(colored_square_code[i * 3 + 1] * 2, 16),
                "blue": int(colored_square_code[i * 3 + 2] * 2, 16)
            } for i in range(9)]
        elif len(colored_square_code) == 54:
            return [{
                "index": i,
                "red": int(colored_square_code[i * 3:i * 3 + 1], 16),
                "green": int(colored_square_code[i * 3 + 2:i * 3 + 3], 16),
                "blue": int(colored_square_code[i + 4: i * 3 + 5], 16)
            } for i in range(9)]
        else:
            raise Exception("Invalid color encoding.")

    @staticmethod
    def encode_square(color_list: List) -> str:
        """Method for encoding given square list data to a string

            Args:
                color_list: List of lists in the form a 3 x 3 or 4 x 4 square

            Returns:
                An encoded color square using hex color codes in 9 chunks each of length 3 or 6

        """
        return "".join("".join(item for item in sub_list) for sub_list in color_list)

    # TODO: make working .
    @staticmethod
    def convert_to_jpg() -> None:
        """

            Returns:
               .jpg file is saved to images with the same name as the original file

        """
        pass
