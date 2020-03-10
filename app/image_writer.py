import os

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")

image = open(f"{ROOT}/images/demofile.svg", "w")
image.write("""
    <svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="100" x="000" y="000" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)"/>
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
image.close()
