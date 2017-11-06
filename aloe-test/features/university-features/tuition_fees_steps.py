import os

import json

import aloe

from nose.tools import assert_equals

import flask_login
import sqlalchemy

from app import app
from app.database import db

from app.models.university import UniversityPending

def split_currency_string(tuition_fee):
    return tuition_fee[0:-3], tuition_fee[-3:]

def tuition_fee_matches(f, tuition_fee, currency, period, award):
    matches = True
    matches &= f.tuition_fee_min == int(tuition_fee)
    matches &= f.tuition_fee_max == int(tuition_fee)
    matches &= f.currency == currency
    matches &= f.period == period
    matches &= f.award == award

    return matches

@aloe.step(u'the user adds the tuition fee \"([\w\d ]*)\" per (\w*) for a \"([\w\d ]*)\" to university \"([\w\d ]*)\"')
def the_user_creates_the_tuition_fee(step, tuition_fee, period, award, university_name):

    tuition_fee, currency = split_currency_string(tuition_fee)
    with app.test_request_context():

        university_id = UniversityPending.get_by_name(university_name=university_name, language=aloe.world.language).university_id

        aloe.world.response = aloe.world.app.post(
            '/tuition_fee/create', 
            data={
                'university_id':university_id,
                'tuition_fee': tuition_fee,
                'currency':currency,
                'award':award,
                'period':period,
                'language':aloe.world.language
            },
        )

@aloe.step(u'the following tuition fees are returned:')
def the_following_tuition_fee_details_are_returned(step):
    returned_json = json.loads(aloe.world.response.data.decode("utf-8"))
    returned_json.pop("tuition_fee_id")

    step.hashes[0]["tuition_fee_min"] = int(step.hashes[0]["tuition_fee_min"])
    step.hashes[0]["tuition_fee_max"] = int(step.hashes[0]["tuition_fee_max"])
    assert_equals(step.hashes[0], returned_json)

@aloe.step(u'And the tuition fees (\d*) (\w*) per (\w*) for a \"([\w\d ]*)\" should exist at \"([\w\d ]*)\" in language \"([\w\d ]*)\"')
def the_tuition_fee_should_exist(step, tuition_fee, currency, period, award, university_name, language):
    with app.test_request_context():
        university = UniversityPending.get_by_name(university_name=university_name, language=aloe.world.language)
        exists = any([tuition_fee_matches(f, tuition_fee, currency, period, award) for f in university.tuition_fees])
        assert exists