Feature: Courses can be created and added to a category

Scenario: A user wants to create a new course
Given the standard user is logged in
And the user sets the course "Advanced Hamster Training" as pending for creation
Then I should get a '200' response
And the course "Advanced Hamster Training" should be pending for creation

Scenario: A user wants to approve creation of a course
Given the standard user is logged in
And the course "Advanced Hamster Training" is pending for creation
And the user accepts the creation of course "Advanced Hamster Training"
Then I should get a '200' response
And the following course details are returned:
 | course_name | category_names | language |
 | Advanced Hamster Training | | en |
And the course "Advanced Hamster Training" should exist

Scenario: A user wants to add an existing course to an empty category
Given the standard user is logged in
And the category "Pet Care" exists
And the course "Advanced Hamster Training" exists
When the user pends addition of course "Advanced Hamster Training" to category "Pet Care"
Then I should get a '200' response
And the course "Advanced Hamster Training" should be pending to be added to category "Pet Care"

Scenario: A user wants to approve adding a course to a category
Given the standard user is logged in
And the category "Pet Care" exists
And the course "Advanced Hamster Training" exists
And the course "Advanced Hamster Training" is pending to be added to category "Pet Care"
And the user accepts pending changes to category "Pet Care"
Then I should get a '200' response
And the category "Pet Care" should have the courses:
 | course_name | language |
 | Advanced Hamster Training | en |

Scenario: A user wants to pend adding a course to a category with courses in
Given the standard user is logged in
And the category "Pet Care" exists
And the course "Advanced Hamster Training" exists
And the course "Advanced Hamster Training" is in category "Pet Care"
And the course "Yak Shaving" exists
When the user pends addition of course "Yak Shaving" to category "Pet Care"
Then I should get a '200' response
And the course "Yak Shaving" should be pending to be added to category "Pet Care"

Scenario: A user wants to approve addition of a course to a category with courses in
Given the standard user is logged in
And the category "Pet Care" exists
And the course "Advanced Hamster Training" exists
And the course "Advanced Hamster Training" is in category "Pet Care"
And the course "Yak Shaving" exists
And the course "Yak Shaving" is pending to be added to category "Pet Care"
And the user accepts pending changes to category "Pet Care"
Then I should get a '200' response
And the category "Pet Care" should have the courses:
 | course_name | language |
 | Advanced Hamster Training | en |
 | Yak Shaving | en |

Scenario: A user wants to add a course with a name in a nonenglish language
Given the french user is logged in
And the language is "fr"
And the category "Pet Care" exists
And the course "Reptiles de base" exists
When the user pends addition of course "Reptiles de base" to category "Pet Care"
Then I should get a '200' response
And the course "Reptiles de base" should be pending to be added to category "Pet Care"

Scenario: A user wants to approve adding a course to a category in a nonenglish language
Given the standard user is logged in
And the language is "fr"
And the category "Pet Care" exists
And the course "Reptiles de base" exists
And the course "Reptiles de base" is pending to be added to category "Pet Care"
When the user accepts pending changes to category "Pet Care"
Then I should get a '200' response
And the category "Pet Care" should have the courses:
 | course_name | language |
 | Reptiles de base | fr |

Scenario: A user wants to add a translation to a course name
Given the french user is logged in
And the category "Pet Care" exists
And the course "Basic Reptiles" exists
And the course "Basic Reptiles" exists in category "Pet Care"
When the translation "Reptiles de base" in "fr" is pending to be added to course "Basic Reptiles"
Then I should get a '200' response
When the user accepts pending changes to course "Basic Reptiles"
Then I should get a '200' response
And the course "Basic Reptiles" should have the "en" translations:
 | course_name |
 | Basic Reptiles |
And the course "Basic Reptiles" should have the "fr" translations:
 | course_name |
 | Reptiles de base |
