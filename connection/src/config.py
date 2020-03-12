from configparser import ConfigParser
import os


ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")


def config(filename: str = f'{ROOT}/connection/database.ini', section: str ='postgresql') -> dict:
    """Creates the configuration for the postres database.

    Args:
        filename: The name of the file to use for the setup
        section: The database to use?

    Returns:
        The database instance
    """
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section: {section} not found in the file: {filename}.')

    return db
