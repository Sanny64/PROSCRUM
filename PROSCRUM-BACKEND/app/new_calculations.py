from app.models import CourseWithID

def calculate_score_differential(score, course_rating, slope_rating):
    """
    Berechnet den Score Differential für eine gespielte Runde.

    :param score: Tatsächlicher Score des Spielers (GBE).
    :param course_rating: Course Rating des gespielten Kurses.
    :param slope_rating: Slope Rating des gespielten Kurses.
    :return: Berechneter Score Differential.
    """
    sD = (score - course_rating) * 113 / slope_rating
    return sD

def calculate_CH(hcpi : float, slope_rating : int, course_rating : float, par : int):
    """
    Calculate the player's Course Handicap
    
    :param hcpi: Aktuelles HCPI.
    :param slope_rating: slope rating des gespielten Kurses.
    :return: Berechnetes Course Handicap.
    """
    return round(((hcpi * slope_rating) / 113) + (course_rating - par))

def calculate_whs_handicap(scores: list[int], slope_rating: int, course_rating: float, par: int, old_SDs: list[float], course : CourseWithID, old_HCPI: float = 54, nine_holes : bool = False):
    """
    Berechnet das Handicap nach dem World Handicap System (WHS).

    :param course: der gespielte Kurs
    :param par: das Par der gepsielten Löcher
    :param course_rating: das course rating des Platzes
    :param slope_rating: das slope rating des Platzes
    :param scores: die gespielten scores
    :param old_SDs: Liste von Score Differentials der letzten (maximal) 19 gespielten Runden.
    :param old_HCPI: der akutelle Handicap Index vor der Berechnung.
    :param nine_holes: Handelt es sich bei der neuesten runde um eine Runde mit 9 Löchern
    :return: Berechnetes Handicap-Index., score differential
    """

    score_differentials = old_SDs[:]
    course_handicap = calculate_CH(old_HCPI, slope_rating, course_rating, par)

    if len(score_differentials) == 0:
        round_score = convert_to_GBE_score_first_round(scores, course)
    else:
        round_score = convert_to_GBE_score(scores, course, course_handicap)

    round_SD = calculate_score_differential(round_score, course_rating, slope_rating)
    
    if nine_holes:
        round_SD += get_SD_9_holes_for_HCPI(old_HCPI)
    round_SD = round(round_SD,1)
    score_differentials.append(round_SD)

    handicap_index = get_HDC_for_SDs(score_differentials)

    if old_HCPI >= 26.5:
        if handicap_index > old_HCPI:
            return old_HCPI

    return [round(handicap_index, 1), round_SD]


def get_HDC_for_SDs(score_differentials : list[float]):
    """
    Berechnet den Handicap Index aus den gegebenen letzten Score Differentials.

    :param score_differentials: Die letzten Score Differentials (max 20)
    :return: Den neuen Handicap Index
    """
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

    return (sum(best_scores) / len(best_scores)) + adjustment


def convert_to_GBE_score(netto_scores : list[int], course: CourseWithID, course_hc : float):
    """
    Berechnet den tatsächlich gespielten Score einer Runde

    :param netto_scores: Die gespielten Scores des Spielers.
    :param course: Der gespielte Kurs.
    :param course_hc: Das Course Handicap des gespielten Kurses.
    :return: Das berechnete GesamtBruttoErgebnis.
    """
    holes = course.holes

    GBE_score = 0

    for i, score in enumerate(netto_scores):
        hole_par = holes[i].par
        hole_hdc = holes[i].hdc
        strokes_received = get_strokes_received(course_hc, hole_hdc)
        netto_double_bogey = hole_par + strokes_received + 2
        GBE_score += min(netto_double_bogey, score)
    return GBE_score

def get_strokes_received(course_handicap : float, hole_hdc : int):
    """
    calculates the handicap strokes received at a hole

    :param course_handicap: the course handicap of the player
    :param hole_hdc: the stroke index of the hole
    :return: the handicap strokes received at that hole.
    """
    base_strokes = course_handicap // 18
    thresh_hold = course_handicap % 18
    if hole_hdc <= thresh_hold:
        base_strokes += 1
    return base_strokes

