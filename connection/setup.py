import setuptools

setuptools.setup(
    name='fractal_connections',
    version='0.1dev',
    package_dir={'': 'src'},
    packages=setuptools.find_packages("src"),
    provides=setuptools.find_packages("src"),
)
