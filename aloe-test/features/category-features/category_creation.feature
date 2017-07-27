Feature: Categories can be created

Scenario: A user wants to create a category
And the standard user is logged in
When the user creates the category "Pet Care"
Then I should get a '200' response
And the following category details are returned:
 | category_name | courses |
 | Pet Care | |
And the category "Pet Care" should exist
