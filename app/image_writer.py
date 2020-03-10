import os

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")


class Image:
    """Class for altering images"""

    @staticmethod
    def write_image() -> None:
        """Writes an image in the svg format"""
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
