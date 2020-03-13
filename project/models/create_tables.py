import psycopg2

from project.connection.config import config


def create_tables() -> None:
    """Create tables in the postgres database

        Returns:
            (Re-)Creates the users and images table in the fractal-machine database.

    """
    commands = (
        """
        DROP TABLE IF EXISTS users;
        """,
        """
        DROP TABLE IF EXISTS images;
        """,
        """
        CREATE TABLE images(
            id SERIAL PRIMARY KEY,
            data VARCHAR (55) NOT NULL
        );
        """,
        """ 
        CREATE TABLE users(
            id INT PRIMARY KEY,
            username VARCHAR (50) UNIQUE NOT NULL,
            password VARCHAR (50) NOT NULL,
            FOREIGN KEY (id) REFERENCES images (id) ON UPDATE CASCADE ON DELETE SET NULL
        );
        """
    )
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    create_tables()
