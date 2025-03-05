from app.models import RoundIn, RoundOut
from app.new_calculations import calculate_whs_handicap
from app.old_calculation import calculate_ega_handicap

def start_calculations(new_round: RoundIn, old_rounds: list[RoundOut]):

    if old_rounds:  # Check if the list is not empty
        old_hdc_2020 = old_rounds[-1].calc_result_2020
        old_hdc_2021 = old_rounds[-1].calc_result_2021
    else:
        old_hdc_2020 = -54  # Default value if list is empty
        old_hdc_2021 = 54  # Default value if list is empty

    old_SDs = []
    for round in old_rounds:
        old_SDs.append(round.score_differential)

    current_course = new_round.course
    if current_course.course_rating_9 is not None:
        course_rating = current_course.course_rating_9
        nine_hole = True
    else:
        course_rating = current_course.course_rating_18
        nine_hole = False

    # calculate the handicaps
    handicaps = []
    handicaps.append(calculate_ega_handicap(old_hdc_2020, current_course.holes, current_course.slope_rating,course_rating , current_course.course_par, new_round.scores, nine_hole))
    result_new = calculate_whs_handicap(new_round=new_round, old_SDs=old_SDs, old_HCPI=old_hdc_2021, nine_holes = nine_hole)
    handicaps.append(result_new[0])
    handicaps.append(result_new[1])
    return handicaps


def update_calculations(updated_round: RoundIn, rounds: list[RoundOut]):
    """
    Aktualisiert das Handicap nach einer Änderung in einer Runde für alle Runden

    :param updated_round: die aktualisierte Runde
    :param rounds: die Liste der Runden des Spielers
    :return: die neue Liste an Runden (aktualisiert, provisorisch bis Datenbankanschluss)
    """
    updated_round_out = RoundOut(
        **updated_round.model_dump(),
        calc_result_2020=0.0,
        calc_result_2021=0.0,
        score_differential=0.0
    )

    updated_round_out.calc_result_2020, updated_round_out.calc_result_2021, updated_round_out.score_differential = start_calculations(updated_round, rounds[:updated_round.round_number])
    
    for i in range(len(rounds)):
        if rounds[i].round_number == updated_round.round_number:
            rounds[i] = updated_round_out
        elif rounds[i].round_number > updated_round.round_number:
            rounds[i].calc_result_2020, rounds[i].calc_result_2021, rounds[i].score_differential = start_calculations(rounds[i], rounds[:rounds[i].round_number])
     
    return rounds
