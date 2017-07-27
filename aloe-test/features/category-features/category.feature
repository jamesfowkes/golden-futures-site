Feature: Categories can be added

Scenario: A user wants to add a category
And the standard user is logged in
When the user adds the category "Pet Care"
Then I should get a '200' response
And the following category details are returned:
 | category_name | courses |
 | Pet Care | |
And the category "Pet Care" should exist
