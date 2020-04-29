Feature: Fractalization

  Scenario: Image Fractalates Correctly
    When an image is fractalated
    Then the image matrix should match the stored image
