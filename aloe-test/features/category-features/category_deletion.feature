Feature: Empty categories can be deleted, categories with courses cannot be

Scenario: A user wants to delete an empty category
Given the standard user is logged in
And the category "Pet Care" exists
And the user sets the category "Pet Care" as pending for deletion
Then I should get a '200' response
And the category "Pet Care" should be pending for deletion

Scenario: A user accepts deletion of an empty category
Given the standard user is logged in
And the category "Pet Care" exists
And the category "Pet Care" is pending for deletion
And the user deletes the category "Pet Care"
Then I should get a '200' response
And the category "Pet Care" should not exist

Scenario: A user cannot delete a category with courses
Given the standard user is logged in
And the category "Pet Care" exists
And the course "Advanced Hamster Training" exists
And the course "Advanced Hamster Training" is in category "Pet Care"
And the user sets the category "Pet Care" as pending for deletion
Then I should get a '409' response
