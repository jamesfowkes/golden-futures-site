Feature: Admin users can create other users, standard users cannot

Scenario: An admin user wants to create a standard user
Given the admin user is logged in
When the user creates standard user:
 | username | given_name | password |
 | Stan | Stan Dard | abc123 |
Then I should get a '200' response
And the following user details are returned:
 | username | given_name | admin_flag
 | Stan | Stan Dard | False

Scenario: An admin user wants to create an admin user
Given the admin user is logged in
When the user creates admin user:
 | username | given_name | password |
 | Admin2 | Admin Istrator | def456 |
Then I should get a '200' response
And the following user details are returned:
 | username | given_name | admin_flag
 | Admin2 | Admin Istrator | True

Scenario: A standard user tries to create a user and fails
Given the standard user is logged in
When the user creates standard user:
 | username | given_name | password |
 | Stan | Stan Dard | abc123 |
Then I should get a '403' response
