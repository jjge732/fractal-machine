import os

from behave import given, then, use_step_matcher, when
from behave.runner import Context

from project.app.image_editor import Image
from project.app.routes.aws import API
from project.tests.models.expected_output import Output

use_step_matcher("re")

ROOT = os.environ.get("FRACTAL_MACHINE_ROOT")


@given("the image named (?P<name>[-_\w\s]+) is deleted")
def step_delete_image(ctx: Context, name: str) -> None:
    """Deletes an image from the images folder

    Args:
        ctx: The behave context
        name: The name of the image to delete

    """
    file_name = f"{sanitize(name)}-3x3.svg"
    try:
        print(f"Attempting to remove the image named {name}")
        os.remove(f"{ROOT}/project/images/{file_name}")
        print(f"Successfully removed the image named {name}")

    except FileNotFoundError:
        print(f"No image named {file_name} was found to remove.")


@when("an image is fractalated")
def step_generate_fractal(ctx: Context) -> None:
    """Generates a fractalated image

    Args:
        ctx: The behave context

    """
    print("Attempting to create a fractal matrix and store it on the behave context")
    ctx.fractalated_image = Image.fractalate(
        [
            [
                [
                    "F00", "FFF", "0F0"
                ],
                [
                    "00F", "3D5", "E21"
                ],
                [
                    "F00", "FFF", "0F0"
                ]
            ]
        ],
        [4],
        3
    )[1]
    print("Successfully created a fractal matrix and stored it on the behave context")


@then("the image matrix should match the stored image")
def step_assert_image_matches(ctx: Context) -> None:
    """Checks that the output image matches the expected output

    Args:
        ctx: The behave context

    """
    print(f"Attempting to assert that the output matrix is the expected matrix")
    assert ctx.fractalated_image == Output().matrix
    print(f"Successfully asserted that the output matrix is the expected matrix")


@when("an image named (?P<name>[-_\w\s]+) is created")
def step_create_image(ctx: Context, name: str) -> None:
    """Generates a fractalated image

    Args:
        ctx: The behave context
        name: The name to give to the image

    """
    file_name = sanitize(name)
    Image.write_image(
        [
            [
                "F00", "FFF", "0F0"
            ],
            [
                "00F", "3D5", "E21"
            ],
            [
                "F00", "FFF", "0F0"
            ]
        ],
        4,
        file_name
    )


@when("the image named (?P<name>[-_\w\s]+) is uploaded to S3")
def step_upload_image(ctx: Context, name: str) -> None:
    """Upload an image to the S3 bucket

    Args:
        ctx: The behave context
        name: The name of the file to upload to S3

    """
    print(f"Attempting to upload the image named {name} to S3")
    file_name = f"{sanitize(name)}-3x3.svg"
    API.storeImage(file_name)
    print(f"Successfully uploaded the image named {name} to S3")


@when("the image named (?P<name>[-_\w\s]+) is downloaded from S3")
def download_image(ctx: Context, name: str) -> None:
    """Download an image from the S3 bucket

    Args:
        ctx: The behave context
        name: The name of the file to upload to S3

    """
    print(f"Attempting to download the image named {name}")
    file_name = f"{sanitize(name)}-3x3.svg"
    API.retrieveImage(file_name)
    print(f"Successfully downloaded the image named {name}")


@then("the image named (?P<name>[-_\w\s]+) should be in the (?P<quantity>\d+) most recent image names in S3")
def step_get_stored_image_names(ctx: Context, name: str, quantity: str) -> None:
    """

    Args:
        ctx: The behave context
        name: The image name that should be present in the most recent images list
        quantity: The number of image names to retrieve

    """
    print(f"Attempting to get the most recent {quantity} image names stored in S3")
    quantity = int(quantity)
    file_name = f"{sanitize(name)}-3x3.svg"
    image_name_list = API.retrieveMostRecentImages(quantity)
    print(f"Successfully retrieved most recent {quantity} image names stored in S3.")
    assert file_name in image_name_list, \
        f"The file {file_name} was not present in {image_name_list}"


@then("the image named (?P<name>[-_\w\s]+) should (?P<negate>|not )be present")
def step_verify_image_status(ctx: Context, name: str, negate: str) -> None:
    """Verify that a given image is present or absent

    Args:
        ctx: The behave context
        name: The name of the file to assert is present or absent
        negate: Has a value of 'not' if it is supposed to be absent. Otherwise has a value of ''

    """
    file_name = f"{sanitize(name)}-3x3.svg"
    print(f"Attempting to assert that the image named {name} is {negate}present.")

    try:
        open(f"{ROOT}/project/images/{file_name}", "r")
        assert not negate, f"The file {name} was present when it was not expected to be"
    except FileNotFoundError:
        assert negate, f"The file {name} was not present when it was expected to be"
    print(f"Successfully asserted that the image named {name} is {negate}present.")


def sanitize(string: str) -> str:
    """Converts string to a format that can be more easily used by the application

    Args:
        string: The string to sanitize

    Returns:
        A sanitized string

    """
    return string.lower().strip().replace(" ", "-")
