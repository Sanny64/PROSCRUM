from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware

from app.models import CourseCreate, CourseWithID, RoundIn, RoundOut
from app.calculations import start_calculations
from app.mockups import generate_mockups, generate_courses

from random import randrange

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mock data:
courses_list = generate_courses()
my_rounds = generate_mockups()

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

def find_round(round_number: int):
    for round in my_rounds:
        if round.round_number == round_number:
            return round
        
def find_course(id: int):
    for course in courses_list:
        if course.course_id == id:
            return course
        
def find_index_round(round_number):
    for i, r in enumerate(my_rounds):
        print(f"i: {i}, r: {r}")
        if r.round_number == round_number:
            return i

def find_index_course(id):
    for i, c in enumerate(courses_list):
        print(f"i: {i}, c: {c}")
        if c.course_id == id:
            return i

"""-----ENDPOINTS-----"""

@app.get("/")
def home():
    return {"message": "Hello Golf!"}

# "/rounds" Endpoints:

@app.post("/rounds")
def create_round(round: RoundIn):
    print(round)

    calc_result = start_calculations(round, my_rounds)
    new_calc_result_2020 = calc_result[0]
    new_calc_result_2021 = calc_result[1]
    score_differential = calc_result[2]

    new_round = RoundOut(
        round_number=round.round_number, 
        course=round.course, scores=round.scores, 
        calc_result_2020=new_calc_result_2020, 
        calc_result_2021=new_calc_result_2021, 
        score_differential=score_differential
    )
    my_rounds.append(new_round)

    return Response(status_code=status.HTTP_201_CREATED)

@app.get("/rounds")
def get_rounds():   
    return {"result": my_rounds}

@app.get("/rounds/{round_number}")
def get_one_round(round_number: int):
    round = find_round(round_number)
    if not round:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} was not found")
    return {"result": round}

@app.put("/rounds/{round_number}")
def update_round(round_number: int, round: RoundOut):
    updated_round = find_round(round_number)

    if not updated_round:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} was not found")
    
    updated_round.course.course_name = round.course.course_name
 
    # TODO:
    # Neuberechnung noch buggy. Eventuell liegt es an der calculation implementierung. Im Team besprechen
    if (
    updated_round.course.course_par != round.course.course_par or 
    updated_round.course.course_rating_9 != round.course.course_rating_9 or
    updated_round.course.course_rating_18 != round.course.course_rating_18 or
    updated_round.course.slope_rating != round.course.slope_rating or
    updated_round.course.holes != round.course.holes or
    updated_round.scores != round.scores):
        updated_calc_results = start_calculations(round, my_rounds)
        new_updated_calc_result_2020 = updated_calc_results[0]
        new_updated_calc_result_2021 = updated_calc_results[1]
        updated_round.calc_result_2020 = new_updated_calc_result_2020
        updated_round.calc_result_2021 = new_updated_calc_result_2021
        updated_round.score_differential = updated_calc_results[2]
    else:
        updated_round.calc_result_2020 = round.calc_result_2020
        updated_round.calc_result_2021 = round.calc_result_2021
        updated_round.score_differential = round.score_differential
        
    updated_round.course.course_par = round.course.course_par
    updated_round.course.course_rating_9 = round.course.course_rating_9
    updated_round.course.course_rating_18 = round.course.course_rating_18
    updated_round.course.slope_rating = round.course.slope_rating
    updated_round.course.holes = round.course.holes
    updated_round.scores = round.scores

    return {"result": updated_round}

@app.delete("/rounds/{round_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_round(round_number: int):
    round_index = find_index_round(round_number)
    print(round_index)
    if round_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} does not exist.")

    my_rounds.pop(round_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# "/courses" Endpoints:

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
    updated_course.course_rating_9 = course.course_rating_9
    updated_course.course_rating_18 = course.course_rating_18
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