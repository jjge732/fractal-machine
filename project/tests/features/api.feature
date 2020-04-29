Feature: API properly makes requests

    Scenario: Users are able to upload images
        When an image named test image is created
        Then the image named test image should be present
        When the image named test image is uploaded to S3
        Then the image named test image should be in the 5 most recent image names in S3

    Scenario: Users are able to download images
        Given the image named test image is deleted
        Then the image named test image should not be present
        When the image named test image is downloaded from S3
        Then the image named test image should be present

    @teardown
    Scenario: Delete image for next test run
        Given the image named test image is deleted
        Then the image named test image should not be present