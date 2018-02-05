Feature: Admissions can be added to a university

Scenario: A user wants to pend creating an admission and approve it
Given the standard user is logged in
And the university "University of Life" exists
And the university "University of Life" is pending for edit
When the user pends creation of admission "Bronze Swimming Certificate" for university "University of Life"
Then I should get a '200' response
And the admission "Bronze Swimming Certificate" should be pending for creation at "University of Life"

#And the university "University of Life" exists
#And the admission ""
#When the user pends addition of admission "Bronze Swimming Certificate" to university "University of Life"
#Then I should get a '200' response
#And the following admissions are returned:
# | university_name | admission |
# | University of Life | Bronze Swimming Certificate |
#And the admission "Bronze Swimming Certificate" should exist at "University of Life" in language "en"