def convert_to_GBE_score_first_round(netto_scores : list[int], course : CourseWithID):
    """
    Berechnet den tastächlichen Score eines Spielers in seiner ersten Runde.


    :param netto_scores: Die gespielten Scores.
    :param course: Der bespielte Kurs.
    :return: Das berechnete GesamtBruttoErgebnis.
    """
    holes = course.holes

    GBE_score = 0

    for i, score in enumerate(netto_scores):
        hole_par = holes[i].par
        netto_double_bogey = hole_par + 5
        GBE_score += min(netto_double_bogey, score)
    return GBE_score


def get_SD_9_holes_for_HCPI(HCPI: float):
    """
    Gibt das zu ergänzende Score Differential bei einer 9 Loch Runde zurück.

    :param HCPI: der HandicapIndex.
    :return: das zu ergänzende Score Differential für die restlichen 9 Löcher
    """
    hcpi_sd_table = {
        -6.0: -1.92, -2.0: 0.16, 2.0: 2.24, 6.0: 4.32, 10.0: 6.40,
        -5.9: -1.87, -1.9: 0.21, 2.1: 2.29, 6.1: 4.37, 10.1: 6.45,
        -5.8: -1.82, -1.8: 0.26, 2.2: 2.34, 6.2: 4.42, 10.2: 6.50,
        -5.7: -1.76, -1.7: 0.32, 2.3: 2.40, 6.3: 4.48, 10.3: 6.56,
        -5.6: -1.71, -1.6: 0.37, 2.4: 2.45, 6.4: 4.53, 10.4: 6.61,
        -5.5: -1.66, -1.5: 0.42, 2.5: 2.50, 6.5: 4.58, 10.5: 6.66,
        -5.4: -1.61, -1.4: 0.47, 2.6: 2.55, 6.6: 4.63, 10.6: 6.71,
        -5.3: -1.56, -1.3: 0.52, 2.7: 2.60, 6.7: 4.68, 10.7: 6.76,
        -5.2: -1.50, -1.2: 0.58, 2.8: 2.66, 6.8: 4.74, 10.8: 6.82,
        -5.1: -1.45, -1.1: 0.63, 2.9: 2.71, 6.9: 4.79, 10.9: 6.87,
        -5.0: -1.40, -1.0: 0.68, 3.0: 2.76, 7.0: 4.84, 11.0: 6.92,
        -4.9: -1.35, -0.9: 0.73, 3.1: 2.81, 7.1: 4.89, 11.1: 6.97,
        -4.8: -1.30, -0.8: 0.78, 3.2: 2.86, 7.2: 4.94, 11.2: 7.02,
        -4.7: -1.24, -0.7: 0.84, 3.3: 2.92, 7.3: 5.00, 11.3: 7.08,
        -4.6: -1.19, -0.6: 0.89, 3.4: 2.97, 7.4: 5.05, 11.4: 7.13,
        -4.5: -1.14, -0.5: 0.94, 3.5: 3.02, 7.5: 5.10, 11.5: 7.18,
        -4.4: -1.09, -0.4: 0.99, 3.6: 3.07, 7.6: 5.15, 11.6: 7.23,
        -4.3: -1.04, -0.3: 1.04, 3.7: 3.12, 7.7: 5.20, 11.7: 7.28,
        -4.2: -0.98, -0.2: 1.10, 3.8: 3.18, 7.8: 5.26, 11.8: 7.34,
        -4.1: -0.93, -0.1: 1.15, 3.9: 3.23, 7.9: 5.31, 11.9: 7.39,
        -4.0: -0.88, 0.0: 1.20, 4.0: 3.28, 8.0: 5.36, 12.0: 7.44,
        -3.9: -0.83, 0.1: 1.25, 4.1: 3.33, 8.1: 5.41, 12.1: 7.49,
        -3.8: -0.78, 0.2: 1.30, 4.2: 3.38, 8.2: 5.46, 12.2: 7.54,
        -3.7: -0.72, 0.3: 1.36, 4.3: 3.44, 8.3: 5.52, 12.3: 7.60,
        -3.6: -0.67, 0.4: 1.41, 4.4: 3.49, 8.4: 5.57, 12.4: 7.65,
        -3.5: -0.62, 0.5: 1.46, 4.5: 3.54, 8.5: 5.62, 12.5: 7.70,
        -3.4: -0.57, 0.6: 1.51, 4.6: 3.59, 8.6: 5.67, 12.6: 7.75,
        -3.3: -0.52, 0.7: 1.56, 4.7: 3.64, 8.7: 5.72, 12.7: 7.80,
        -3.2: -0.46, 0.8: 1.62, 4.8: 3.70, 8.8: 5.78, 12.8: 7.86,
        -3.1: -0.41, 0.9: 1.67, 4.9: 3.75, 8.9: 5.83, 12.9: 7.91,
        -3.0: -0.36, 1.0: 1.72, 5.0: 3.80, 9.0: 5.88, 13.0: 7.96,
        -2.9: -0.31, 1.1: 1.77, 5.1: 3.85, 9.1: 5.93, 13.1: 8.01,
        -2.8: -0.26, 1.2: 1.82, 5.2: 3.90, 9.2: 5.98, 13.2: 8.06,
        -2.7: -0.20, 1.3: 1.88, 5.3: 3.96, 9.3: 6.04, 13.3: 8.12,
        -2.6: -0.15, 1.4: 1.93, 5.4: 4.01, 9.4: 6.09, 13.4: 8.17,
        -2.5: -0.10, 1.5: 1.98, 5.5: 4.06, 9.5: 6.14, 13.5: 8.22,
        -2.4: -0.05, 1.6: 2.03, 5.6: 4.11, 9.6: 6.19, 13.6: 8.27,
        -2.3:  0.00, 1.7: 2.08, 5.7: 4.16, 9.7: 6.24, 13.7: 8.32,
        -2.2:  0.06, 1.8: 2.14, 5.8: 4.22, 9.8: 6.30, 13.8: 8.38,
        -2.1:  0.11, 1.9: 2.19, 5.9: 4.27, 9.9: 6.35, 13.9: 8.43,
        14.0:  8.48, 18.0: 10.56, 22.0: 12.64, 26.0: 14.72, 30.0: 16.80,
        14.1:  8.53, 18.1: 10.61, 22.1: 12.69, 26.1: 14.77, 30.1: 16.85,
        14.2:  8.58, 18.2: 10.66, 22.2: 12.74, 26.2: 14.82, 30.2: 16.90,
        14.3:  8.64, 18.3: 10.72, 22.3: 12.80, 26.3: 14.88, 30.3: 16.96,
        14.4:  8.69, 18.4: 10.77, 22.4: 12.85, 26.4: 14.93, 30.4: 17.01,
        14.5:  8.74, 18.5: 10.82, 22.5: 12.90, 26.5: 14.98, 30.5: 17.06,
        14.6:  8.79, 18.6: 10.87, 22.6: 12.95, 26.6: 15.03, 30.6: 17.11,
        14.7:  8.84, 18.7: 10.92, 22.7: 13.00, 26.7: 15.08, 30.7: 17.16,
        14.8:  8.90, 18.8: 10.98, 22.8: 13.06, 26.8: 15.14, 30.8: 17.22,
        14.9:  8.95, 18.9: 11.03, 22.9: 13.11, 26.9: 15.19, 30.9: 17.27,
        15.0:  9.00, 19.0: 11.08, 23.0: 13.16, 27.0: 15.24, 31.0: 17.32,
        15.1:  9.05, 19.1: 11.13, 23.1: 13.21, 27.1: 15.29, 31.1: 17.37,
        15.2:  9.10, 19.2: 11.18, 23.2: 13.26, 27.2: 15.34, 31.2: 17.42,
        15.3:  9.16, 19.3: 11.24, 23.3: 13.32, 27.3: 15.40, 31.3: 17.48,
        15.4:  9.21, 19.4: 11.29, 23.4: 13.37, 27.4: 15.45, 31.4: 17.53,
        15.5:  9.26, 19.5: 11.34, 23.5: 13.42, 27.5: 15.50, 31.5: 17.58,
        15.6:  9.31, 19.6: 11.39, 23.6: 13.47, 27.6: 15.55, 31.6: 17.63,
        15.7:  9.36, 19.7: 11.44, 23.7: 13.52, 27.7: 15.60, 31.7: 17.68,
        15.8:  9.42, 19.8: 11.50, 23.8: 13.58, 27.8: 15.66, 31.8: 17.74,
        15.9:  9.47, 19.9: 11.55, 23.9: 13.63, 27.9: 15.71, 31.9: 17.79,
        16.0:  9.52, 20.0: 11.60, 24.0: 13.68, 28.0: 15.76, 32.0: 17.84,
        16.1:  9.57, 20.1: 11.65, 24.1: 13.73, 28.1: 15.81, 32.1: 17.89,
        16.2:  9.62, 20.2: 11.70, 24.2: 13.78, 28.2: 15.86, 32.2: 17.94,
        16.3:  9.68, 20.3: 11.76, 24.3: 13.84, 28.3: 15.92, 32.3: 18.00,
        16.4:  9.73, 20.4: 11.81, 24.4: 13.89, 28.4: 15.97, 32.4: 18.05,
        16.5:  9.78, 20.5: 11.86, 24.5: 13.94, 28.5: 16.02, 32.5: 18.10,
        16.6:  9.83, 20.6: 11.91, 24.6: 13.99, 28.6: 16.07, 32.6: 18.15,
        16.7:  9.88, 20.7: 11.96, 24.7: 14.04, 28.7: 16.12, 32.7: 18.20,
        16.8:  9.94, 20.8: 12.02, 24.8: 14.10, 28.8: 16.18, 32.8: 18.26,
        16.9:  9.99, 20.9: 12.07, 24.9: 14.15, 28.9: 16.23, 32.9: 18.31,
        17.0: 10.04, 21.0: 12.12, 25.0: 14.20, 29.0: 16.28, 33.0: 18.36,
        17.1: 10.09, 21.1: 12.17, 25.1: 14.25, 29.1: 16.33, 33.1: 18.41,
        17.2: 10.14, 21.2: 12.22, 25.2: 14.30, 29.2: 16.38, 33.2: 18.46,
        17.3: 10.20, 21.3: 12.28, 25.3: 14.36, 29.3: 16.44, 33.3: 18.52,
        17.4: 10.25, 21.4: 12.33, 25.4: 14.41, 29.4: 16.49, 33.4: 18.57,
        17.5: 10.30, 21.5: 12.38, 25.5: 14.46, 29.5: 16.54, 33.5: 18.62,
        17.6: 10.35, 21.6: 12.43, 25.6: 14.51, 29.6: 16.59, 33.6: 18.67,
        17.7: 10.40, 21.7: 12.48, 25.7: 14.56, 29.7: 16.64, 33.7: 18.72,
        17.8: 10.46, 21.8: 12.54, 25.8: 14.62, 29.8: 16.70, 33.8: 18.78,
        17.9: 10.51, 21.9: 12.59, 25.9: 14.67, 29.9: 16.75, 33.9: 18.83,
        34.0: 18.88, 38.0: 20.96, 42.0: 23.04, 46.0: 25.12, 50.0: 27.20,
        34.1: 18.93, 38.1: 21.01, 42.1: 23.09, 46.1: 25.17, 50.1: 27.25,
        34.2: 18.98, 38.2: 21.06, 42.2: 23.14, 46.2: 25.22, 50.2: 27.30,
        34.3: 19.04, 38.3: 21.12, 42.3: 23.20, 46.3: 25.28, 50.3: 27.36,
        34.4: 19.09, 38.4: 21.17, 42.4: 23.25, 46.4: 25.33, 50.4: 27.41,
        34.5: 19.14, 38.5: 21.22, 42.5: 23.30, 46.5: 25.38, 50.5: 27.46,
        34.6: 19.19, 38.6: 21.27, 42.6: 23.35, 46.6: 25.43, 50.6: 27.51,
        34.7: 19.24, 38.7: 21.32, 42.7: 23.40, 46.7: 25.48, 50.7: 27.56,
        34.8: 19.30, 38.8: 21.38, 42.8: 23.46, 46.8: 25.54, 50.8: 27.62,
        34.9: 19.35, 38.9: 21.43, 42.9: 23.51, 46.9: 25.59, 50.9: 27.67,
        35.0: 19.40, 39.0: 21.48, 43.0: 23.56, 47.0: 25.64, 51.0: 27.72,
        35.1: 19.45, 39.1: 21.53, 43.1: 23.61, 47.1: 25.69, 51.1: 27.77,
        35.2: 19.50, 39.2: 21.58, 43.2: 23.66, 47.2: 25.74, 51.2: 27.82,
        35.3: 19.56, 39.3: 21.64, 43.3: 23.72, 47.3: 25.80, 51.3: 27.88,
        35.4: 19.61, 39.4: 21.69, 43.4: 23.77, 47.4: 25.85, 51.4: 27.93,
        35.5: 19.66, 39.5: 21.74, 43.5: 23.82, 47.5: 25.90, 51.5: 27.98,
        35.6: 19.71, 39.6: 21.79, 43.6: 23.87, 47.6: 25.95, 51.6: 28.03,
        35.7: 19.76, 39.7: 21.84, 43.7: 23.92, 47.7: 26.00, 51.7: 28.08,
        35.8: 19.82, 39.8: 21.90, 43.8: 23.98, 47.8: 26.06, 51.8: 28.14,
        35.9: 19.87, 39.9: 21.95, 43.9: 24.03, 47.9: 26.11, 51.9: 28.19,
        36.0: 19.92, 40.0: 22.00, 44.0: 24.08, 48.0: 26.16, 52.0: 28.24,
        36.1: 19.97, 40.1: 22.05, 44.1: 24.13, 48.1: 26.21, 52.1: 28.29,
        36.2: 20.02, 40.2: 22.10, 44.2: 24.18, 48.2: 26.26, 52.2: 28.34,
        36.3: 20.08, 40.3: 22.16, 44.3: 24.24, 48.3: 26.32, 52.3: 28.40,
        36.4: 20.13, 40.4: 22.21, 44.4: 24.29, 48.4: 26.37, 52.4: 28.45,
        36.5: 20.18, 40.5: 22.26, 44.5: 24.34, 48.5: 26.42, 52.5: 28.50,
        36.6: 20.23, 40.6: 22.31, 44.6: 24.39, 48.6: 26.47, 52.6: 28.55,
        36.7: 20.28, 40.7: 22.36, 44.7: 24.44, 48.7: 26.52, 52.7: 28.60,
        36.8: 20.34, 40.8: 22.42, 44.8: 24.50, 48.8: 26.58, 52.8: 28.66,
        36.9: 20.39, 40.9: 22.47, 44.9: 24.55, 48.9: 26.63, 52.9: 28.71,
        37.0: 20.44, 41.0: 22.52, 45.0: 24.60, 49.0: 26.68, 53.0: 28.76,
        37.1: 20.49, 41.1: 22.57, 45.1: 24.65, 49.1: 26.73, 53.1: 28.81,
        37.2: 20.54, 41.2: 22.62, 45.2: 24.70, 49.2: 26.78, 53.2: 28.86,
        37.3: 20.60, 41.3: 22.68, 45.3: 24.76, 49.3: 26.84, 53.3: 28.92,
        37.4: 20.65, 41.4: 22.73, 45.4: 24.81, 49.4: 26.89, 53.4: 28.97,
        37.5: 20.70, 41.5: 22.78, 45.5: 24.86, 49.5: 26.94, 53.5: 29.02,
        37.6: 20.75, 41.6: 22.83, 45.6: 24.91, 49.6: 26.99, 53.6: 29.07,
        37.7: 20.80, 41.7: 22.88, 45.7: 24.96, 49.7: 27.04, 53.7: 29.12,
        37.8: 20.86, 41.8: 22.94, 45.8: 25.02, 49.8: 27.10, 53.8: 29.18,
        37.9: 20.91, 41.9: 22.99, 45.9: 25.07, 49.9: 27.15, 53.9: 29.23,
        54.0: 29.28
    }

    if HCPI in hcpi_sd_table:
        return hcpi_sd_table[HCPI]
    else:
        rounded_hcpi= round(HCPI, 1)
        if rounded_hcpi in hcpi_sd_table:
            return hcpi_sd_table[rounded_hcpi]
        else:
            raise IndexError("HCPI not in table, what did u do?", HCPI)
