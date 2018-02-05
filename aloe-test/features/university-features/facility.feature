Feature: Facilities can be added to a university

Scenario: A user wants to pend creating a set of facilities and approve it
Given the standard user is logged in
And the university "University of Life" exists
And the university "University of Life" is pending for edit
When the user pends creation of facility "All you can eat biros" for university "University of Life"
Then I should get a '200' response
And the facility "All you can eat biros" should be pending for creation at "University of Life"
When the user approves the user approves pending changes to university "University of Life"
Then I should get a '200' response
And the facility "All you can eat biros" should exist at "University of Life" in language "en"
