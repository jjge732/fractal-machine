import os
from typing import List

from fpdf import FPDF

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")


class Image:
    """Class for writing images to files, encoding and decoding image_codes, and converting image types."""

    # TODO: decide way that data should be given to this function from the GUI
    @staticmethod
    def write_image(color_list: List, degrees_of_fractility: int = 1, file_name: str = "fractal") -> None:
        """Writes an image in the svg format using data from user input in the GUI

            Args:
                color_list: List of lists in the form a 3 x 3 or 4 x 4 square
                file_name: The name to give the svg file

            Returns:
                An svg file of the fractal with the given name

        """
        if "." in file_name:
            file_name = file_name.split('.')[0]
        count = 0
        print(f"Attempting to create the fractal.")
        while True:
            try:
                name = f"{ROOT}/project/images/{f'{file_name}-{count}' if count != 0 else file_name}.svg"
                image = open(name, "x")
                break
            except Exception:
                count += 1
        image_str = Image.fractalate(color_list, degrees_of_fractility)
        image.write(image_str)
        if image is not None:
            image.close()
            print(f"Image successfully written as {name}")

    @staticmethod
    def fractalate(color_list: List, degrees_of_fractility: int) -> str:
        """

            Args:
                color_list: List of lists in the form a 3 x 3 or 4 x 4 square
                degrees_of_fractility: Number of times to fractalate

            Returns:
                A string of the svg file

        """
        square_side_length = len(color_list)
        new_square_side_length = square_side_length ** degrees_of_fractility
        new_color_list = [
            color_list[index % square_side_length] * new_square_side_length
            for index in range(new_square_side_length)
        ]

        square_side_length = len(color_list)
        if degrees_of_fractility > 1:
            Image.fract(color_list, new_color_list, square_side_length)

        for sub_list in new_color_list:
            print(sub_list)

        new_square_side_length = 100 * square_side_length
        image_str = f'<svg width="{new_square_side_length}" height="{new_square_side_length}" xmlns="http://www.w3.org/2000/svg">'
        for x, color_sub_list in enumerate(new_color_list):
            for y, color in enumerate(color_sub_list):
                x_index = int(100 * x / (square_side_length ** (degrees_of_fractility - 1)))
                y_index = int(100 * y / (square_side_length ** (degrees_of_fractility - 1)))
                image_str += f'<rect width="{100 / (square_side_length ** (degrees_of_fractility - 1))}" height="{100 / (square_side_length ** (degrees_of_fractility - 1))}" x="{x_index}" y="{y_index}" style="fill:#{color};stroke-width:3;stroke:rgb(0,0,0)"/>'
        return f"{image_str}</svg>"

    @staticmethod
    def fract(color_list: List, new_color_list: List, square_side_length: int) -> None:
        """

        Args:
            color_list: The original fractal as a list
            new_color_list: The newly created fractal size as a list
            square_side_length: The size of the square

        """
        for x_index, sub_list in enumerate(color_list):
            for y_index, color in enumerate(sub_list):
                if color == "FFF":
                    print(f"x index {x_index} y index {y_index}")
                    for index_1 in range(square_side_length):
                        for index_2 in range(square_side_length):
                            new_color_list[x_index * square_side_length + index_1][
                                y_index * square_side_length + index_2] = "FFF"
                            new_color_list[x_index * square_side_length + index_2][
                                y_index * square_side_length + index_1] = "FFF"

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

    @staticmethod
    def convert_to_jpg() -> None:
        """

            Returns:
               .jpg file is saved to images with the same name as the original file

        """
        pass
