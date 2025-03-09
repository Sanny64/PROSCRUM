from app.models import HoleConfig, CourseWithID, RoundIn, RoundOut
from app.calculations import start_calculations
from datetime import date

def generate_courses():
    courses_list = []
    
    course_1 = CourseWithID(
    course_id=1,
    course_name="Sunny Hills Golf Course",
    course_par_1_to_9=35,
    course_par_10_to_18=37,
    course_par_all=72,
    course_rating_1_to_9=34.1,
    course_rating_10_to_18=35.4,
    course_rating_all=70.9,
    slope_rating=115,
    holes=[
        HoleConfig(hole=1, par=3, hdc=4),
        HoleConfig(hole=2, par=4, hdc=16),
        HoleConfig(hole=3, par=4, hdc=1),
        HoleConfig(hole=4, par=5, hdc=10),
        HoleConfig(hole=5, par=4, hdc=7),
        HoleConfig(hole=6, par=4, hdc=13),
        HoleConfig(hole=7, par=3, hdc=5),
        HoleConfig(hole=8, par=4, hdc=17),
        HoleConfig(hole=9, par=4, hdc=2),
        HoleConfig(hole=10, par=5, hdc=11),
        HoleConfig(hole=11, par=4, hdc=8),
        HoleConfig(hole=12, par=4, hdc=14),
        HoleConfig(hole=13, par=3, hdc=6),
        HoleConfig(hole=14, par=4, hdc=18),
        HoleConfig(hole=15, par=4, hdc=3),
        HoleConfig(hole=16, par=5, hdc=12),
        HoleConfig(hole=17, par=4, hdc=9),
        HoleConfig(hole=18, par=4, hdc=15)
    ]
    )
    courses_list.append(course_1)
    
    course_2 = CourseWithID(
    course_id=2,
    course_name="Shady Hills Golf Course",
    course_par_1_to_9=35,
    course_par_10_to_18=37,
    course_par_all=72,
    course_rating_1_to_9=35.7,
    course_rating_10_to_18=36.1,
    course_rating_all=72.3,
    slope_rating=130,
    holes=[
        HoleConfig(hole=1, par=3, hdc=16),
        HoleConfig(hole=2, par=4, hdc=1),
        HoleConfig(hole=3, par=4, hdc=10),
        HoleConfig(hole=4, par=5, hdc=7),
        HoleConfig(hole=5, par=4, hdc=13),
        HoleConfig(hole=6, par=4, hdc=4),
        HoleConfig(hole=7, par=3, hdc=17),
        HoleConfig(hole=8, par=4, hdc=2),
        HoleConfig(hole=9, par=4, hdc=11),
        HoleConfig(hole=10, par=5, hdc=8),
        HoleConfig(hole=11, par=4, hdc=14),
        HoleConfig(hole=12, par=4, hdc=5),
        HoleConfig(hole=13, par=3, hdc=18),
        HoleConfig(hole=14, par=4, hdc=3),
        HoleConfig(hole=15, par=4, hdc=12),
        HoleConfig(hole=16, par=5, hdc=9),
        HoleConfig(hole=17, par=4, hdc=15),
        HoleConfig(hole=18, par=4, hdc=6)
    ]
    )
    courses_list.append(course_2)
    
    return courses_list
    

