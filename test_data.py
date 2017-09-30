"""

This data is used for debugging the website.
Unit and BDD tests use their own datasets.

"""

import os

from flask import current_app

os.environ["GF_CONFIG_CLASS"] = "config.DebugConfig"

from app import app
from app.database import db
from app.models.university import University
from app.models.category import Category
from app.models.course import Course

from app.models.base_model import DeclarativeBase

test_university_data = {
    "National Technical Training Institute": {
        "courses": [
            "Architecture", "Information Technology", "Civil Engineering", "Electrical Engineering", "Electronic Engineering"
        ]
    },
    "Asia Euro University": {
        "courses": [
            "Accounting", "Computer Science", "Electronics and Electricity", "Finance and Banking",
            "Electrical Engineering", "Electronic Engineering", "Chinese for Business", "English",
            "English for Business", "English for Translation and Interpretation", "Law",
            "Management", "Marketing", "Political Science", "Public Administration",
            "International Relations", "Hotel and Tourism Management"
        ]
    },
    "Royal University of Fine Arts": {
        "courses": [
            "Architecture"
        ]
    },
    "Western University": {
        "courses": [
            "Accounting", "Biology", "Chemistry", "Computer Science", "Information Technology",
            "Banking and Finance", "Development Economics", "Teaching English as a Foreign Language",
            "Education and Languages", "English for Communication", "ASEAN Law", "Law", "Management",
            "Marketing", "Hospitality Management", "Hotel and Hospitality Management", "Tourism Management",
            "Tourism and Guide"
        ]
    },
    "IIC University of Technology": {
        "courses": [
            "Business Statistics and Forecasting", "International Business", "Computer Science", "Information Technology",
            "Software Engineering", "Teaching English as a Foreign Language", "Geography", "History",
            "Chinese Language", "English Business Communication", "Japanese Language", "Law", "Legal Studies",
            "Mathematics", "Politcal Science", "Public Administration", "Tourism Management"
        ]
    },
    "O3D Asia Graphic School": {
        "courses": [
            "Graphic Design"
        ]
    },
    "Pannasastra University of Cambodia": {
        "courses": [
            "Accounting", "Architecture and Interior Design", "Interior Design", "Product Design",
            "Banking and Finance", "Business Administration", "Business Information System", "Computer Engineering",
            "Computer Science", "Economics", "Teaching English to Speakers of Other Languages(TESOL)",
            "Early Childhood Education","Civil Engineering", "History", "Anthropology", "Archeology",
            "Asian Studies", "Khmer Studies", "Southeast Asian Studies", "Asian Studies", "English for Communication",
            "Khmer Studies", "Southeast Asian Studies", "Tourism Management", "Marketing", "Communications", "Journalism",
            "Media Management", "Ethnomusicology", "Music", "Environmental Policy and Planning", "Environmental Science",
            "Political Science", "Public Administration", "Philosophy", "Religion", "Anthropology", "Archeology",
            "Asian Studies", "International Relations", "Psychology", "Sociology"
        ]
    },
    "Prek Leap National College ofAgriculture": {
        "courses": [
            "Agribusiness/Economics",
            "Agricultural Economics",
            "Agricultural Extension & Rural Development",
            "Agricultural Management",
            "Agronomy Science",
            "Animal Health & Production",
            "Animal Sciences & Veterinary Medicine",
            "Aquatic Resource",
            "Management & Aquaculture",
            "Fisheries",
            "Food Processing",
            "Food Technology",
            "Forestry",
            "Horticulture"
        ]
    }
}

