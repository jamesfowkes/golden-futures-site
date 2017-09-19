Feature: Contact details can be added to a university

Scenario: A user wants to add some contact details
Given the standard user is logged in
And the language is "en"
And the university "University of Life" exists in "en"
When the user adds the contact detail "enquiries@uol.ac" to university "University of Life"
Then I should get a '200' response
And the following contact details are returned:
 | university_name | contact_detail |
 | University of Life | enquiries@uol.ac |
And the contact detail "enquiries@uol.ac" should exist at "University of Life" in language "en"
