Feature: Empty categories can be deleted, categories with courses cannot be

Scenario: A user wants to delete an empty category
And the standard user is logged in
And the category "Pet Care" exists
And the user deletes the category "Pet Care"
Then I should get a '200' response
And the category "Pet Care" should not exist

Scenario: A user wants to delete a category with courses
And the standard user is logged in
And the category "Pet Care" exists
And the course "Advanced Hamster Training" exists in category "Pet Care"
And the user deletes the category "Pet Care"
Then I should get a '409' response
And the category "Pet Care" should exist in language "en"
