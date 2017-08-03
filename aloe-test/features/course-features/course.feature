Feature: Courses can be created and added to a category

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

Scenario: A user wants to add a course with a name in a nonenglish langauge
Given the standard user is logged in
And the language is "fr"
And the category "Pet Care" exists
When the user adds the course "Reptiles de base" to category "Pet Care"
Then I should get a '200' response
And the following course details are returned:
 | course_name | category_name |
 | Reptiles de base | Pet Care |
And the course "Reptiles de base" should exist
And the category "Pet Care" should have the courses:
 | course_name |
 | Reptiles de base |

Scenario: A user wants to add a translation to a course name
Given the standard user is logged in
And the category "Pet Care" exists
And the course "Basic Reptiles" exists in category "Pet Care"
And the language is "fr"
When the user adds the translation "Reptiles de base" to course "Basic Reptiles"
Then I should get a '200' response
And the following course details are returned:
 | course_name | category_name |
 | Reptiles de base | Pet Care |
And the course "Reptiles de base" should have the translations:
 | en | fr |
 | Basic Reptiles | Reptiles de base |