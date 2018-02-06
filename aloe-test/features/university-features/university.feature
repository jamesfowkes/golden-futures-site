Feature: Universities can be created in any language and translations can then be added

Scenario: A user wants to pend addition of a university
Given the standard user is logged in
When the user pends addition of university "University of Life"
Then I should get a '200' response

Scenario: A user wants to approve addition of a university
Given the standard user is logged in
Given the university "University of Life" is pending for addition
When the user approves the user approves pending changes to university "University of Life"
Then I should get a '200' response
And the following university details are returned:
 | university_name | language |
 | University of Life | en |
And the university "University of Life" should exist in "en"

Scenario: A user wants to add a university name translation
Given the standard user is logged in
And the university "University of Life" exists
When the user pends addition of translation "Université de la Vie" in "fr" to university "University of Life"
Then I should get a '200' response

Scenario: A user wants to approve addition of a university name translation
Given the standard user is logged in
And the university "University of Life" exists
And the translation "Université de la Vie" in "fr" of university "University of Life" is pending
When the user approves the user approves pending changes to university "University of Life"
Then I should get a '200' response
And the following university details are returned:
 | university_name | language |
 | University of Life | en |
 | Université de la Vie | fr |
And the university "Université de la Vie" should exist in "fr"
And the university "University of Life" should have "fr" translation "Université de la Vie"
