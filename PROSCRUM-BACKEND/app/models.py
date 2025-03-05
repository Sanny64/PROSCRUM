from pydantic import BaseModel
from datetime import date

class HoleConfig(BaseModel):
    hole: int
    par: int
    hdc: int

class CourseBase(BaseModel):
    course_name: str
    course_par_1_to_9: int | None
    course_par_10_to_18: int | None
    course_par_all: int | None
    course_rating_1_to_9: float | None 
    course_rating_10_to_18: float | None 
    course_rating_all: float | None 
    slope_rating: int
    holes: list[HoleConfig]

class CourseCreate(CourseBase):
    pass

class CourseWithID(CourseBase):
    course_id: int

class RoundBase(BaseModel):
    # user_id: int
    round_number: int
    course: CourseWithID 
    scores: list[int]

class RoundIn(RoundBase):
    pass

class RoundOut(RoundBase):
    calc_result_2020: float
    calc_result_2021: float
    score_differential: float