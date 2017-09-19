Feature: Tutition fees can be added to a university

Scenario: A user wants to add some tuition fees
Given the standard user is logged in
And the language is "en"
And the university "University of Life" exists in "en"
When the user adds the tuition fee "1000000USD" per year for a "Swimming Certificate" to university "University of Life"
Then I should get a '200' response
And the following tuition fees are returned:
 | university_name | tuition_fee | currency | award | period |
 | University of Life | 1000000 | USD | Swimming Certificate | year |
And the tuition fees 1000000 USD per year for a "Swimming Certificate" should exist at "University of Life" in language "en"
