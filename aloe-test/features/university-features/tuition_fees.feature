Feature: Tuition fees can be added to a university

Scenario: A user wants to pend creating a tuition fee and approve it
Given the standard user is logged in
And the university "University of Life" exists
And the university "University of Life" is pending for edit
When the user pends addtion of tuition fee "1000000USD" per year for a "Swimming Certificate" to university "University of Life"
Then I should get a '200' response
And the tuition fee "1000000USD" per year for a "Swimming Certificate" should be pending for creation at "University of Life"
When the user approves the user approves pending changes to university "University of Life"
Then I should get a '200' response
And the tuition fee "1000000USD" per year for a "Swimming Certificate" should exist at "University of Life"
