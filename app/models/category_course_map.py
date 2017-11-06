import sqlalchemy as sa
from app.models.base_model import DeclarativeBase

category_course_map_table = sa.Table('CategoryCourseMap', DeclarativeBase.metadata,
    sa.Column('category_id', sa.Integer, sa.ForeignKey('Category.category_id')),
    sa.Column('course_id', sa.Integer, sa.ForeignKey('Course.course_id'))
)

category_course_pending_map_table = sa.Table('CategoryCoursePendingMap', DeclarativeBase.metadata,
    sa.Column('category_id', sa.Integer, sa.ForeignKey('CategoryPending.category_id')),
    sa.Column('course_id', sa.Integer, sa.ForeignKey('CoursePending.course_id'))
)
