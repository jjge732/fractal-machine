import psycopg2
from project.connection.config import config


class Image:
    """Class for defining methods to alter the images table."""

    @staticmethod
    def add_image(colored_square_code: str) -> int:
        """Insert a new image into the images table

            Args:
                colored_square_code: The encoded colored square.
                    Encoded using hex color codes in 9 chunks each of length 3 or 6

            Returns:
                The id of the image in the table

        """
        sql_command = """
            INSERT INTO images(data)
                 VALUES ('%s') RETURNING id;
            """
        connection = None
        image_id = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(sql_command % colored_square_code)
            image_id = cursor.fetchone()[0]

            connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

        return image_id if not None else -1

    @staticmethod
    def retrieve_image(image_id: str) -> str:
        """Retrieve an image code from the database by it's id

        Args:
            image_id: The id of the image to retrieve

        Returns:
            The colored_square_code of the image

        """
        sql_command = """
            SELECT * FROM images
            WHERE (id = %d);
        """
        connection = None
        data = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(sql_command % image_id)
            data = cursor.fetchone()[0]

            connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

        return data or None