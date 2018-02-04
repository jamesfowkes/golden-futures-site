Feature: Categories can be created

Scenario: A user wants to create a category
Given the standard user is logged in
And the user sets the category "Pet Care" as pending for creation
Then I should get a '200' response
And the category "Pet Care" should be pending for creation

Scenario: A user accepts creation of a category
Given the standard user is logged in
And the category "Pet Care" is pending for creation
And the user accepts pending changes to category "Pet Care"
Then I should get a '200' response
And the following category details are returned:
 | category_name | language |
 | Pet Care | en |
And the category "Pet Care" should exist in language "en"

Scenario: A user wants to create a category in a non-english language
Given the french user is logged in
And the language is "fr"
And the user sets the category "French Pet Care" as pending for creation
Then I should get a '200' response
And the category "French Pet Care" should be pending for creation in language "fr"
