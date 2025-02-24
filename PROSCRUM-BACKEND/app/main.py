from fastapi import FastAPI, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models import CourseCreate, CourseWithID
from app.mockups import generate_mockups

from random import randrange

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Mock data:
courses_list = generate_mockups()

# Generate random scores for POST Method test
rand_scores = []
for i in range(18):
    score = randrange(1, 13)
    rand_scores.append(score)
print(rand_scores)

# For first tests without DB
course_ratings = []
course_pars = []
course_scores = []
slope_ratings = []

# Utility:

def find_course(id: int):
    for course in courses_list:
        if course.course_id == id:
            return course

def find_index_course(id):
    for i, c in enumerate(courses_list):
        print(f"i: {i}, c: {c}")
        if c.course_id == id:
            return i

"""-----ENDPOINTS-----"""

@app.get("/")
def home():
    return {"message": "Hello Golf!"}


@app.get("/courses")
def get_courses():
    return {"result": courses_list}

@app.get("/courses/{id}")
def get_one_course(id: int):
    course = find_course(id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} was not found")
    return {"result": course}

@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    print(course)
    new_course = CourseWithID(
        course_name=course.course_name,
        course_par=course.course_par,
        course_rating_9=course.course_rating_9,
        course_rating_18=course.course_rating_18,
        slope_rating=course.slope_rating,
        holes=course.holes,
        course_id= len(courses_list) + 1
    )
    courses_list.append(new_course)
    
    return {"result": new_course}

@app.put("/courses/{id}")
def update_course(id: int, course: CourseWithID):
    updated_course = find_course(id)

    if not updated_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} was not found")
    
    updated_course.course_name = course.course_name
    updated_course.course_par = course.course_par
    updated_course.course_rating = course.course_rating
    updated_course.slope_rating = course.slope_rating
    updated_course.holes = course.holes

    return {"result": updated_course}

@app.delete("/courses/{id}")
def delete_course(id: int):
    course_index = find_index_course(id)
    print(course_index)
    if course_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} does not exist.")

    courses_list.pop(course_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)