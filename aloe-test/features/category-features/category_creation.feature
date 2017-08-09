Feature: Categories can be created

Scenario: A user wants to create a category
Given the standard user is logged in
When the user creates the category "Pet Care"
Then I should get a '200' response
And the following category details are returned:
 | category_name | language |
 | Pet Care | en |
And the category "Pet Care" should exist in language "en"

Scenario: A user wants to create a category in a non-english language
Given the standard user is logged in
And the language is "fr"
When the user creates the category "French Pet Care"
Then I should get a '200' response
And the following category details are returned:
 | category_name | language |
 | French Pet Care | fr |
And the category "French Pet Care" should exist in language "fr"
