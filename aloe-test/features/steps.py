import aloe
from urllib.parse import urlparse

from nose.tools import assert_equals

from flask import request, g

from app import app

@aloe.step(u'I should get a \'(.*)\' response')
def i_should_get_response(step, expected_status_code):
    assert_equals(aloe.world.response.status_code, int(expected_status_code))

@aloe.step(u'I should be redirected to \'(.*)\'')
def i_should_be_redirected_to(step, expected_path):

    assert_equals(urlparse(aloe.world.response.location).path, expected_path)

@aloe.step(u'the language is \"(\w*)\"')
def the_language_is(step, language):
    aloe.world.language = language
