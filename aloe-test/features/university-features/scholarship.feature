Feature: Scholarships can be added to a university

Scenario: A user wants to add a scholarship
Given the standard user is logged in
And the language is "en"
And the university "University of Life" exists in "en"
When the user adds the scholarship "Available to applicants made of >30% mercury" to university "University of Life"
Then I should get a '200' response
And the following scholarships are returned:
 | university_name | scholarship |
 | University of Life | Available to applicants made of >30% mercury |
And the scholarship "Available to applicants made of >30% mercury" should exist at "University of Life" in language "en"
