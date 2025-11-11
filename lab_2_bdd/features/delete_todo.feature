Feature: Delete a single To-Do item
    As a user of the API,
    I want to delete a specific to-do item by its ID,
    so that I can keep my to-do list clean.

    Scenario: A to-do item exists and can be deleted
        Given the API has a list of to-dos
        When the user deletes the to-do with id 2
        Then the response status code should be 200
        And the response should indicate successful deletion

    Scenario: A to-do item does not exist
        Given the API has a list of to-dos
        When the user deletes the to-do with id 99
        Then the response status code should be 404
        And the response should contain a "not found" error message
