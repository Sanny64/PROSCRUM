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