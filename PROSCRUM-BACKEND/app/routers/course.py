from fastapi import Response, status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..models import CourseCreate, CourseWithID, HoleConfig
from ..database import get_db
from .. import schemas, oauth2

router = APIRouter(
    prefix="/courses",
    tags=['Courses']
)

@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(schemas.Course).all()
    return_courses_list = []
    for course in courses:
        holes = db.query(schemas.Hole).filter(schemas.Hole.course_id == course.course_id).all()
        hole_config_list = []
        for hole in holes:
            hole_config = HoleConfig(hole=hole.hole, par=hole.par, hdc=hole.hdc)
            hole_config_list.append(hole_config)

        leaders = db.query(schemas.Course_Leader_Secretary).filter(schemas.Course_Leader_Secretary.course_id == course.course_id).all()
        leaders_secretaries = [user_id.user_id for user_id in leaders]

        course_with_id = CourseWithID(
            course_id=course.course_id,
            course_name=course.course_name,
            course_par_1_to_9=course.course_par_1_to_9,
            course_par_10_to_18=course.course_par_10_to_18,
            course_par_all=course.course_par_all,
            course_rating_1_to_9=course.course_rating_1_to_9,
            course_rating_10_to_18=course.course_rating_10_to_18,
            course_rating_all=course.course_rating_all,
            slope_rating=course.slope_rating,
            holes=hole_config_list,
            leaders_secretaries=leaders_secretaries
        )
        return_courses_list.append(course_with_id)

    return {"result": return_courses_list}

@router.get("/{id}")
def get_one_course(id: int, db: Session = Depends(get_db)):
    course = db.query(schemas.Course).filter(schemas.Course.course_id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} was not found")
    
    holes = db.query(schemas.Hole).filter(schemas.Hole.course_id == course.course_id).all()
    hole_config_list = []
    for hole in holes:
        hole_config = HoleConfig(hole=hole.hole, par=hole.par, hdc=hole.hdc)
        hole_config_list.append(hole_config)

    leaders = db.query(schemas.Course_Leader_Secretary).filter(schemas.Course_Leader_Secretary.course_id == course.course_id).all()
    leaders_secretaries = [user_id.user_id for user_id in leaders]

    course_with_id = CourseWithID(
        course_id=course.course_id,
        course_name=course.course_name,
        course_par_1_to_9=course.course_par_1_to_9,
        course_par_10_to_18=course.course_par_10_to_18,
        course_par_all=course.course_par_all,
        course_rating_1_to_9=course.course_rating_1_to_9,
        course_rating_10_to_18=course.course_rating_10_to_18,
        course_rating_all=course.course_rating_all,
        slope_rating=course.slope_rating,
        holes=hole_config_list,
        leaders_secretaries=leaders_secretaries
    )

    return {"result": course_with_id}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")

    new_course = schemas.Course(
        course_name = course.course_name,
        course_par_1_to_9 = course.course_par_1_to_9,
        course_par_10_to_18 = course.course_par_10_to_18,
        course_par_all = course.course_par_all,
        course_rating_1_to_9 = course.course_rating_1_to_9,
        course_rating_10_to_18 = course.course_rating_10_to_18,
        course_rating_all = course.course_rating_all,
        slope_rating = course.slope_rating)
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    for hole in course.holes:
        new_hole = schemas.Hole(course_id=new_course.course_id, **hole.model_dump())
        db.add(new_hole)
        db.commit()
    
    db.refresh(new_course)

    for user in course.leaders_secretaries:
        user_db = db.query(schemas.User).filter(schemas.User.user_id == user).first()
        if user_db.role_id > 1:
            new_leaders_secretaries = schemas.Course_Leader_Secretary(
                course_id=new_course.course_id,
                user_id= user
            )
            db.add(new_leaders_secretaries)
            db.commit()

    db.refresh(new_course)
    return_course = CourseWithID(course_id=new_course.course_id, **course.model_dump())

    return {"result": return_course}

@router.put("/{id}")
def update_course(id: int, updated_course: CourseCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    
    course_query = db.query(schemas.Course).filter(schemas.Course.course_id == id)

    course = course_query.first()

    if course == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} was not found")
    
    update_dict = updated_course.model_dump()
    update_dict.pop("holes", None)
    update_dict.pop("leaders_secretaries", None)

    course_query.update(update_dict,
        synchronize_session=False)
    
    db.commit()

    hole_config_list = []
    hole_db_list = db.query(schemas.Hole).filter(schemas.Hole.course_id == id).all()
    for hole, hole_db in zip(updated_course.holes, hole_db_list):
        hole_query = db.query(schemas.Hole).filter(schemas.Hole.hole_id == hole_db.hole_id)
        hole_data = hole.model_dump()
        hole_data["hole_id"] = hole_db.hole_id
        hole_data["course_id"] = hole_db.course_id
        hole_query.update(hole_data, synchronize_session=False)
        db.commit()
        hole_config_list.append(hole)

    course = course_query.first()

    leaders_query = db.query(schemas.Course_Leader_Secretary).filter(schemas.Course_Leader_Secretary.course_id == course.course_id)
    leaders_query.delete(synchronize_session=False)
    db.commit()

    for user in updated_course.leaders_secretaries:
            user_db = db.query(schemas.User).filter(schemas.User.user_id == user).first()
            if user_db.role_id > 1:
                new_leaders_secretaries = schemas.Course_Leader_Secretary(
                    course_id=id,
                    user_id=user
                )
                db.add(new_leaders_secretaries)
                db.commit()

    return_course_with_id = CourseWithID(
        course_id=course.course_id,
        course_name=course.course_name,
        course_par_1_to_9=course.course_par_1_to_9,
        course_par_10_to_18=course.course_par_10_to_18,
        course_par_all=course.course_par_all,
        course_rating_1_to_9=course.course_rating_1_to_9,
        course_rating_10_to_18=course.course_rating_10_to_18,
        course_rating_all=course.course_rating_all,
        slope_rating=course.slope_rating,
        holes=hole_config_list,
        leaders_secretaries= updated_course.leaders_secretaries
    )

    return {"result": return_course_with_id}

@router.delete("/{id}")
def delete_course(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")

    course_query = db.query(schemas.Course).filter(schemas.Course.course_id == id)

    course = course_query.first()
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {id} does not exist.")

    course_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)