Feature: Users can login and logout

Scenario: An invalid login attempt is rejected on username
Given the standard user is in the system
And the standard user is not logged in
When a login attempt is made with credentials:
 | username | password |
 | standard | badpassword |
Then I should get a '401' response