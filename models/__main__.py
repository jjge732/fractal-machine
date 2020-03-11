import psycopg2
from connection.config import config


def create_tables() -> None:
    """Create tables in the postgres database"""
    commands = (
        """
        CREATE TABLE images(
            id INT PRIMARY KEY,
            data VARCHAR (50) UNIQUE NOT NULL
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
