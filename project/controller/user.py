import psycopg2
from connection.src.config import config


# TODO: decide if we want this
# TODO: create method for adding images to user, finding images by user, and deleting images from user
class User:
    """Class for """
    @staticmethod
    def add_user(username: str, password: str) -> int:
        """Insert a new user into the users table

            Args:
                username: The name of the user to add to the users table
                password: The user's password

            Returns:
                The id of the user added to the users table

        """
        sql_command = """
            INSERT INTO users(username, password)
                 VALUES(%s) RETURNING id;
            """
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(sql_command, (username, password))
            user_id = cursor.fetchone()[0]
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

        return user_id if not None else -1

    @staticmethod
    def find_user(username: str) -> dict:
        """Find a user in the users table

            Args:
                username: The name of the user in the users table

            Returns:
                Data of the user stored in the users table

        """
        sql_command = """
                SELECT * FROM users WHERE username is (%s);
                """
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(sql_command, username)
            user = cursor.fetchone()[0]
            # commit the changes to the database
            connection.commit()
            # close communication with the database
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

        return user if not None else {"error_message": f"Unable to find user: {username}"}

    @staticmethod
    def delete_user(username: str) -> bool:
        """Delete a user from the users table

            Args:
                username: The name of the user to delete

            Returns:
                True if the user was deleted or False if they were not
        """
        sql_command = """
            DELETE FROM users WHERE id is (%s);
            """
        connection = None
        try:
            user_id = User.find_user(username)
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            cursor.execute(sql_command, user_id)
            connection.commit()
            cursor.close()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
            return False
