from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

class Roles(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, nullable=False)
    role = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False)

class Course(Base):
    __tablename__= "courses"

    course_id = Column(Integer, primary_key=True, nullable=False)
    course_name = Column(String, nullable=False)
    course_par_1_to_9 = Column(Integer, nullable=True)
    course_par_10_to_18 = Column(Integer, nullable=True)
    course_par_all = Column(Integer, nullable=True)
    slope_rating = Column(Integer, nullable=False)
    course_rating_1_to_9 = Column(Float(precision=2), nullable=True)
    course_rating_10_to_18 = Column(Float(precision=2), nullable=True)
    course_rating_all = Column(Float(precision=2), nullable=True)

class Hole(Base):
    __tablename__= "holes"

    hole_id = Column(Integer, primary_key=True, nullable=False)
    hole = Column(Integer, nullable=False)
    hdc = Column(Integer, nullable=False)
    par = Column(Integer, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)

class Score(Base):
    __tablename__ = "scores"

    score_id = Column(Integer, primary_key=True, nullable=False)
    hole_1_strokes = Column(Integer, nullable=True)
    hole_2_strokes = Column(Integer, nullable=True)
    hole_3_strokes = Column(Integer, nullable=True)
    hole_4_strokes = Column(Integer, nullable=True)
    hole_5_strokes = Column(Integer, nullable=True)
    hole_6_strokes = Column(Integer, nullable=True)
    hole_7_strokes = Column(Integer, nullable=True)
    hole_8_strokes = Column(Integer, nullable=True)
    hole_9_strokes = Column(Integer, nullable=True)
    hole_10_strokes = Column(Integer, nullable=True)
    hole_11_strokes = Column(Integer, nullable=True)
    hole_12_strokes = Column(Integer, nullable=True)
    hole_13_strokes = Column(Integer, nullable=True)
    hole_14_strokes = Column(Integer, nullable=True)
    hole_15_strokes = Column(Integer, nullable=True)
    hole_16_strokes = Column(Integer, nullable=True)
    hole_17_strokes = Column(Integer, nullable=True)
    hole_18_strokes = Column(Integer, nullable=True)

class Round(Base):
    __tablename__ = "rounds"

    round_id = Column(Integer, primary_key=True, nullable=False)
    round_number = Column(Integer, nullable=False)
    hdc_2020 = Column(Float(precision=2), nullable=False)
    hdc_2021 = Column(Float(precision=2), nullable=False)
    score_differential = Column(Float(precision=2), nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    score_id = Column(Integer, ForeignKey("scores.score_id", ondelete="CASCADE"), nullable=False)

    user = relationship("User")

class Course_Leader_Secretary(Base):
    __tablename__ = "courses_leaders_secretaries"

    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True, nullable=False)