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
And the following university details are correct in response:
    """
    {
        "translations": {
            "en": {
                "university_name": "University of Life",
                "university_intro": null
            },
            "fr": {
                "university_name": null,
                "university_intro": null
            }
        }
    }
    """
And the university "University of Life" should exist in "en"

Scenario: A user wants to edit a university name and intro
Given the standard user is logged in
And the university "University of Life" exists
When the user pends the following data to it:
    | university_name | university_intro | language |
    | University of Life | We teach you stuff | en |
    | Université de la Vie | We teach you stuff in French | fr |
Then I should get a '200' response
And the following data is pending for that university
    """
    {
        "translations": {
            "en": {
                "university_name": "University of Life",
                "university_intro": "We teach you stuff"
            },
            "fr": {
                "university_name": "Université de la Vie",
                "university_intro": "We teach you stuff in French"
            }
        }
    }
    """

Scenario: A user wants to edit university courses
Given the standard user is logged in
And the university "University of Life" exists
And the course "Test Course 1" exists
And the course "Test Course 2" exists
When the user pends those courses to that university
Then I should get a '200' response
And those courses should be pending for addition

Scenario: A user wants to approve addition of a university name translation
Given the standard user is logged in
And the university "University of Life" exists
And the translation "Université de la Vie" in "fr" of university "University of Life" is pending
When the user approves the user approves pending changes to university "University of Life"
Then I should get a '200' response
And the following university details are correct in response:
    """
    {
        "translations": {
            "en": {
                "university_name": "University of Life",
                "university_intro": null
            },
            "fr": {
                "university_name": "Université de la Vie",
                "university_intro": null
            }
        }
    }
    """
