from app.models import RoundIn, RoundOut
from app.new_calculations import calculate_whs_handicap
from app.old_calculation import calculate_ega_handicap

def start_calculations(new_round: RoundIn, old_rounds: list[RoundOut]):
    """
    Berechnet das neue HDC eines Spielers im EGA und WHS

    :param new_round: die neueste Runde des Spielers
    :param old_rounds: die bisher gespielten runden des Spielers
    :return: the new hdcs and score differential for the round ([old_calc, new_calc, score_differential])
    """

    # get current HDC
    if old_rounds:  # Check if the list is not empty
        old_hdc_2020 = old_rounds[-1].calc_result_2020
        if new_round.date.year >= 2021:
            old_hdc_2021 = old_rounds[-1].calc_result_2021
        else: 
            old_hdc_2021 = -old_hdc_2020
    else:
        old_hdc_2020 = -54  # Default value if list is empty
        old_hdc_2021 = 54  # Default value if list is empty

    # get old Score Differentials for new calculation of the last 19 rounds
    old_SDs = []
    for round in old_rounds[19:]:
        old_SDs.append(round.score_differential)

    current_course = new_round.course
    slope_rating = current_course.slope_rating
    scores = new_round.scores
    nine_hole = True
    holes_played = current_course.holes

    # filter holes, scores and take correct course rating (if its a nine hoel round)
    if all(x == 0 for x in new_round.scores[:9]): # check if the first 9 scores are 0
        scores = scores[9:] # drop first 9
        holes_played = holes_played[9:]
        course_rating = current_course.course_rating_10_to_18
        course_par = current_course.course_par_10_to_18
    elif all(x == 0 for x in scores[9:]): # check if the last 9 scores are 0
        scores = scores[:9]
        holes_played = holes_played[:9]
        course_rating = current_course.course_rating_1_to_9
        course_par = current_course.course_par_1_to_9
    else:
        nine_hole = False
        course_rating = current_course.course_rating_all
        course_par = current_course.course_par_all
    
    

    # calculate the handicaps
    handicaps = [calculate_ega_handicap(old_hdc_2020, holes_played, slope_rating, course_rating, course_par, scores, nine_hole)]
    result_new = calculate_whs_handicap(scores, slope_rating, course_rating, course_par, old_SDs, holes_played, old_hdc_2021, nine_hole)
    handicaps.append(result_new[0])
    handicaps.append(result_new[1])
    return handicaps
