Feature: Admissions can be added to a university

Scenario: A user wants to add an admission
Given the standard user is logged in
And the language is "en"
And the university "University of Life" exists in "en"
When the user adds the admission "Bronze Swimming Certificate" to university "University of Life"
Then I should get a '200' response
And the following admissions are returned:
 | university_name | admission |
 | University of Life | Bronze Swimming Certificate |
And the admission "Bronze Swimming Certificate" should exist at "University of Life" in language "en"
