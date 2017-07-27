Feature: Admin users can delete other users, standard users cannot

Scenario: An admin user wants to delete a standard user
Given some users exist
Given the admin user is logged in
When the user deletes the standard user
Then I should get a '200' response

Scenario: An admin user wants to delete an admin user
Given some users exist
And the admin user is logged in
When the user deletes the admin user
Then I should get a '200' response

Scenario: A standard user tries to delete a user and fails
Given some users exist
And the standard user is logged in
When the user deletes the standard user
Then I should get a '403' response