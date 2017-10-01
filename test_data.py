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
from app.models.admission import Admission
from app.models.scholarship import Scholarship
from app.models.tuition_fee import TuitionFee
from app.models.contact_detail import ContactDetail
from app.models.facility import Facility

from app.models.base_model import DeclarativeBase

test_university_data = {
    "National Technical Training Institute": {
        "courses": [
            "Architecture", "Information Technology", "Civil Engineering", "Electrical Engineering", "Electronic Engineering"
        ],
        "admission": [
            "Bachelor Degree:BAC II Certificate, or High Diploma of Technical or Specialty, or Associate Degree."
        ],
        "tuition_fees": [
            {
                "min": 380,
                "max": 450,
                "currency": "$",
                "award": "Bachelor Degree",
                "period": "year"
            }
        ],
        "scholarships": [
            "100% Scholarship to Senior and Junior Technical Students in Pedagogy.",
            "50% Scholarship to Female Students in Civil Engineering, Electrical Engineering, Electronic Engineering, Architecture, and IT.",
            "Student ranked 1 st : 50% scholarship",
            "Student ranked 2 nd : 30% scholarship",
            "Student ranked 3 rd : 20% scholarship",
            "Student ranked 4th and 5 th : 10% scholarship"
        ],
        "contact_details": [
            "www.ntti.edu.kh",
            "info@ntti.edu.kh",
            "023 883 039"
        ],
        "facilities": []
    },

    "Asia Euro University": {
        "courses": [
            "Accounting", "Computer Science", "Electronics and Electricity", "Finance and Banking",
            "Electrical Engineering", "Electronic Engineering", "Chinese for Business", "English",
            "English for Business", "English for Translation and Interpretation", "Law",
            "Management", "Marketing", "Political Science", "Public Administration",
            "International Relations", "Hotel and Tourism Management"
        ],
        "admission": [
            "Foundation Year: BACC II Certificate and Pass Entrance Exam",
            "Bachelor Degree: Foundation Year Certificate and Pass Entrance Exam",
            "Associate Degree: Pass/Fail BACC II Certificate and Pass Entrance Exam",
        ],
        "tuition_fees": [
            {
                "min": 360,
                "max": 400,
                "currency": "$",
                "award": "Bachelor Degree",
                "period": "year"
            }
        ],
        "scholarships": [
            "Grade A- 100%",
            "Grade B- 40%",
            "Grade C- 30%",
            "Grade D- 25%",
            "Grade E- 20%",
        ],
        "contact_details": [
            "www.aeu.edu.kh",
            "Email: info@aeu.edu.kh",
            "www.facebook.com/aeucamboadia",
            "Phone:(855)23 998 124 / 1572 00 72"
        ],
        "facilities": []
    },

    "Royal University of Fine Arts": {
        "courses": [
            "Architecture"
        ],
        "admission": [
            "Bachelor Degree:High School Diploma or Equivalent",
        ],
        "tuition_fees": [
            {
                "min": 380,
                "max": 480,
                "currency": "$",
                "award": "Bachelor Degree",
                "period": "year"
            }
        ],
        "scholarships": [
            "Scholarships are only available from the government.",
            "30 students a year receive a scholarship.",
            "You should apply through your high school."
        ],
        "contact_details": [
            "www.rufa.edu.kh",
            "rufa@camnet.com.kh",
            "023 986 417",
            "012 444 589",
            "No. 72, Street 19"
        ],
        "facilities": []
    },

    "Western University": {
        "courses": [
            "Accounting", "Biology", "Chemistry", "Computer Science", "Information Technology",
            "Banking and Finance", "Development Economics", "Teaching English as a Foreign Language",
            "Education and Languages", "English for Communication", "ASEAN Law", "Law", "Management",
            "Marketing", "Hospitality Management", "Hotel and Hospitality Management", "Tourism Management",
            "Tourism and Guide"
        ],
        "admission": [
            "Foundation Year / Bachelor Degree: High School Diploma or equivalent. Pass entrance exam.",
            "Associate Degree: High School Diploma or equivalent, or certificate of completion of Grade 12. Pass entrance exam."
        ],
        "tuition_fees": [
            {
                "min": 450,
                "max": 450,
                "currency": "$",
                "award": "Bachelor Degree",
                "period": "year"
            },
            {
                "min": 450,
                "max": 450,
                "currency": "$",
                "award": "Associate Degree",
                "period": "year"
            }
        ],
        "scholarships": [
            "Grade A: 100% scholarship",
            "Grade B: $240",
            "Grade C: $300",
            "Grade D: $360",
            "Grade E: 0% scholarship"
        ],
        "contact_details": [
            "www.western.edu.kh",
            "info@western.edu.kh",
            "023 998 233",
            "No. 15, Street 173"
        ],
        "facilities": [
            "Library",
            "Cafeteria",
            "Computer Lab",
            "Smart boards and Projectors",
            "Conference Hall"
        ]
    },

    "IIC University of Technology": {
        "courses": [
            "Business Statistics and Forecasting", "International Business", "Computer Science", "Information Technology",
            "Software Engineering", "Teaching English as a Foreign Language", "Geography", "History",
            "Chinese Language", "English Business Communication", "Japanese Language", "Law", "Legal Studies",
            "Mathematics", "Political Science", "Public Administration", "Tourism Management"
        ],
        "admission": [
            "High School Diploma or an equivalent.",
        ],
        "tuition_fees": [
            {
                "min": 390,
                "max": 440,
                "currency": "$",
                "award": "Bachelor Degree",
                "period": "year"
            },
            {
                "min": 360,
                "max": 360,
                "currency": "$",
                "award": "Associate Degree",
                "period": "year"
            }
        ],
        "scholarships": [
            "No Scholarships available."
        ],
        "contact_details": [
            "www.iic.edu.kh",
            "info@iic.edu.kh",
            "023 425 148",
            "No. 650, Street 2"
        ],
        "facilities": []
    },

    "O3D Asia Graphic School": {
        "courses": [
            "Graphic Design"
        ],
        "admission": [
            "High School Diploma or equivalent.",
            "You also need to be motivated by a real interest in the domain and have a basic artistic knowledge."
        ],
        "tuition_fees": [
            {
                "min": 2500,
                "max": 2500,
                "currency": "$",
                "award": "Bachelor Degree",
                "period": "year"
            },
            {
                "min": 90,
                "max": 90,
                "currency": "$",
                "award": "Application Fee (non-refundable)",
                "period": ""
            }
        ],
        "scholarships": [
            "O3D Asia Graphic School does not offer any Scholarships.",
            "CMK Bank offers full funding through loans to be reimbursed once the student is in full employed."
        ],
        "contact_details": [
            "www.o3dasia.com",
            "contact@o3dasia.com",
            "+855 (0) 92 968 912",
            "No. 108ABCD Mao Tse Toung Blvd"
        ],
        "facilities": []
    },

    "Pannasastra University of Cambodia": {
        "courses": [
            "Accounting", "Architecture and Interior Design", "Interior Design", "Product Design",
            "Banking and Finance", "Business Administration", "Business Information System", "Computer Engineering",
            "Computer Science", "Economics", "Teaching English to Speakers of Other Languages(TESOL)",
            "Early Childhood Education", "Civil Engineering", "History", "Anthropology", "Khmer Studies",
            "Southeast Asian Studies", "Asian Studies", "English for Communication", "Tourism Management",
            "Marketing", "Communications", "Journalism", "Media Management", "Ethnomusicology", "Music",
            "Environmental Policy and Planning", "Environmental Science", "Political Science", "Public Administration",
            "Philosophy", "Religion", "Anthropology", "Archaeology", "International Relations",
            "Psychology", "Sociology"
        ],
        "admission": [
            "Lycee Baccalaureate, High School Diploma or equivalent."
            "Pass Admission Test (covers Mathematics, Physics Chemistry, Science and General Knowledge).",
            "Pass English Placement Test (grade D or higher).",
            "Obtained IELTS score of 5.5 or TOFEL score of 500"
        ],
        "tuition_fees": [
            {
                "min": 774,
                "max": 774,
                "currency": "$",
                "award": "Bachelor Degree",
                "period": "year"
            },
            {
                "min": 774,
                "max": 774,
                "currency": "$",
                "award": "Associate Degree",
                "period": "year"
            }
        ],
        "scholarships": [
            "Grade A: 100% Scholarship",
            "Grade B: Partial Scholarship",
            "All scholarships are only valid for one year. Students must reapply by September 31st of each academic year"
        ],
        "contact_details": [
            "www.puc.edu.kh",
            "info@puc.edu.kh",
            "023 990 153",
            "012 681 606",
            "No. 92-94, Vithei Samdech Sothearos"
        ],
        "facilities": []
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
        ],
       "admission": [
            "High School Diploma or equivalent"
        ],
        "tuition_fees": [
            {
                "min": 380,
                "max": 380,
                "currency": "$",
                "award": "Bachelor Degree",
                "period": "year"
            },
            {
                "min": 330,
                "max": 330,
                "currency": "$",
                "award": "Associate Degree",
                "period": "year"
            }
        ],
        "scholarships": [
            "Prek Leap offers between 300-500 scholarships each academic year.",
            "They are dependent on student grades.",
            "Students need to apply through the University."
        ],
        "contact_details": [
            "www.pnsa.edu.kh",
            "info@pnsa.edu.kh",
            "+855 162 695 62",
            "National Road 6A"
        ],
        "facilities": []
    }
}