def generate_round_in(courses_list):
    round_in = []
    
    course_1 = courses_list[0]

    # Runde 1
    round_1 = RoundIn(
    course=course_1,
    round_number=1,
    scores=[5, 6, 8, 7, 6, 6, 6, 6, 6, 7, 6, 6, 5, 6, 6, 6, 5, 6],
    date=date(2020, 12, 2)
    )
    round_in.append(round_1)

    # Runde 2
    round_2 = RoundIn(
    course=course_1,
    round_number=2,
    scores=[4, 5, 5, 6, 6, 5, 6, 9, 5, 5, 6, 6, 5, 6, 6, 6, 5, 6],
    date=date(2020, 12, 3)
    )
    round_in.append(round_2)

    course_3 = courses_list[1]

    round_3 = RoundIn(
    course=course_3,
    round_number=3,
    scores=[4, 5, 5, 6, 6, 7, 4, 8, 4, 5, 6, 6, 5, 6, 6, 6, 5, 6],
    date=date(2020, 12, 4)
    )
    round_in.append(round_3)

    # Runde 4 (Verwendet das gleiche Course-Objekt wie für Runde 3)
    round_4 = RoundIn(
    course=course_3,
    round_number=4,
    scores=[5, 6, 6, 7, 6, 6, 4, 7, 6, 7, 6, 6, 5, 5, 6, 6, 5, 6],
    date=date(2020, 12, 5)
    )
    round_in.append(round_4)

    # Runde 5
    round_5 = RoundIn(
    course=course_1,
    round_number=5,
    scores=[4, 5, 5, 6, 5, 5, 4, 5, 5, 6, 5, 5, 4, 5, 5, 6, 5, 5],
    date=date(2020, 12, 6)
    )
    round_in.append(round_5)

    # Runde 6 (9 Löcher von Course 1)
    course_6 = courses_list[0]

    round_6 = RoundIn(
    course=course_6,
    round_number=6,
    scores=[5, 6, 6, 7, 6, 5, 5, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    date=date(2020, 12, 7)
    )
    round_in.append(round_6)

    # Runde 7 (Verwendet das gleiche Course-Objekt wie für Runde 6)
    round_7 = RoundIn(
    course=course_6,
    round_number=7,
    scores=[5, 7, 9, 7, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    date=date(2020, 12, 24)
    )
    round_in.append(round_7)

    # Runde 8 (Verwendet das gleiche Course-Objekt wie für Runde 1 und 5)
    round_8 = RoundIn(
    course=course_1,
    round_number=8,
    scores=[4, 5, 5, 6, 6, 5, 4, 5, 5, 7, 5, 5, 4, 5, 5, 7, 5, 5],
    date=date(2022, 12, 2)
    )
    round_in.append(round_8)

    # Runde 9 (Verwendet das gleiche Course-Objekt wie für Runde 3 und 4) glaube falsch
    round_9 = RoundIn(
    course=course_3,
    round_number=9,
    scores=[4, 5, 5, 6, 5, 5, 4, 5, 5, 6, 5, 5, 4, 5, 5, 6, 5, 5],
    date=date(2022, 12, 3)
    )
    round_in.append(round_9)

    # Runde 10 irgendwie course 1
    course_10 = courses_list[1]
        
    round_10 = RoundIn(
    course=course_10,
    round_number=10,
    scores=[4, 5, 5, 6, 5, 5, 4, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    date=date(2022, 12, 4)
    )
    round_in.append(round_10)

    # Runde 11 (Verwendet das gleiche Course-Objekt wie für Runde 10)
    round_11 = RoundIn(
    course=course_10,
    round_number=11,
    scores=[5, 6, 6, 7, 6, 6, 5, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    date=date(2022, 12, 5)
    )
    round_in.append(round_11)

    # Runde 12 (Verwendet das gleiche Course-Objekt wie für Runde 3, 4, 9 und 10)
    round_12 = RoundIn(
    course=course_3,
    round_number=12,
    scores=[6, 7, 7, 8, 7, 7, 6, 7, 10, 8, 7, 7, 6, 7, 7, 8, 7, 7],
    date=date(2022, 12, 6)
    )
    round_in.append(round_12)
    
    return round_in

def calculate_round_outs(round_ins: list[RoundIn]):
    round_out_list = []
    
    for round in round_ins:
        calc_result = start_calculations(round, round_out_list)
        new_calc_result_2020 = calc_result[0]
        new_calc_result_2021 = calc_result[1]
        round_score_differential = calc_result[2]

        new_round = RoundOut(
            **round.model_dump(),
            calc_result_2020=new_calc_result_2020, 
            calc_result_2021=new_calc_result_2021, 
            score_differential=round_score_differential
        )
        round_out_list.append(new_round)
        
    return round_out_list

def generate_mockups():
    courses_list = generate_courses()
    round_in_list = generate_round_in(courses_list)
    round_out_list = calculate_round_outs(round_in_list)
    return round_out_list

courses_list = generate_courses()
my_rounds = generate_mockups()