import sqlalchemy as sa
from app.models.base_model import DeclarativeBase

university_course_map_table = sa.Table('UniversityCourseMap', DeclarativeBase.metadata,
    sa.Column('university_id', sa.Integer, sa.ForeignKey('University.university_id')),
    sa.Column('course_id', sa.Integer, sa.ForeignKey('Course.course_id'))
)