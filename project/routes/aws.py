import os
import requests

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")

class API:
    
    @staticmethod
    def retrieveImage(file_name: str) -> None:
        """Method for retrieving an image from the S3 bucket by it's name.
        
        Args:
            file_name: The name of the file to retrieve

        """
        print(f"Attempting to retrieving {file_name} from S3...")
        response = requests.get(f"https://lwvefma751.execute-api.us-east-2.amazonaws.com/v1/{file_name}")
        if response.status_code != 200:
            raise Exception(f"File unable to be located: {response}")
        try:
            file = open(file_name, "x")
        except Exception:
            print(f"Overwritting file named {file_name} in the images folder.")
            file = open(file_name, "w")
        file.write(response.text)
        print(f"Successfully retrieved file from S3 and stored it in the images folder!")

    @staticmethod
    def storeImage(file_name: str) -> None:
        """Method for storing an image in an S3 bucket

            Args:
                file_name: The name of the file to store in S3
     
        """
        contentTypeDict = {
            "pdf": "application/pdf",
            "svg": "image/svg+xml"
        }
        file_extension = file_name.split('.')[-1]

        if file_extension in contentTypeDict.keys():
            contentType = contentTypeDict[file_extension]
        else:
            raise TypeError(
                f"The format of {file_name} was not recognized. Please only send a file of one of the following formats:\n{', '.join(contentTypeDict.keys())}"
            )
        print(f"Attempting to store {file_name} in S3...")
        file = open(f"{ROOT}/project/images/{file_name}")
        response = requests.put(
            url=f"https://lwvefma751.execute-api.us-east-2.amazonaws.com/v1/{file_name}",
            data=file,
            headers={
                "Content-Type": "image/svg+xml"
            }
        )
        if response.status_code == 200:
            print(f"Successfully stored f{file_name} in S3!")
        else:
            print(f"An error occurred with status code {requests.status_code} and data:\n{response.data}")