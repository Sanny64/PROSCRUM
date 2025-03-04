from fastapi import Response, status, HTTPException, APIRouter

from ..utils import find_round, find_index_round
from ..models import RoundIn, RoundOut
from ..calculations import start_calculations
from ..mockups import my_rounds

router = APIRouter(
    prefix="/rounds",
    tags=['Rounds']
)

@router.post("/")
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

@router.delete("/{round_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_round(round_number: int):
    round_index = find_index_round(round_number)
    print(round_index)
    if round_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"round with round_number: {round_number} does not exist.")

    my_rounds.pop(round_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)