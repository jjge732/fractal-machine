from setuptools import setup, find_packages

setup(
      name='fractal',
      version='0.1',
      description='Foo',
      url='https://github.com/jjge732/fractal-machine',
      author='Bar',
      packages=find_packages(),
      package_data={"": ["features/*.feature"]},
      include_package_data=True,
      zip_safe=False,
      entry_points={
            "console_scripts": [
                  "run = project.app.game_color:start",
                  "test = project.tests.behave_cli:run_behave"
            ]
      }
)