test_course_data = [
    "Accounting"
    "Agribusiness/Economics"
    "Agricultural Economics"
    "Agricultural Extension & Rural Development"
    "Agricultural Management"
    "Agronomy Science"
    "Animal Health & Production"
    "Animal Sciences & Veterinary Medicine"
    "Anthropology"
    "Aquatic Resource"
    "Archeology"
    "Architecture"
    "Architecture and Interior Design"
    "ASEAN Law"
    "Asian Studies"
    "Banking and Finance"
    "Biology"
    "Business Administration"
    "Business Information System"
    "Business Statistics and Forecasting"
    "Chemistry"
    "Chinese for Business"
    "Chinese Language"
    "Civil Engineering"
    "Communications"
    "Computer Engineering"
    "Computer Science"
    "Development Economics"
    "Early Childhood Education"
    "Economics"
    "Education and Languages"
    "Electrical Engineering"
    "Electronic Engineering"
    "Electronics and Electricity"
    "English"
    "English Business Communication"
    "English for Business"
    "English for Communication"
    "English for Translation and Interpretation"
    "Environmental Policy and Planning"
    "Environmental Science"
    "Ethnomusicology"
    "Finance and Banking"
    "Fisheries"
    "Food Processing"
    "Food Technology"
    "Forestry"
    "Geography"
    "Graphic Design"
    "History"
    "Horticulture"
    "Hospitality Management"
    "Hotel and Hospitality Management"
    "Hotel and Tourism Management"
    "Information Technology"
    "Interior Design"
    "International Business"
    "International Relations"
    "Japanese Language"
    "Journalism"
    "Khmer Studies"
    "Law"
    "Legal Studies"
    "Management"
    "Management & Aquaculture"
    "Marketing"
    "Mathematics"
    "Media Management"
    "Music"
    "Philosophy"
    "Politcal Science"
    "Political Science"
    "Product Design"
    "Psychology"
    "Public Administration"
    "Religion"
    "Sociology"
    "Software Engineering"
    "Southeast Asian Studies"
    "Teaching English as a Foreign Language"
    "Teaching English to Speakers of Other Languages(TESOL)"
    "Tourism and Guide"
    "Tourism Management"
]

test_category_data = {
    "Accounting": ["Accounting", "Banking and Finance", "Finance and Banking"],

    "Agriculture": [
        "Agribusiness/Economics",
        "Agricultural Economics",
        "Agricultural Extension & Rural Development",
        "Agricultural Management",
        "Agronomy Science",
        "Animal Health & Production",
        "Animal Sciences & Veterinary Medicine",
        "Fisheries",
        "Food Processing",
        "Food Technology",
        "Forestry",
        "Horticulture"
    ],

    "Architecture": [
        "Architecture",
        "Architecture and Interior Design"
    ],
    
    "Art and Design": [
        "Architecture and Interior Design",
        "Interior Design"
    ],

    "Biology": ["Biology"],

    "Chemistry": ["Chemistry"],

    "Business": [
        "Banking and Finance",
        "Business Administration",
        "International Business"
    ],

    "Computing": [
        "Business Information Technology",
        "Computer Engineering",
        "Computer Science",
        "Information Technology"
    ],

    "Economics": [
        "Agricultural Economics",
        "Development Economics"
        "Economic Information Program",
        "Economics",
        "Finance and Banking",
    ],

    "Education": [
        "Early Childhood Education",
        "Education and Languages",
        "Teaching English as a Foreign Language",
        "Teaching English to Speakers of Other Languages(TESOL)"
    ],

    "Engineering": [
        "Electrical Engineering",
        "Electronic Engineering",
        "Civil Engineering",
        "Computer Engineering",
        "Electrical and Energy Engineering",
    ],

    "Geography": ["Geography"],
    "History": ["History", "Archaeology"],

    "Humanities": [
        "Anthropology",
        "Archeology",
        "Asian Studies",
        "Khmer Studies",
        "Southeast Asian Studies"
    ],

    "Languages": [
        "Asian Studies",
        "Chinese",
        "Chinese for Business",
        "English",
        "English for Business",
        "English for Communication",
        "Japanese Language",
        "Khmer Studies",
        "Southeast Asian Studies"
    ],

    "Law": [
        "Law",
        "ASEAN Law",
        "Legal Studies"
    ],

    "Management": [
        "Hospitality Management",
        "Hotel and Hospitality Management",
        "Hotel and Tourism Management",
        "Management",
        "Tourism Management",
        "Media Management"
    ],

    "Marketing": [
        "Marketing"
    ],

    "Mathematics": ["Mathematics"],

    "Media": ["Journalism"],

    "Music": [
        "Ethnomusicology",
        "Music"
    ],

    "Other Sciences": [
        "Environmental Science",
        "Environmental Policy and Planning"
    ],

    "Politics": [
        "Political Science"
    ],

    "Public Sector": ["Public Administration"],

    "Religion and Philosophy": [
        "Religion",
        "Philosophy"
    ],

    "Social Sciences": [
        "International Relations",
        "Psychology",
        "Sociology",
    ],

    "Tourism": [
        "Hotel and Tourism Management"
    ]
}

if __name__ == "__main__":

    with app.app_context():
        DeclarativeBase.metadata.drop_all(bind=db.engine)
        DeclarativeBase.metadata.create_all(bind=db.engine)

        universities = {university: University.create(university, "en") for university in test_university_data}
        categories = {category: Category.create(category, "en") for category in test_category_data}
        courses = {course: Course.create(course, "en") for course in test_course_data}