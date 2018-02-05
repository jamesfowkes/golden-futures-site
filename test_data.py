""" test_data.py

Usage:
    test_data.py create_baseline
    test_data.py create_pending
    test_data.py copy
    test_data.py make_original

Options:
    --add_pending    Add a set of pending changes

This data is used for debugging the website.
Unit and BDD tests use their own datasets.

"""

import os
import sys
import shutil

import docopt

from flask import current_app

os.environ["GF_CONFIG_CLASS"] = "config.DebugConfig"

from app import app
from app.database import db
from app.models.university import University, UniversityPending, UniversityPendingTranslation, UniversityPendingCourse
from app.models.category import Category, CategoryPending, CategoryPendingTranslation, CategoryPendingCourses
from app.models.course import Course, CoursePending, CoursePendingTranslation
from app.models.admission import Admission, AdmissionPending, AdmissionPendingTranslation
from app.models.scholarship import Scholarship, ScholarshipPending, ScholarshipPendingTranslation
from app.models.tuition_fee import TuitionFee, TuitionFeePending, TuitionFeePendingTranslation
from app.models.contact_detail import ContactDetail, ContactDetailPending, ContactDetailPendingTranslation
from app.models.facility import Facility, FacilityPending, FacilityPendingTranslation
from app.models.user import User

from app.models.base_model import DeclarativeBase

def khmer(s):
    return "!" + s + "!"

PENDING_TABLES = [CategoryPending, CoursePending, UniversityPending, TuitionFeePending, AdmissionPending,
    ContactDetailPending, FacilityPending, ScholarshipPending, CategoryPendingTranslation, CoursePendingTranslation,
    UniversityPendingTranslation, TuitionFeePendingTranslation, AdmissionPendingTranslation, 
    ContactDetailPendingTranslation, FacilityPendingTranslation, ScholarshipPendingTranslation,
    CategoryPendingCourses, UniversityPendingCourse]
    
def drop_all_pending_tables():
    
    for table in PENDING_TABLES:
        try:
            table.__table__.drop(bind=db.engine)
        except:
            pass

        table.__table__.create(bind=db.engine)

def load_courses_from_db(test_course_data):
    return {course_name: Course.get_single(course_name=course_name, language="en") for course_name in test_course_data}

def load_categories_from_db(test_category_data):
    return {category_name: Category.get_single(category_name=category_name, language="en") for category_name in test_category_data}

def load_universities_from_db(test_university_data):
    return {university_name: University.get_single(university_name=university_name, language="en") for university_name in test_university_data}

