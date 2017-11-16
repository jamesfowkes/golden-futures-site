Feature: Users can login and logout

Scenario: An invalid login attempt is rejected on username
Given the standard user is not logged in
When a login attempt is made with credentials:
 | username | password |
 | notausername | abc123 |
Then I should be redirected to '/login'

Scenario: An invalid login attempt is rejected on password
Given the standard user is not logged in
When a login attempt is made with credentials:
 | username | password |
 | standard | badpassword |
Then I should be redirected to '/login'