Feature: Courses can be edited and deleted

Scenario: A user wants to rename a course
Given the standard user is logged in
And the course "Advanced Hamster Training" exists
When the user pends translation "Advanced Hamster and Gerbil Training" in "en" for course "Advanced Hamster Training"
Then I should get a '200' response
And the course "Advanced Hamster Training" should be pending for edit as "Advanced Hamster and Gerbil Training"
When the user accepts pending changes to course "Advanced Hamster and Gerbil Training"
Then the course "Advanced Hamster and Gerbil Training" should exist
Then the course "Advanced Hamster Training" should not exist