test_university_data = {
    "National Technical Training Institute": {
        "courses": [
            "Architecture", "Information Technology", "Civil Engineering", "Electrical Engineering", "Electronic Engineering"
        ],

        "admission": [
            "Bachelor Degree:BAC II Certificate, or High Diploma of Technical or Specialty"
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
            "Student ranked 1st : 50% scholarship",
            "Student ranked 2nd : 30% scholarship",
            "Student ranked 3rd : 20% scholarship",
            "Student ranked 4th and 5th : 10% scholarship"
        ],
        "contact_details": [
            "www.ntti.edu.kh",
            "info@ntti.edu.kh",
            "023 883 039"
        ],
        "facilities": ["Librarrry"]
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
                "period": "",
                "include_in_filter": False
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
    "Prek Leap National College of Agriculture": {
        "courses": [
            "Agribusiness/Economics",
            "Agricultural Economics",
            "Agricultural Extension & Rural Development",
            "Agricultural Management",
            "Agronomy Science",
            "Animal Health & Production",
            "Animal Sciences & Veterinary Medicine",
            "Aquatic Resource Management & Aquaculture",
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

test_category_data = {
    "Accounting": {
        "courses": [
            "Accounting", "Banking and Finance", "Finance and Banking"
        ],
        "intro": "Accountants usually interpret and report the financial information about a business. With experience they can provide financial advice to management teams.",
        "careers": "accounting technician, accountant, company secretary, actuary, economist, conveyance, consultant, purchasing manager, retail banker, tax adviser"
    },

    "Agriculture": {
        "courses": [ "Agribusiness/Economics", "Agricultural Economics", "Agricultural Extension & Rural Development",
            "Agricultural Management", "Agronomy Science", "Animal Health & Production", "Animal Sciences & Veterinary Medicine",
            "Aquatic Resource Management & Aquaculture", "Fisheries", "Food Processing", "Food Technology", "Forestry",
            "Horticulture"
        ],
        "intro": "Agriculture is a science focusing on producing goods through forestry as well as farming. It involves Biology, Chemistry and Environmental Studies, alongside aspects of Food Science, Technology, Economics and Management.",
        "careers":"Farm Management, Research or Advisory, Selling or Marketing agricultural goods or Technology."
    },

    "Architecture": {
        "courses": [
            "Architecture", "Architecture and Interior Design"
        ],
        "intro": "Architecture is the art and science of designing buildings and other physical structures.",
        "careers": "architect, architectural technologist, interior and spatial designer, building surveyor, higher education lecturer, structural engineer, town planner, production designer (theatre/television/film), historic buildings inspector"
    },

    "Art and Design": {
        "courses": [
            "Architecture and Interior Design", "Interior Design", "Graphic Design", "Product Design"
        ],
        "intro": "A degree in design prepares students to apply artistic principles and techniques in their area of specialization.",
        "careers": "animator, ceramics designer, creative copywriter, fashion designer, fine artist, furniture designer / restorer, glass blower, graphic designer, illustrator, industrial / product designer, interior designer, jewellery designer, make-up artist, museum / gallery conservator, photographer, production designer (theatre, TV, film), tattoo artist, textile designer"
    },

    "Biology": {
        "courses": [
            "Biology"
        ],
        "intro": "A major in biology provides students with a broad base for understanding principles governing life processes at all levels–molecular, cellular and ecological.",
        "careers": "Applied Biology, (Environmental) Research, or Teaching."
    },


    "Chemistry": {
        "courses": [
            "Chemistry"
        ],
        "intro": "Chemistry can be defined as the study of matter – what it’s composed of and its structure, its properties, and how it reacts and changes when exposed to different situations",
        "careers": "Research and Development in Manufacturing Firms. Jobs are also available in the Chemical, Pharmaceutical and Food Industries."
    },


    "Business": {
        "courses": [
            "Banking and Finance", "Business Administration", "International Business", "Business Statistics and Forecasting"
        ],
        "intro": "A business administration degree focuses on business management and prepares you to work in the world of commerce.",
        "careers": "production, sales, accounting, marketing"
    },

    "Computing": {
        "courses": [
            "Business Information System", "Computer Engineering", "Computer Science", "Information Technology"
        ],
        "intro": "Study computing problems and solutions, and the design of computer systems from a scientific perspective.",
        "careers": "database administrator, games developer, information systems manager, IT consultant, multimedia programmer, systems analyst / developer, web designer / developer"
    },

    "Economics": {
        "courses": [
            "Agricultural Economics", "Development Economics", "Economics", "Finance and Banking"
        ],
        "intro": "Economics educates students on how the economy works and what issues and trends it faces, using parts of Mathematics and Technology.",
        "careers": "accountant, economist, financial risk / investment analyst, statistician"
    },

    "Education": {
        "courses": [
            "Early Childhood Education", "Education and Languages", "Teaching English as a Foreign Language",
            "Teaching English to Speakers of Other Languages(TESOL)"
        ],
        "intro": "Helping others through teaching, at any level, can be a very rewarding career choice. A degree in education can prepare students to teach at various levels depending on your preferences.",
        "careers": "community education officer, teacher, education administrator, teaching assistant, youth worker"
    },

    "Engineering": {
        "courses": [
            "Electrical Engineering", "Electronic Engineering", "Civil Engineering", "Computer Engineering",
            "Electronics and Electricity", "Software Engineering"
        ],
       "intro": "Apply scientific, economic and social knowledge to designing and building structures, machines and processes. Within the engineering profession, there are thousands of challenging activities in areas such as research, development, design, manufacture and operation of products and services.",
       "careers": "logistics, engineer, patent lawyer, technical consultant"
    },

    "Geography": {
        "courses": [
            "Geography"
        ],
        "intro": "The study of the physical features of the earth and its atmosphere, and of human activity as it affects and is affected by these, including the distribution of populations and resources and political and economic activities.",
        "careers": "urban planning, community development, writer/researcher"
    },

    "History": {
        "courses": [
            "History", "Archaeology"
        ],
    "intro": "A degree in history focuses on the interpretation of the past, criticizing evidence and theories about events.",
    "careers": "teaching, law, social work, business administration"
    },

    "Humanities": {
        "courses": [
            "Anthropology", "Archaeology", "Asian Studies", "Khmer Studies", "Southeast Asian Studies"
        ],
        "intro": "Humanities focus on the cultures of various peoples from different periods of time and locations.",
        "careers": "teacher, advertising sales agent, technical writer, artist, counselor, event organizer, public relations manager, travel agent, lawyer, editor, museum worker / curator, interpreter, translator, genealogist, journalist, foreign correspondent, linguist, human resources specialist"
    },

    "Languages": {
        "courses": [
            "Asian Studies", "Chinese", "Chinese Language", "Chinese for Business", "English", "English for Business",
            "English for Communication", "Japanese Language", "Khmer Studies", "Southeast Asian Studies",
            "English for Translation and Interpretation", "English Business Communication"
        ],
        "intro": "The economy is becoming increasingly international and more and more companies need employees who can communicate effectively with colleagues and organizations across the world.",
        "careers": "translator, interpreter, teacher, foreign civil service, advertising, editing and publishing, subtitles and voice-overs"
    },

    "Law": {
        "courses": [
            "Law", "ASEAN Law", "Legal Studies"
        ],
        "intro": "Within the field of law, there are many different areas of specialization such as business law, public law, private law, criminal law and corporate law.",
        "careers": "lawyer, judge, professional counselor, mediator, politician, banker, entrepreneur, public interest advocate, journalist"
    },

    "Management": {
        "courses": [
            "Hospitality Management", "Hotel and Hospitality Management","Hotel and Tourism Management", "Management",
            "Tourism Management", "Media Management"
        ],
        "intro": "Examines policies and practices in the context of organizations, management theory, leadership, communication, employment relations and organizational behavior.",
        "careers": "manager, business / financial analyst, accountant, sales representative"
    },

    "Marketing": {
        "courses": [
            "Marketing"
        ],
        "intro": "Involves researching and satisfying customer needs, through product and service development, planning, pricing, advertising, promotion and distribution.",
        "careers": "Sales assistant, market researcher, advertising"
    },

    "Mathematics": {
        "courses": [
            "Mathematics"
        ],
        "intro": "A degree in mathematics provides you with a broad range of skills in problem solving, logical reasoning and flexible thinking.",
        "careers": "teacher, actuary, operational researcher, statistician"
    },

    "Media": {
        "courses": [
            "Journalism", "Communications"
        ],
        "intro": "Develop and create media and services for communications, advertising, and marketing purposes.",
        "careers": "media planner, multimedia specialist, researcher, public relations officer, television / film / video producer"
    },

    "Music": {
        "courses": [
            "Ethnomusicology",
            "Music"
        ],
        "intro": "Develops musical abilities and students also learn the history, style and practices of musicians and composers.",
        "careers": "music therapist, musician, teacher, sound technician"
    },

    "Other Sciences": {
        "courses": [
            "Environmental Science", "Environmental Policy and Planning"
        ],
        "intro": "These degrees are branches or mixtures of the three core sciences specializing in a range of areas.",
        "careers": "scientist, environmental researcher / planner"
    },

    "Politics": {
        "courses": [
            "Political Science"
        ],
        "intro": "Politics studies people’s values, what governments do, and the effect of all on our lives. It focuses on issues such as democracy, power, freedom, political economy, social movements, international law and conflict.",
        "careers": "politician, charity officer, diplomatic services operational officer, human resources officer, market researcher, newspaper journalist"
    },

    "Public Sector": {
        "courses": [
        "Public Administration"
        ],
        "intro": "Teaches students to serve as managers in the local and state departments of the government.",
        "careers": "Government / non-government organizations"
    },

    "Religion and Philosophy": {
        "courses": [
            "Religion", "Philosophy"
        ],
        "intro": "A degree in religion teaches students of the beliefs and practices of the world’s religions. A degree in philosophy develops intellectual thinking through solving complex and abstract questions.",
        "careers": "lawyer, teacher, accountant, social worker, banker, entrepreneur"
    },

    "Social Sciences": {
        "courses": [
            "International Relations", "Psychology", "Sociology",
        ],
        "intro": "Social science is the scientific study of human society and social relationships.",
        "careers": "teacher, social worker, psychologist, manager, anthropologist"
    },

    "Tourism": {
        "courses": [
           "Hotel and Tourism Management", "Tourism and Guide"
        ],
        "intro": "This degree prepares students to manage travel-related business and related tour services such as travel agency management, tour arranging and planning, tourism marketing, and tourism policy.",
        "careers": "holiday representative, tour manager, tourism officer, travel agency manager"
    }
}

users = [
    ["admin", "Administrator", "admin123", True, "en"],
    ["normal", "Normal User", "normal123", False, "en"]
]

pending_additions = {
    "course": ["Weird Spanish", "Zombish"],
    "category": [
        ["Inhumanities", "Using the humanities for mischief and profit", "Investment Banker, Homeopath"],
        ["Forbidden Medicine", "REDACTED", "Unemployed Surgeon", "Archaeology"]
    ],
    "university": [
        {
            "name": "Limkokwing University of Creative Technology",
            "admissions": [
                "Senior High School Certificate/ Diploma or equivalent",
                ("Foundation Year Certificate from University or another recognized institution. "
                "Foundation years can be completed at the University, contact the University directly for more information."),
                "Certificate of English Proficiency from a recognized institution or pass entrance examination."
            ],
            "contact_details": [
                "www.limkokwing.edu.kh"
                "023 995 733",
                "No. 120-126, Street 1986"
            ],
            "tuition_fees": [
                {
                    "min": 1500,
                    "max": 1500,
                    "currency": "$",
                    "award": "Foundation",
                    "period": "year"
                },
                {
                    "min": 1500,
                    "max": 2000,
                    "currency": "$",
                    "award": "Bachelor Degree",
                    "period": "year"
                },
                {
                    "min": 90,
                    "max": 90,
                    "currency": "$",
                    "award": "Application Fee",
                    "period": ""
                }
            ],
            "scholarships": [
                "Contact the University for more information"
            ],
            "courses": [
                "Accounting", "Architecture", "Product Design", "Information Technology"
            ],
            "facilities": ["Library", "Multimedia Labs"]
        }
    ]
}

pending_edits = {
    "course": [["Information Technology", "Information and Communication Technology"]],
    "category": [["Mathematics", "A degree in mathematics provides you with a broad range of skills in problem solving, logical reasoning and flexible thinking.", "teacher, actuary, operational researcher, statistician, professional nerd"]],
    "university": {
        "National Technical Training Institute": {
            "translations": {
                "en": {
                    "university_name": "New National Technical Training Institute",
                    "university_intro": "This is the New National Technical Training Institute"
                },
                "km": {
                    "university_name": khmer("New National Technical Training Institute"),
                    "university_intro": khmer("This is the New National Technical Training Institute")
                }
            },

            "new_courses": ["Software Engineering"],
            "deleted_courses": ["Architecture", "Information Technology"],

            "deleted_facilities": [
                "Librarrry"
            ],

            "new_facilities": [
                {"en": {"facility_string": "Library"}, "km": {"facility_string": khmer("Library")}}
            ],
            "deleted_facilities": [0],

            "new_contact_details": [
                {
                    "en": {"contact_detail_string": "Russian Blvd, Sangkat Teukthla Khan Sensok"},
                    "km": {"contact_detail_string": khmer("Russian Blvd, Sangkat Teukthla Khan Sensok")}
                }
            ],

            "deleted_contact_details": [0],

            "new_admissions": [
                {
                    "en": {"admission_string": "Bachelor Degree:BAC II Certificate, or High Diploma of Technical or Specialty, or Associate Degree."},
                    "km": {"admission_string": khmer("Bachelor Degree:BAC II Certificate, or High Diploma of Technical or Specialty, or Associate Degree.")}
                }
            ],

            "deleted_admissions": [0],

            "new_tuition_fees": [
                {
                    "en": {
                        "tuition_fee_min": 999,
                        "tuition_fee_max": 999, 
                        "currency": "$",
                        "period": "year",
                        "award": "Nobel Prize"
                    },
                    "km": {
                        "tuition_fee_min": int(float(999)/ 0.00025),
                        "tuition_fee_max": int(float(999)/ 0.00025), 
                        "currency": "៛",
                        "period": khmer("year"),
                        "award": khmer("Nobel Prize")
                    }
                }
            ],

            "deleted_tuition_fees": [0],

            "new_scholarships": [
                {
                    "en": {"scholarship_string": "100% Scholarship to anyone with more than seven legs."},
                    "km": {"scholarship_string": khmer("100% Scholarship to anyone with more than seven legs.")},
                }
            ],

            "deleted_scholarships": [0]
        }
    }
}

pending_deletions = {
    "category": ["Computing"],
    "course": ["Graphic Design"]
}

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    ## Build courses list from category data
    test_course_data = []
    for _, category_data in test_category_data.items():
        test_course_data.extend(category_data["courses"])

    test_course_data = set(test_course_data)

    courses = {}
    categories = {}
    universities = {}

    if args["create_baseline"]:


        print("Creating application context...", end=""); sys.stdout.flush()
        with app.app_context():
            print("done.")
            
            print("Creating empty database {}...".format(app.config["SQLALCHEMY_DATABASE_URI"]), end=""); sys.stdout.flush()
            DeclarativeBase.metadata.drop_all(bind=db.engine)
            DeclarativeBase.metadata.create_all(bind=db.engine)
            print("done.")
            
            print("Creating courses...", end=""); sys.stdout.flush()
            
            for course in test_course_data:
                courses[course] = Course.create(course, "en")
                courses[course].set_name(khmer(course), "km")

            print("done.")

            print("Creating categories...", end=""); sys.stdout.flush()
            
            for category_name, category_data in test_category_data.items():
                new_category = Category.create(category_name, "en")
                categories[category_name] = new_category

                new_category.set_name(khmer(category_name), "km")
                new_category.set_intro(category_data["intro"], "en")
                new_category.set_intro(khmer(category_data["intro"]), "km")

                new_category.set_careers(category_data["careers"], "en")
                new_category.set_careers(khmer(category_data["careers"]), "km")

                for course in category_data["courses"]:
                    categories[category_name].add_course(courses[course])

            print("done.")

            # Create universities and link to courses
            print("Creating universities...")
            
            for university in test_university_data:
                universities[university] = University.create({
                        "en": {
                            "university_name": university,
                            "university_intro": "This is the " + university
                        },
                        "km": {
                            "university_name": khmer(university),
                            "university_intro": khmer("This is the " + university)
                        }
                    }
                )


            for university, uni_data in test_university_data.items():

                print(university + "...")
                for course in uni_data["courses"]:
                    universities[university].add_course(courses[course])

                for admission in uni_data["admission"]:
                    adm = Admission.create(universities[university].university_id, {
                            "en": {"admission_string": admission},
                            "km": {"admission_string": khmer(admission)}
                        }
                    )

                for tuition_fee in uni_data["tuition_fees"]:
                    fee = TuitionFee.create(
                        universities[university].university_id, 
                        tuition_fee.get("include_in_filter", True),
                            {
                            "en": {
                                "tuition_fee_min": tuition_fee["min"],
                                "tuition_fee_max": tuition_fee["max"], 
                                "currency": tuition_fee["currency"],
                                "period": tuition_fee["period"],
                                "award": tuition_fee["award"],
                            },
                            "km": {                            
                                "tuition_fee_min": int(float(tuition_fee["min"])/ 0.00025),
                                "tuition_fee_max": int(float(tuition_fee["max"])/ 0.00025), 
                                "currency": "៛",
                                "period": khmer(tuition_fee["period"]),
                                "award": khmer(tuition_fee["award"])
                            }
                        }
                    )

                for scholarship in uni_data["scholarships"]:
                    sch = Scholarship.create(universities[university].university_id, {
                        "en": {"scholarship_string": scholarship},
                        "km": {"scholarship_string": khmer(scholarship)}
                    })

                for contact_detail in uni_data["contact_details"]:
                    det = ContactDetail.create(universities[university].university_id, {
                        "en": {"contact_detail_string": contact_detail},
                        "km": {"contact_detail_string": khmer(contact_detail)}
                    })

                for facility in uni_data["facilities"]:
                    fac = Facility.create(universities[university].university_id, {
                            "en": {"facility_string": facility},
                            "km": {"facility_string": khmer(facility)}
                        }
                    )

            print("Creating users")

            for user in users:
                user = User.create(*user)

            shutil.copy("app/debug.db", "app/debug.original.db")
            print("Finished creating test data")

    if args["create_pending"]:

        print("Creating application context...", end=""); sys.stdout.flush()
        with app.app_context():
            print("Done")

            drop_all_pending_tables()

            courses = load_courses_from_db(test_course_data)
            categories = load_categories_from_db(test_category_data.keys())
            universities = load_universities_from_db(test_university_data.keys())

            print("Adding pending additions")

            for addition in pending_additions["category"]:
                print("Addition of '{}' category".format(addition[0]))
                category = CategoryPending.addition(category_name=addition[0], language="en")
                category.set_name(khmer(addition[0]), "km")
                category.set_intro(addition[1], "en")
                category.set_intro(khmer(addition[1]), "km")
                category.set_careers(addition[2], "en")
                category.set_careers(khmer(addition[2]), "km")
                if len(addition) == 4:
                    category.add_course(courses[addition[3]])

            for addition in pending_additions["course"]:
                print("Addition of '{}' course".format(addition))
                course = CoursePending.addition(course_name=addition, language="en")

            for addition in pending_additions["university"]:
                print("Addition of '{}' university".format(addition["name"]))
                university = UniversityPending.addition({
                    "en": {
                        "university_name": addition["name"],
                        "university_intro": "This is the " + addition["name"]
                    },
                    "km": {
                        "university_name": khmer(addition["name"]),
                        "university_intro": "This is the " + khmer(addition["name"])
                    },
                })

                for course in addition["courses"]:
                    university.add_course(courses[course])

                for tuition_fee in addition["tuition_fees"]:
                    TuitionFeePending.addition(university.pending_id, {
                        "en": {
                            "tuition_fee_min": tuition_fee["min"],
                            "tuition_fee_max": tuition_fee["max"], 
                            "currency": tuition_fee["currency"],
                            "period": tuition_fee["period"],
                            "award": tuition_fee["award"]
                        },
                        "km": {
                            "tuition_fee_min": int(float(tuition_fee["min"])/ 0.00025),
                            "tuition_fee_max": int(float(tuition_fee["max"])/ 0.00025),
                            "currency": "៛",
                            "period": khmer(tuition_fee["period"]),
                            "award": khmer(tuition_fee["award"])
                        }
                    })


                for admission in addition["admissions"]:
                    AdmissionPending.addition(university.pending_id, {
                        "en": {"admission_string": admission},
                        "km": {"admission_string": khmer(admission)}
                    })

                for contact_detail in addition["contact_details"]:
                    ContactDetailPending.addition(university.pending_id, {
                        "en": {"contact_detail_string": contact_detail},
                        "km": {"contact_detail_string": khmer(contact_detail)}
                    })

                for scholarship in addition["scholarships"]:
                    ScholarshipPending.addition(university.pending_id, {
                        "en": {"scholarship_string": scholarship},
                        "km": {"scholarship_string": khmer(scholarship)}
                    })

                for facility in addition["facilities"]:
                    FacilityPending.addition(university.pending_id, {
                        "en": {
                                "facility_string": facility,
                            }
                        }
                    )

            print("Adding pending edits")

            for edit in pending_edits["category"]:
                print("Edit of '{}'".format(edit[0]))
                category = CategoryPending.edit(categories[edit[0]])
                category.set_intro(edit[1], "en")
                category.set_careers(edit[2], "en")

            for edit in pending_edits["course"]:
                print("Edit of '{}'".format(edit[0]))
                course = CoursePending.edit(courses[edit[0]])
                course.set_name(edit[1], "en")

            for name, edits in pending_edits["university"].items():
                print("Edit of '{}'".format(name))
                pending_uni = UniversityPending.edit(universities[name])
                pending_uni.set_translations(edits["translations"])

                for new_course in edits["new_courses"]:
                    pending_uni.add_course(courses[new_course])

                for deleted_course in edits["deleted_courses"]:
                    pending_uni.remove_course(courses[new_course])

                for new_contact_detail in edits["new_contact_details"]:
                    ContactDetailPending.addition(pending_uni.pending_id, new_contact_detail)

                for deleted_contact_detail_idx in edits["deleted_contact_details"]:
                    contact_detail = universities[name].contact_details[deleted_contact_detail_idx]
                    ContactDetailPending.deletion(contact_detail)

                for admission in edits["new_admissions"]:
                    AdmissionPending.addition(pending_uni.pending_id, admission)

                for admission_idx in edits["deleted_admissions"]:
                    admission = universities[name].admissions[admission_idx]
                    AdmissionPending.deletion(admission)

                for tuition_fee in edits["new_tuition_fees"]:
                    TuitionFeePending.addition(pending_uni.pending_id, tuition_fee)

                for tuition_fee_idx in edits["deleted_tuition_fees"]:
                    tuition_fee = universities[name].tuition_fees[tuition_fee_idx]
                    TuitionFeePending.deletion(tuition_fee)

                for scholarship in edits["new_scholarships"]:
                    ScholarshipPending.addition(pending_uni.pending_id, scholarship)

                for scholarship_idx in edits["deleted_scholarships"]:
                    scholarship = universities[name].scholarships[scholarship_idx]
                    ScholarshipPending.deletion(scholarship)

                for facility in edits["new_facilities"]:
                    FacilityPending.addition(pending_uni.pending_id, facility)

                for facility_idx in edits["deleted_facilities"]:
                    facility = universities[name].facilities[facility_idx]
                    FacilityPending.deletion(facility)

            print("Adding pending deletions")

            for deletion in pending_deletions["category"]:
                print("Deletion of '{}'".format(deletion))
                category = CategoryPending.deletion(categories[deletion])

            for deletion in pending_deletions["course"]:
                course = CoursePending.deletion(courses[deletion])

    elif args["copy"]:
        shutil.copy("app/debug.original.db", "app/debug.db")

    elif args["make_original"]:
        shutil.copy("app/debug.db", "app/debug.original.db")
