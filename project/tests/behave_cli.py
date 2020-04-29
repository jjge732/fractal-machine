import os

from behave.__main__ import main as behave_main

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")


def run_behave() -> None:
    """Basic wrapper function for running behave"""
    behave_main(os.path.dirname(os.path.realpath(__file__)))


if __name__ == "__main__":
    run_behave()
