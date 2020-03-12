import psycopg2
from fractal_connections import config


def connect() -> None:
    """Connects to the postgres database."""
    connection = None
    try:
        params = config()

        print("Attempting to connect to the postgres database.")
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
        cursor.execute('Select version()')
        db_version = cursor.fetchone()
        print(f"Connected to the postgres database version number: {db_version}")

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
