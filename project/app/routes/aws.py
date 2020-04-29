import os
import requests
from typing import List

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")
URL = "https://lwvefma751.execute-api.us-east-2.amazonaws.com/v1/"


class API:

    @classmethod
    def retrieveListOfImageNames(cls) -> List[str]:
        """Method for retrieving all the image names from the S3 bucket."""
        response = cls._retrievalHelper()
        return [name['file_name'] for name in response]

    @classmethod
    def retrieveMostRecentImages(cls, nbrImages: int = 5) -> List[str]:
        """Method for retrieveing the most recent images from the S3 bucket.

        Args:
            nbrImages: The number of images to retrieve from the database

        """
        response = cls._retrievalHelper()
        length = len(response)
        sorted_list = cls._quickSort(response, length - 1)
        return [name['file_name'] for name in sorted_list[length - nbrImages:]]

    @staticmethod
    def retrieveImage(file_name: str) -> None:
        """Method for retrieving an image from the S3 bucket by it's name.
        
        Args:
            file_name: The name of the file to retrieve

        """
        print(f"Attempting to retrieving {file_name} from S3...")
        response = requests.get(f"{URL}{file_name}")
        if response.status_code != 200:
            raise Exception(f"File unable to be located: {response}")
        try:
            file_location = f"{ROOT}/project/images/{file_name}"
            file = open(file_location, "x")
        except Exception:
            print(f"Overwritting file named {file_name} in the images folder.")
            file = open(file_location, "w")
        file.write(response.text)
        print(f"Successfully retrieved file from S3 and stored it in the images folder!")

    @staticmethod
    def storeImage(file_name: str) -> None:
        """Method for storing an image in an S3 bucket.

            Args:
                file_name: The name of the file to store in S3
     
        """
        file_extension = file_name.split('.')[-1].lower()

        if file_extension != "svg":
            raise TypeError(
                f"The format of {file_name} was not recognized. Please only send an svg file."
            )
        print(f"Attempting to store {file_name} in S3...")
        file = open(f"{ROOT}/project/images/{file_name}", "r")
        response = requests.put(
            url=f"{URL}{file_name}",
            data=file,
            headers={
                "Content-Type": "image/svg+xml"
            }
        )
        if response.status_code == 200:
            print(f"Successfully stored {file_name} in S3!")
        else:
            print(f"An error occurred with status code {response.status_code} and data:\n{response.content}")
            raise Exception

    @staticmethod
    def _retrievalHelper() -> List[dict]:
        """Private helper method for retrieving objects from the S3 bucket

        Returns:
            An alphabetical list of dictionaries containing file names and the dates they were last updated

        """
        print(f"Attempting to retrieving image names from S3...")
        response = requests.get(URL)
        if response.status_code != 200:
            raise Exception(f"Unable to be connect to S3.")
        print(f"Successfully retrieved file names from S3!")
        return response.json()['body']

    @classmethod
    def _quickSort(cls, files: List[dict], high_index: int, low_index: int = 0) -> List[dict]:
        """
        Private helper method that sorts the files retrieved from S3 by their last updated date
            and returns the sorted file names

        Args:
            files: A dictionary containing file names and updated dates
            high_index: The highest index this method call should sort
            low_index: The lowest index this method call should sort

        Returns:
            A sorted list of dictionaries containing file names and the dates they were last updated

        """
        if not high_index:
            high_index = len(files) - 1

        if low_index < high_index:
            partition_index = cls._partition(files, high_index, low_index)
            cls._quickSort(files, partition_index - 1, low_index)
            cls._quickSort(files, high_index, partition_index + 1)
        return files

    @classmethod
    def _partition(cls, files: List[dict], high_index: int, low_index: int) -> int:
        """Private helper method for finding the partition of the list

        Args:
            A dictionary containing file names and updated dates
            high_index: The highest index this method call should use for partitioning
            low_index: The lowest index this method call should use for partitioning

        Returns:
            A partition index for this subsection of the list

        """
        i = (low_index - 1)
        pivot = files[high_index]["updated_date"]

        for j in range(low_index, high_index):

            if files[j]["updated_date"] < pivot:
                i = i + 1
                files[i], files[j] = files[j], files[i]

        files[i + 1], files[high_index] = files[high_index], files[i + 1]
        return i + 1
