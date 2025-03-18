from fastapi import Response, status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from ..models import RoundIn, RoundOut
from ..calculations import start_calculations, update_calculations

from ..database import get_db
from .. import schemas, oauth2, models


router = APIRouter(
    prefix="/rounds",
    tags=['Rounds']
)

def convert_to_round_out(round: schemas.Round, db: Session) -> RoundOut:
    round_course = db.query(schemas.Course).filter(schemas.Course.course_id == round.course_id).first()

    round_course_holes_db = db.query(schemas.Hole).filter(schemas.Hole.course_id == round.course_id).all()

    hole_config_list = []
    for hole in round_course_holes_db:
        hole_config = models.HoleConfig(hole=hole.hole, par=hole.par, hdc=hole.hdc)
        hole_config_list.append(hole_config)

    leaders = db.query(schemas.Course_Leader_Secretary).filter(schemas.Course_Leader_Secretary.course_id == round_course.course_id).all()
    leaders_secretaries = [user_id.user_id for user_id in leaders]

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
        holes=hole_config_list,
        leaders_secretaries=leaders_secretaries
    )

    scores = []
    round_scores_db = db.query(schemas.Score).filter(schemas.Score.score_id == round.score_id).first()
    for i in range(18):
        stroke = getattr(round_scores_db, 'hole_' + str(i+1) + '_strokes')
        scores.append(stroke)

    user = db.query(schemas.User).filter(schemas.User.user_id == round.user_id).first()
    round_out = RoundOut(
        round_id=round.round_id,
        user_id=round.user_id,
        round_number=round.round_number,
        course=round_course_with_id,
        scores=scores,
        date=round.date,
        calc_result_2020=round.hdc_2020,
        calc_result_2021=round.hdc_2021,
        score_differential=round.score_differential,
        user=user
    )
    return round_out

@router.post("/")
def create_round(round: RoundIn, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id > 1 and current_user.role_id < 4:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    
    user_rounds = db.query(schemas.Round).filter(schemas.Round.user_id == current_user.user_id).all()

    calc_rounds = []
    for user_round in user_rounds:
        round_out = convert_to_round_out(user_round, db)
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

@router.get("/", response_model=list[models.RoundOut])
def get_rounds(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id >= 3:
        all_rounds = db.query(schemas.Round).all()
        all_round_outs = []
        for round in all_rounds:
            round_out = convert_to_round_out(round, db)
            all_round_outs.append(round_out)
        return all_round_outs
    elif current_user.role_id >= 2:
        leader_secretaries = db.query(schemas.Course_Leader_Secretary).filter(schemas.Course_Leader_Secretary.user_id == current_user.user_id).all()
        course_id_list = [ls.course_id for ls in leader_secretaries]
        all_rounds = db.query(schemas.Round).all()
        all_round_outs = []
        for round in all_rounds:
            round_out = convert_to_round_out(round, db)
            if round_out.course.course_id in course_id_list:
                all_round_outs.append(round_out)
        return all_round_outs
    elif current_user.role_id == 1:
        user_rounds = db.query(schemas.Round).filter(schemas.Round.user_id == current_user.user_id).all()
        all_user_round_outs = []
        for round in user_rounds:
            round_out = convert_to_round_out(round, db)
            all_user_round_outs.append(round_out)
        return all_user_round_outs
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
        

@router.get("/{round_number}", response_model=list[models.RoundOut])
def get_one_round(round_number: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id == 4:
        all_rounds = db.query(schemas.Round).all()
        all_round_outs = []
        for round in all_rounds:
            round_out = convert_to_round_out(round, db)
            all_round_outs.append(round_out)
        return all_round_outs
    elif current_user.role_id == 1:
        round = db.query(schemas.Round).filter(
            schemas.Round.round_number == round_number,
            schemas.Round.user_id == current_user.user_id
        ).first()
        if not round:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} was not found")
        
        round_out = convert_to_round_out(round, db)
        return [round_out]
    elif current_user.role_id >= 2:
        leader_secretaries = db.query(schemas.Course_Leader_Secretary).filter(schemas.Course_Leader_Secretary.user_id == current_user.user_id).all()
        course_id_list = [ls.course_id for ls in leader_secretaries]
        all_rounds = db.query(schemas.Round).all()
        all_round_outs = []
        for round in all_rounds:
            round_out = convert_to_round_out(round, db)
            if round_out.course.course_id in course_id_list:
                all_round_outs.append(round_out)
        return all_round_outs
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")

@router.put("/{round_number}")
def update_round(round_number: int, round: RoundOut, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    if current_user.role_id < 2 or current_user.role_id == 3:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action.")
    else:
        updated_round = db.query(schemas.Round).filter(
            schemas.Round.round_number == round_number,
            schemas.Round.course_id == round.course.course_id,
            schemas.Round.user_id == round.user_id
        ).first()

        if not updated_round:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} was not found")
        
        updated_round_out = convert_to_round_out(updated_round, db)

        if (
        updated_round_out.scores != round.scores or
        updated_round_out.course.course_par_all != round.course.course_par_all or
        updated_round_out.course.course_par_1_to_9 != round.course.course_par_1_to_9 or 
        updated_round_out.course.course_par_10_to_18 != round.course.course_par_10_to_18 or 
        updated_round_out.course.course_rating_1_to_9 != round.course.course_rating_1_to_9 or
        updated_round_out.course.course_rating_10_to_18 != round.course.course_rating_10_to_18 or
        updated_round_out.course.course_rating_all != round.course.course_rating_all or
        updated_round_out.course.slope_rating != round.course.slope_rating or
        updated_round_out.course.holes != round.course.holes):
            user_rounds = db.query(schemas.Round).filter(schemas.Round.user_id == round.user_id).all()
            all_user_round_outs = []
            for r in user_rounds:
                round_out = convert_to_round_out(r, db)
                all_user_round_outs.append(round_out)

            score_query = db.query(schemas.Score).filter(schemas.Score.score_id == updated_round.score_id)
            updated_scores = []
            updated_scores.append(updated_round.score_id)
            for score in round.scores:
                updated_scores.append(score)
            score_query.update(updated_scores, synchronize_session=False)
            db.commit()

            updated_rounds = update_calculations(round, all_user_round_outs)

            for r in updated_rounds:                
                round_query = db.query(schemas.Round).filter(schemas.Round.round_id == r.round_id)
                round_db = round_query.first()
                r_dict = r.model_dump()
                r_dict["course_id"] = r.course.course_id
                r_dict["score_id"] = round_db.score_id
                r_dict["hdc_2020"] = r.calc_result_2020
                r_dict["hdc_2021"] = r.calc_result_2021
                r_dict.pop("calc_result_2021", None)
                r_dict.pop("calc_result_2020", None)
                r_dict.pop("user", None)
                r_dict.pop("course", None)
                r_dict.pop("scores", None)
                print(r_dict)
                round_query.update(r_dict, synchronize_session=False)
                db.commit()
            
            db.refresh(updated_round)
            updated_round_out = convert_to_round_out(updated_round, db)

        else:
            updated_round_out = RoundOut(**round.model_dump())


        return {"result": updated_round_out}

@router.delete("/{round_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_round(round_number: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    round_query = db.query(schemas.Round).filter(
        schemas.Round.round_number == round_number,
        schemas.Round.user_id == current_user.user_id
    )
    
    round = round_query.first()

    score_query = db.query(schemas.Score).filter(schemas.Score.score_id == round.score_id)
    
    if round is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} for user_id: {current_user.user_id} does not exist.")

    round_query.delete(synchronize_session=False)
    db.commit()
    score_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