test_course_data = [
    "Accounting",
    "Agribusiness/Economics",
    "Agricultural Economics",
    "Agricultural Extension & Rural Development",
    "Agricultural Management",
    "Agronomy Science",
    "Animal Health & Production",
    "Animal Sciences & Veterinary Medicine",
    "Anthropology",
    "Aquatic Resource",
    "Archaeology",
    "Architecture",
    "Architecture and Interior Design",
    "ASEAN Law",
    "Asian Studies",
    "Banking and Finance",
    "Biology",
    "Business Administration",
    "Business Information System",
    "Business Statistics and Forecasting",
    "Chemistry",
    "Chinese for Business",
    "Chinese Language",
    "Chinese",
    "Civil Engineering",
    "Communications",
    "Computer Engineering",
    "Computer Science",
    "Development Economics",
    "Early Childhood Education",
    "Economics",
    "Education and Languages",
    "Electrical Engineering",
    "Electronic Engineering",
    "Electronics and Electricity",
    "English",
    "English Business Communication",
    "English for Business",
    "English for Communication",
    "English for Translation and Interpretation",
    "Environmental Policy and Planning",
    "Environmental Science",
    "Ethnomusicology",
    "Finance and Banking",
    "Fisheries",
    "Food Processing",
    "Food Technology",
    "Forestry",
    "Geography",
    "Graphic Design",
    "History",
    "Horticulture",
    "Hospitality Management",
    "Hotel and Hospitality Management",
    "Hotel and Tourism Management",
    "Information Technology",
    "Interior Design",
    "International Business",
    "International Relations",
    "Japanese Language",
    "Journalism",
    "Khmer Studies",
    "Law",
    "Legal Studies",
    "Management",
    "Management & Aquaculture",
    "Marketing",
    "Mathematics",
    "Media Management",
    "Music",
    "Philosophy",
    "Political Science",
    "Product Design",
    "Psychology",
    "Public Administration",
    "Religion",
    "Sociology",
    "Software Engineering",
    "Southeast Asian Studies",
    "Teaching English as a Foreign Language",
    "Teaching English to Speakers of Other Languages(TESOL)",
    "Tourism and Guide",
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
        "Business Information System",
        "Computer Engineering",
        "Computer Science",
        "Information Technology"
    ],

    "Economics": [
        "Agricultural Economics",
        "Development Economics",
        "Economics",
        "Finance and Banking"
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
    ],

    "Geography": ["Geography"],
    "History": ["History", "Archaeology"],

    "Humanities": [
        "Anthropology",
        "Archaeology",
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

        # Create categories and courses and link them together
        categories = {category: Category.create(category, "en") for category in test_category_data}
        courses = {course: Course.create(course, "en") for course in test_course_data}

        for category, cat_courses in test_category_data.items():
            for course in cat_courses:
                categories[category].add_course(courses[course])

        # Create universities and link to courses
        universities = {university: University.create(university, "en") for university in test_university_data}

        for university, uni_data in test_university_data.items():
            for course in uni_data["courses"]:
                universities[university].add_course(courses[course])

            for admission in uni_data["admission"]:
                Admission.create(universities[university].university_id, admission, "en")

            for tuition_fee in uni_data["tuition_fees"]:
                TuitionFee.create(
                    universities[university].university_id,
                    tuition_fee["min"], tuition_fee["max"], 
                    tuition_fee["currency"], tuition_fee["period"],
                    tuition_fee["award"], "en"
                )

            for scholarship in uni_data["scholarships"]:
                Scholarship.create(universities[university].university_id, scholarship, "en")

            for contact_detail in uni_data["contact_details"]:
                ContactDetail.create(universities[university].university_id, contact_detail, "en")

            for facility in uni_data["facilities"]:
                Facility.create(universities[university].university_id, facility, "en")
