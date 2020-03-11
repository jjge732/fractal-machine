import psycopg2
from connection.config import config


class Image:
    """Class for defining methods to alter the images table."""
    @staticmethod
    def add_image(file_name: str) -> int:
        """Insert a new image into the images table

            Args:
                file_name: The name of the file to add to the table

            Returns:
                The id of the image in the table

        """
        sql_command = """
            INSERT INTO images(data)
                 VALUES(%s) RETURNING id;
            """
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(sql_command, file_name)
            image_id = cursor.fetchone()[0]

            connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

        return image_id if not None else -1