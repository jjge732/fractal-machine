import os
from typing import List

from fpdf import FPDF

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")


class Image:
    """Class for writing images to files, encoding and decoding image_codes, and converting image types."""

    # TODO: decide way that data should be given to this function from the GUI
    @staticmethod
    def write_image() -> None:
        """Writes an image in the svg format using data from user input in the GUI

            Args:
                TBD: need to decide format to move image from the GUI to here
        """
        image = None
        count = 0
        while True:
            try:
                file_name = f"{ROOT}/images/demofile{f'-{count}' if count != 0 else ''}.svg"
                image = open(file_name, "x")
                break
            except Exception:
                count += 1

        image.write("""
            <svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">
                <rect width="100" height="100" x="000" y="000" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
                <rect width="100" height="100" x="000" y="100" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
                <rect width="100" height="100" x="000" y="200" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
                <rect width="100" height="100" x="100" y="000" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
                <rect width="100" height="100" x="100" y="100" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
                <rect width="100" height="100" x="100" y="200" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
                <rect width="100" height="100" x="200" y="000" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
                <rect width="100" height="100" x="200" y="100" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
                <rect width="100" height="100" x="200" y="200" style="fill:#00f;stroke-width:3;stroke:rgb(0,0,0)"/>
            </svg>
        """)

        if image is not None:
            image.close()
            print(f"Image successfully written as {file_name}")

    @staticmethod
    def convert_to_pdf(colored_square_code: str) -> None:
        """Method for converting an svg file to pdf

            Args:
                colored_square_code: The encoded colored square.
                    Encoded using hex color codes in 9 chunks each of length 3 or 6
                    Obtained from the database.

            Returns:
                File is output to images directory with the same name as the original file.

        """
        colored_square_list = Image.decode_square(colored_square_code)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_xy(0, 0)
        for i in colored_square_list:
            for j in range(9):
                pdf.set_fill_color(r=i["red"], g=i["green"], b=i["blue"])
                pdf.rect(x=i["index"][0] * 2, y=i["index"][1] * 2, w=2, h=2, style='F')

        pdf.output(f"{ROOT}/images/demo.pdf", 'F')

    @staticmethod
    def decode_square(colored_square_code: str) -> List:
        """Method for decoding the colored square

            Args:
                colored_square_code: The encoded colored square.
                    Encoded using hex color codes in 9 chunks each of length 3 or 6
                    Obtained from the database.

            Returns:
                List of each color code

        """
        if len(colored_square_code) == 27:
            return [{
                "index": (i % 3, i / 3),
                "red": int(colored_square_code[i * 3] * 2, 16),
                "green": int(colored_square_code[i * 3 + 1] * 2, 16),
                "blue": int(colored_square_code[i * 3 + 2] * 2, 16)
            } for i in range(9)]
        elif len(colored_square_code) == 54:
            return [{
                "index": i,
                "red": int(colored_square_code[i:1], 16),
                "green": int(colored_square_code[i + 2:i + 3], 16),
                "blue": int(colored_square_code[i + 4: i + 5], 16)
            } for i in range(9)]
        else:
            raise Exception("Invalid color encoding.")

    @staticmethod
    def encode_square() -> str:
        """Method for encoding given square list data to a string

            Args:
                TBD:

        """
        pass

    @staticmethod
    def convert_to_jpg() -> None:
        """

            Returns:
               .jpf file is saved to images with the same name as the original file

        """
