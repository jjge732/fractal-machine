import os
from typing import List

from fpdf import FPDF

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")


class Image:
    """Class for writing images to files, encoding and decoding image_codes, and converting image types."""

    # TODO: decide way that data should be given to this function from the GUI
    @staticmethod
    def write_image(color_list: List, file_name: str = "fractal") -> None:
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
        square_side_length = len(color_list)
        print(f"Creating a square of side length: {square_side_length}")
        while True:
            try:
                file_name = f"{ROOT}/images/{f'{file_name}-{count}' if count != 0 else ''}.svg"
                image = open(file_name, "x")
                break
            except Exception:
                count += 1
        image_str = f'<svg width="{square_side_length}00" height="{square_side_length}00" xmlns="http://www.w3.org/2000/svg">'
        for x_index, color_sub_list in enumerate(color_list):
            for y_index, color in enumerate(color_sub_list):
                image_str += f'<rect width="100" height="100" x="{x_index}00" y="{y_index}00" style="fill:#{color};stroke-width:3;stroke:rgb(0,0,0)"/>'
        image.write(f"{image_str}</svg>")
        if image is not None:
            image.close()
            print(f"Image successfully written as {file_name}")

    @staticmethod
    def color_code_to_pdf(colored_square_code: str, output_file_name: str = "fractal") -> None:
        """Method for converting a color_code to a pdf file

            Args:
                colored_square_code: The encoded colored square.
                    Encoded using hex color codes in 9 chunks each of length 3 or 6
                    Obtained from the database.
                output_file_name:

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
