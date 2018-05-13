import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import University, UniversityPending
from app.models.quote import QuotePending
        
@aloe.step(u'the user pends creation of quote \"([\w\d ]*)\" for university \"([\w\d ]*)\"')
def the_user_pends_creation_of_quote(step, quote, university_name):
    aloe.world.quote = quote
    with app.test_request_context():
        university_id = University.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/quote/create'.format(university_id), 
            data={
                'university_id':university_id,
                'quote': quote,
                'language': aloe.world.language
            }
        )

@aloe.step(u'And that quote should be pending for creation at \"([\w\d ]*)\"')
def the_quote_should_be_pending_for_creation(step, university_name):
    quote = aloe.world.quote
    with app.app_context():
        university = UniversityPending.get_single(university_name=university_name)
        pending_quotes = QuotePending.get(university=university).all()
        quote_strings = [quote.translations[aloe.world.language].quote_string for quote in pending_quotes]
        assert(quote in quote_strings)

@aloe.step(u'And that quote should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_quote_should_exist(step, university_name, language):
    quote = aloe.world.quote
    with app.test_request_context():
        university = University.get_by_name(university_name=university_name, language=aloe.world.language)
        quotes = [f.quote_string for f in university.quotes]
        assert(quote in quotes)
