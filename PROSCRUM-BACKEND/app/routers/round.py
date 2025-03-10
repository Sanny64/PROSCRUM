from fastapi import Response, status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..utils import find_round, find_index_round
from ..models import RoundIn, RoundOut
from ..calculations import start_calculations
from ..mockups import my_rounds
from ..database import get_db
from .. import schemas, oauth2, models


router = APIRouter(
    prefix="/rounds",
    tags=['Rounds']
)

@router.post("/")
def create_round(round: RoundIn, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):

    user_rounds = db.query(schemas.Round).filter(schemas.Round.user_id == current_user.user_id).all()

    calc_rounds = []
    for user_round in user_rounds:
        round_course = db.query(schemas.Course).filter(schemas.Course.course_id == user_round.course_id).first()

        round_course_holes_db = db.query(schemas.Hole).filter(schemas.Hole.course_id == user_round.course_id).all()

        hole_config_list = []
        for hole in round_course_holes_db:
            hole_config = models.HoleConfig(hole=hole.hole, par=hole.par, hdc=hole.hdc)
            hole_config_list.append(hole_config)

        round_course_with_id = models.CourseWithID(
            course_id=round_course.course_id,
            course_name=round_course.course_name,
            course_par_1_to_9=round_course.course_par_1_to_9,
            course_par_10_to_18=round_course.course_par_10_to_18,
            course_par_all=round_course.course_par_all,
            course_rating_1_to_9=round_course.course_rating_1_to_9,
            course_rating_10_to_18=round_course.course_rating_10_to_18,
            course_rating_all=round_course.course_rating_all,
            slope_rating=round_course.slope_rating,
            holes=hole_config_list
        )

        scores = []
        round_scores_db = db.query(schemas.Score).filter(schemas.Score.score_id == user_round.score_id).first()
        for i in range(18):
            stroke = getattr(round_scores_db, 'hole_' + str(i+1) + '_strokes')
            scores.append(stroke)

        round_out = RoundOut(
            round_id=user_round.round_id,
            user_id=current_user.user_id,
            round_number=user_round.round_number,
            course=round_course_with_id,
            scores=scores,
            date=user_round.date,
            calc_result_2020=user_round.hdc_2020,
            calc_result_2021=user_round.hdc_2021,
            score_differential=user_round.score_differential
        )
        calc_rounds.append(round_out)
        print(round_out)

    print(calc_rounds)

    calc_result = start_calculations(round, calc_rounds)
    new_calc_result_2020 = calc_result[0]
    new_calc_result_2021 = calc_result[1]
    new_score_differential = calc_result[2]

    new_score = schemas.Score(
        hole_1_strokes=round.scores[0],
        hole_2_strokes=round.scores[1],
        hole_3_strokes=round.scores[2],
        hole_4_strokes=round.scores[3],
        hole_5_strokes=round.scores[4],
        hole_6_strokes=round.scores[5],
        hole_7_strokes=round.scores[6],
        hole_8_strokes=round.scores[7],
        hole_9_strokes=round.scores[8],
        hole_10_strokes=round.scores[9],
        hole_11_strokes=round.scores[10],
        hole_12_strokes=round.scores[11],
        hole_13_strokes=round.scores[12],
        hole_14_strokes=round.scores[13],
        hole_15_strokes=round.scores[14],
        hole_16_strokes=round.scores[15],
        hole_17_strokes=round.scores[16],
        hole_18_strokes=round.scores[17]
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    
    new_round = schemas.Round(
        round_number=round.round_number,
        hdc_2020=new_calc_result_2020,
        hdc_2021=new_calc_result_2021,
        score_differential=new_score_differential,
        date=round.date,
        user_id=current_user.user_id,
        course_id=round.course.course_id,
        score_id=new_score.score_id   
    )

    db.add(new_round)
    db.commit()
    db.refresh(new_round)

    return Response(status_code=status.HTTP_201_CREATED)

@router.get("/")
def get_rounds():   
    return {"result": my_rounds}

@router.get("/{round_number}")
def get_one_round(round_number: int):
    round = find_round(round_number)
    if not round:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} was not found")
    return {"result": round}

@router.put("/{round_number}")
def update_round(round_number: int, round: RoundOut):
    updated_round = find_round(round_number)

    if not updated_round:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} was not found")
    
    updated_round.course.course_name = round.course.course_name
 
    # TODO:
    # Neuberechnung noch buggy. Eventuell liegt es an der calculation implementierung. Im Team besprechen
    if (
    updated_round.course.course_par_all != round.course.course_par_all or
    updated_round.course.course_par_1_to_9 != round.course.course_par_1_to_9 or 
    updated_round.course.course_par_10_to_18 != round.course.course_par_10_to_18 or 
    updated_round.course.course_rating_1_to_9 != round.course.course_rating_1_to_9 or
    updated_round.course.course_rating_10_to_18 != round.course.course_rating_10_to_18 or
    updated_round.course.course_rating_all != round.course.course_rating_all or
    updated_round.course.slope_rating != round.course.slope_rating or
    updated_round.course.holes != round.course.holes or
    updated_round.scores != round.scores):
        updated_calc_results = start_calculations(round, my_rounds)
        new_updated_calc_result_2020 = updated_calc_results[0]
        new_updated_calc_result_2021 = updated_calc_results[1]
        updated_round = RoundOut(**round.model_dump())
        updated_round.calc_result_2020=new_updated_calc_result_2020
        updated_round.calc_result_2021=new_updated_calc_result_2021
        updated_round.score_differential=updated_calc_results[2]
    else:
        updated_round = RoundOut(**round.model_dump())

    my_rounds[round_number-1] = updated_round  

    return {"result": updated_round}

@router.delete("/{round_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_round(round_number: int):
    round_index = find_index_round(round_number)
    print(round_index)
    if round_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} does not exist.")

    my_rounds.pop(round_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
