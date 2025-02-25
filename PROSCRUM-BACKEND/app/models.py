from pydantic import BaseModel

class HoleConfig(BaseModel):
    hole: int
    par: int | None = 0
    hdc: int | None = 0

class CourseBase(BaseModel):
    course_name: str
    course_par: int
    course_rating_9: float | None 
    course_rating_18: float | None 
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