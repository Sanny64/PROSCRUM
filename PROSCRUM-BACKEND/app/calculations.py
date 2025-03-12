from app.models import RoundIn, RoundOut
from app.new_calculations import calculate_whs_handicap
from app.old_calculation import calculate_ega_handicap
from send_EMail import send_email

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
    last_19_rounds = old_rounds[-19:]
    for round in last_19_rounds:
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

    # test values
    EMAIL_RECEIVER = "robin.messer@stud-provadis-hochschule.de"
    RECEIVER_NAME = "Robin Messer"
    ROUND_DATE = "2020-05-21"

    send_email(EMAIL_RECEIVER,RECEIVER_NAME, ROUND_DATE)
     
    return rounds
