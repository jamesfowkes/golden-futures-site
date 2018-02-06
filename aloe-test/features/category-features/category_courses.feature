Feature: Courses can be added to categories

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

Scenario: A user wants to pend adding a course to more than one category
Given the standard user is logged in
And the category "Pet Care" exists
And the category "Animal Entertainment" exists
And the course "Advanced Hamster Training" exists
When the user pends addition of course "Advanced Hamster Training" to category "Animal Entertainment"
Then I should get a '200' response
And the course "Advanced Hamster Training" should be pending to be added to category "Animal Entertainment"
When the user pends addition of course "Advanced Hamster Training" to category "Pet Care"
Then I should get a '200' response
And the course "Advanced Hamster Training" should be pending to be added to category "Pet Care"
