Feature: Facilities can be added to a university

Scenario: A user wants to add a facility
Given the standard user is logged in
And the language is "en"
And the university "University of Life" exists in "en"
When the user adds the facility "All you can eat biros" to university "University of Life"
Then I should get a '200' response
And the following facility details are returned:
 | university_name | facility |
 | University of Life | All you can eat biros |
And the facility "All you can eat biros" should exist at "University of Life" in language "en"
