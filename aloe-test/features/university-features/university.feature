Feature: Universities can be created in any language and translations can then be added

Scenario: A user wants to add a university
Given the standard user is logged in
And the language is "en"
When the user adds the university "University of Life"
Then I should get a '200' response
And the following university details are returned:
 | university_name | language |
 | University of Life | en |
And the university "University of Life" should exist