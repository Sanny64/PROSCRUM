from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..models import HoleConfig, CourseWithID
from ..calculations import get_hits_ahead
from ..new_calculations import calculate_CH

from ..database import get_db
from .. import schemas, oauth2, models


router = APIRouter(
    prefix="/scorecard",
    tags=['Scorecard']
)

@router.get("/", response_model=list[models.RoundOut])
def get_Scorecard(HDC: float, course_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id < 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    
    course = db.query(schemas.Course).filter(schemas.Course.course_id == course_id).first()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with course_id: {course_id} was not found")
    
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
        course_rating_10_to_18=course.course_par_10_to_18,
        course_rating_all=course.course_rating_all,
        slope_rating=course.slope_rating,
        holes=hole_config_list,
        leaders_secretaries=leaders_secretaries
    )

    course_HDC = calculate_CH(HDC, course.slope_rating, course.course_rating_all, course.course_par_all)
    hits_ahead = get_hits_ahead(course_with_id, course_HDC)
    
    return{
        "result": {
            "course_HDC": course_HDC,
            "hits_ahead": hits_ahead
        }
    }
