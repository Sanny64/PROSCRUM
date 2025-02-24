from app.models import Course, RoundOut
from app.models import HoleConfig

def calculate_score_differential(score, course_rating, slope_rating):
    """
    Berechnet den Score Differential für eine gespielte Runde.

    :param score: Tatsächlicher Score des Spielers.
    :param course_rating: Course Rating des gespielten Kurses.
    :param slope_rating: Slope Rating des gespielten Kurses.
    :param par: Par des gespielten Kurses.
    :return: Berechneter Score Differential.
    """
    return (score - course_rating) * 113 / slope_rating

def calculate_whs_handicap(rounds: list[RoundOut]):
    """
    Berechnet das Handicap nach dem World Handicap System (WHS).

    :param scores: Liste von Scores der gespielten Runden.
    :param course_ratings: Liste von Course Ratings der gespielten Runden.
    :param slope_ratings: Liste von Slope Ratings der gespielten Runden.
    :param pars: Liste von Pars der gespielten Runden.
    :return: Berechnetes Handicap-Index.
    """
    if len(rounds) < 1:
        raise ValueError("Mindestens 1 Runde ist erforderlich, um ein Handicap zu berechnen.")

    # Berechne die Score Differentials
    score_differentials = []

    for r in rounds:

        if (len(r.scores) == 18):
            round_GBE = convert_to_GBE(r.scores, r.course)
        else:
            round_GBE = convert_to_GBE_9_holes(r.scores, r.course)

        round_SD = calculate_score_differential(round_GBE, r.course.course_rating, r.course.slope_rating)
        score_differentials.append(round_SD)


    score_differentials.sort()  # Sortiere die Differentials aufsteigend

    if len(score_differentials) == 1:
        best_scores = score_differentials[:1]
        adjustment = -2.0
    elif len(score_differentials) == 2:
        best_scores = score_differentials[:1]
        adjustment = -2.0
    elif len(score_differentials) == 3:
        best_scores = score_differentials[:1]
        adjustment = -2.0
    elif len(score_differentials) == 4:
        best_scores = score_differentials[:1]
        adjustment = -1.0
    elif len(score_differentials) == 5:
        best_scores = score_differentials[:1]
        adjustment = 0.0
    elif len(score_differentials) == 6:
        best_scores = score_differentials[:2]
        adjustment = -1.0
    elif len(score_differentials) in [7, 8]:
        best_scores = score_differentials[:2]
        adjustment = 0.0
    elif len(score_differentials) in [9, 10, 11]:
        best_scores = score_differentials[:3]
        adjustment = 0.0
    elif len(score_differentials) in [12, 13, 14]:
        best_scores = score_differentials[:4]
        adjustment = 0.0
    elif len(score_differentials) in [15, 16]:
        best_scores = score_differentials[:5]
        adjustment = 0.0
    elif len(score_differentials) in [17, 18]:
        best_scores = score_differentials[:6]
        adjustment = 0.0
    elif len(score_differentials) == 19:
        best_scores = score_differentials[:7]
        adjustment = 0.0
    else:
        best_scores = score_differentials[:8]
        adjustment = 0.0


    handicap_index = (sum(best_scores) / len(best_scores)) + adjustment
    return round(handicap_index, 1)


def convert_to_GBE(old_scores : list[int], course: Course):

    holes = course.holes

    new_scores = []

    for i, score in enumerate(old_scores):
        hole_par = holes[i].par
        hole_hdc = holes[i].hdc
        netto_double_bogey = hole_par + hole_hdc + 2
        if netto_double_bogey < score:
            new_scores.append(netto_double_bogey)
        else:
            new_scores.append(score)
    return sum(new_scores)


def convert_to_GBE_9_holes(old_scores : list[float], course: Course):

    holes = course.holes

    if (len(holes) < 17):
        raise IndexError("Kurs hat keine 18 Löcher")

    new_scores = convert_to_GBE(old_scores, course)

    if (len(old_scores) > 9):
        raise ValueError(f"score liste ist zu lang: benötigt: 18, gegeben: {len(old_scores)}")
    
    hole_pars = []
    hole_hdcs = []
    for i in range(9, 17):
        hole = holes[i]
        hole_pars.append(hole.par)
        hole_hdcs.append(hole.hdc)
    return sum(new_scores) + sum(hole_pars) + sum(hole_hdcs) + 9
