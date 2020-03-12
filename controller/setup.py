import setuptools

setuptools.setup(
    name='controllers',
    version='0.1dev',
    package_dir={'': 'src'},
    packages=setuptools.find_packages("src"),
    provides=setuptools.find_packages("src"),
)
