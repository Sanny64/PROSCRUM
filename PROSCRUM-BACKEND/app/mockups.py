from app.models import HoleConfig, CourseWithID

def generate_courses():
    courses_list = []
    
    course_1 = CourseWithID(
    course_id=1,
    course_name="Sunny Hills Golf Course",
    course_par=72,
    course_rating_9=None,
    course_rating_18=70.9,
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
    course_par=68,
    course_rating_9=None,
    course_rating_18=72.3,
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
    
    course_3 = CourseWithID(
    course_id=3,
    course_name="Cedar Ridge Golf Course",
    course_par=35,
    course_rating_9=34.1,
    course_rating_18=None,
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
        HoleConfig(hole=9, par=4, hdc=2)
    ]
    )
    courses_list.append(course_3)
    
    course_4 = CourseWithID(
    course_id=4,
    course_name="Sunny Hills Golf Course",
    course_par=35,
    course_rating_9=35.7,
    course_rating_18=None,
    slope_rating=130,
    holes=[
        HoleConfig(hole=1, par=3, hdc=4),
        HoleConfig(hole=2, par=4, hdc=16),
        HoleConfig(hole=3, par=4, hdc=1),
        HoleConfig(hole=4, par=5, hdc=10),
        HoleConfig(hole=5, par=4, hdc=7),
        HoleConfig(hole=6, par=4, hdc=13),
        HoleConfig(hole=7, par=3, hdc=5),
        HoleConfig(hole=8, par=4, hdc=17),
        HoleConfig(hole=9, par=4, hdc=2)
    ]
    )
    courses_list.append(course_4)
    
    return courses_list


def generate_mockups():
    courses_list = generate_courses()

    return courses_list