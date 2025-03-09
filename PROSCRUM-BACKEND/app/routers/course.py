from fastapi import Response, status, HTTPException, APIRouter

from ..models import CourseCreate, CourseWithID
from ..utils import find_course, find_index_course
from ..mockups import courses_list

router = APIRouter(
    prefix="/courses",
    tags=['Courses']
)

@router.get("/courses")
def get_courses():
    return {"result": courses_list}

@router.get("/courses/{id}")
def get_one_course(id: int):
    course = find_course(id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} was not found")
    return {"result": course}

@router.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    print(course)
    new_course = CourseWithID(
        course_name=course.course_name,
        course_par_1_to_9=course.course_par_1_to_9,
        course_par_10_to_18=course.course_par_10_to_18,
        course_par_all=course.course_par_all,
        course_rating_1_to_9=course.course_rating_1_to_9,
        course_rating_10_to_18=course.course_rating_10_to_18,
        course_rating_all=course.course_rating_all,
        slope_rating=course.slope_rating,
        holes=course.holes,
        course_id= courses_list[-1].course_id + 1
    )
    courses_list.append(new_course)
    
    return {"result": new_course}

@router.put("/courses/{id}")
def update_course(id: int, course: CourseWithID):
    updated_course = find_course(id)

    if not updated_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} was not found")
    
    updated_course = CourseWithID(**course.model_dump())
    courses_list[id-1] = updated_course

    return {"result": updated_course}

@router.delete("/courses/{id}")
def delete_course(id: int):
    course_index = find_index_course(id)
    print(course_index)
    if course_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} does not exist.")

    courses_list.pop(course_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)