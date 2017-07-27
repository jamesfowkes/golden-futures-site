Feature: Courses can be added and assigned to a category

Scenario: A user wants to add a course to an empty category
Given the standard user is logged in
And the category "Pet Care" exists
When the user adds the course "Advanced Hamster Training" to category "Pet Care"
Then I should get a '200' response
And the following course details are returned:
 | course_name | category_name |
 | Advanced Hamster Training | Pet Care |
And the course "Advanced Hamster Training" should exist
And the category "Pet Care" should have the courses:
 | course_name |
 | Advanced Hamster Training |

Scenario: A user wants to add a course to a category with courses in
Given the standard user is logged in
And the category "Pet Care" exists
And the course "Advanced Hamster Training" exists in category "Pet Care"
When the user adds the course "Yak Shaving" to category "Pet Care"
Then I should get a '200' response
And the following course details are returned:
 | course_name | category_name |
 | Yak Shaving | Pet Care |
And the course "Advanced Hamster Training" should exist
And the category "Pet Care" should have the courses:
 | course_name |
 | Advanced Hamster Training |
 | Yak Shaving |
