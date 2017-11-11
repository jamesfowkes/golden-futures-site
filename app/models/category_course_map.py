import sqlalchemy as sa
from app.models.base_model import DeclarativeBase

category_course_map_table = sa.Table('CategoryCourseMap', DeclarativeBase.metadata,
    sa.Column('category_id', sa.Integer, sa.ForeignKey('Category.category_id')),
    sa.Column('course_id', sa.Integer, sa.ForeignKey('Course.course_id'))
)
