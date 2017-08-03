import aloe

from nose.tools import assert_equals

@aloe.step(u'I should get a \'(.*)\' response')
def i_should_get_response(step, expected_status_code):
    assert_equals(aloe.world.response.status_code, int(expected_status_code))

@aloe.step(u'the language is \"(\w*)\"')
def the_language_is(step, language):
    aloe.world.language = language