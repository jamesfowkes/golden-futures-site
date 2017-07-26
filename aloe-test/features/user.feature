Feature: Handle creating users

Scenario: An admin user wants to create a standard user
Given the admin user is in the system
And the admin user is logged in
When the admin user creates standard user
 | username | given_name | password |
 | Stan | Stan Dard | abc123 |
 
Then I should get a '200' response
And the following user details are returned:
 | username | given_name | admin_flag
 | Stan | Stan Dard | False
