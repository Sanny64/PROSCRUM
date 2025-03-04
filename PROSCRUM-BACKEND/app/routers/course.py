from fastapi import Response, status, HTTPException, APIRouter

from ..models import CourseCreate, CourseWithID
from ..utils import find_course, find_index_course
from ..mockups import courses_list

router = APIRouter(
    prefix="/courses",
    tags=['Courses']
)

@router.get("/")
def get_courses():
    return {"result": courses_list}

@router.get("/{id}")
def get_one_course(id: int):
    course = find_course(id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} was not found")
    return {"result": course}

@router.post("/", status_code=status.HTTP_201_CREATED)
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

@router.put("/{id}")
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

@router.delete("/{id}")
def delete_course(id: int):
    course_index = find_index_course(id)
    print(course_index)
    if course_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} does not exist.")

    courses_list.pop(course_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)