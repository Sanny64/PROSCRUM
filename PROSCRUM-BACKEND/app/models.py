from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

class HoleConfig(BaseModel):
    hole: int
    par: int
    hdc: int
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
    course_par_1_to_9: int | None
    course_par_10_to_18: int | None
    course_par_all: int | None
    course_rating_1_to_9: float | None 
    course_rating_10_to_18: float | None 
    course_rating_all: float | None 
    slope_rating: int
    holes: list[HoleConfig]
    leaders_secretaries: list[int] | None

class CourseCreate(CourseBase):
    pass

class CourseWithID(CourseBase):
    course_id: int

class UserBase(BaseModel):
    first_name: str
    last_name : str

class UserCreate(UserBase):
    email: EmailStr
    password: str
    role_id: int

class UserOut(UserBase):
    user_id: int
    email: EmailStr
    role_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    email: EmailStr
    role_id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RoundBase(BaseModel):
    round_number: int
    course: CourseWithID 
    scores: list[int]
    date: date

class RoundIn(RoundBase):
    pass

class RoundOut(RoundBase):
    round_id: int
    user_id: int
    calc_result_2020: float
    calc_result_2021: float
    score_differential: float
    user: UserOut

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]
    role_id: Optional[int]