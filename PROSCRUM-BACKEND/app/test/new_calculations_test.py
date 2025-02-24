import unittest
from app.models import CourseWithID, RoundOut, HoleConfig
from new_calculations import calculate_whs_handicap, convert_to_GBE_score, convert_to_GBE_score_first_round, get_SD_9_holes_for_HCPI


class new_calculations_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Definition der Modelle

        # Definition der Golfplätze
        course_1 = CourseWithID(
            course_id=1,
            course_name="Sunny Hills Golf Course",
            course_par=72,
            course_rating=70.9,
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

        # Runde 1
        round_1 = RoundOut(
            round_id=1,
            course=course_1,
            round_number=1,
            scores=[5, 6, 8, 7, 6, 6, 6, 6, 6, 7, 6, 6, 5, 6, 6, 6, 5, 6]
        )

        # Runde 2
        round_2 = RoundOut(
            round_id=2,
            course=course_1,
            round_number=2,
            scores=[4, 5, 5, 6, 6, 5, 6, 9, 5, 5, 6, 6, 5, 6, 6, 6, 5, 6]
        )

        # Runde 3
        course_3 = CourseWithID(
            course_id=2,
            course_name="Green Valley Golf Course",
            course_par=72,
            course_rating=72.3,
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

        round_3 = RoundOut(
            round_id=3,
            course=course_3,
            round_number=3,
            scores=[4, 5, 5, 6, 6, 7, 4, 8, 4, 5, 6, 6, 5, 6, 6, 6, 5, 6]
        )

        # Runde 4 (Verwendet das gleiche Course-Objekt wie für Runde 3)
        round_4 = RoundOut(
            round_id=4,
            course=course_3,
            round_number=4,
            scores=[5, 6, 6, 7, 6, 6, 4, 7, 6, 7, 6, 6, 5, 5, 6, 6, 5, 6]
        )

        # Runde 5
        round_5 = RoundOut(
            round_id=5,
            course=course_1,
            round_number=5,
            scores=[4, 5, 5, 6, 5, 5, 4, 5, 5, 6, 5, 5, 4, 5, 5, 6, 5, 5]
        )

        # Runde 6 (9 Löcher von Course 1)
        course_6 = CourseWithID(
            course_id=3,
            course_name="Cedar Ridge Golf Course",
            course_par=35,
            course_rating=34.1,
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

        round_6 = RoundOut(
            round_id=6,
            course=course_6,
            round_number=6,
            scores=[5, 6, 6, 7, 6, 5, 5, 6, 6]
        )

        # Runde 7 (Verwendet das gleiche Course-Objekt wie für Runde 6)
        round_7 = RoundOut(
            round_id=7,
            course=course_6,
            round_number=7,
            scores=[5, 7, 9, 7, 6, 6, 6, 6, 6]
        )

        # Runde 8 (Verwendet das gleiche Course-Objekt wie für Runde 1 und 5)
        round_8 = RoundOut(
            round_id=8,
            
            course=course_1,
            round_number=8,
            scores=[4, 5, 5, 6, 6, 5, 4, 5, 5, 7, 5, 5, 4, 5, 5, 7, 5, 5]
        )

        # Runde 9 (Verwendet das gleiche Course-Objekt wie für Runde 3 und 4) glaube falsch
        round_9 = RoundOut(
            round_id=9,
            course=course_3,
            round_number=9,
            scores=[4, 5, 5, 6, 5, 5, 4, 5, 5, 6, 5, 5, 4, 5, 5, 6, 5, 5]
        )

        # Runde 10 irgendwie course 1
        course_10 = CourseWithID(
            course_id=4,
            course_name="Sunny Hills Golf Course",
            course_par=35,
            course_rating=35.7,
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

        round_10 = RoundOut(
            round_id=10,
            course=course_10,
            round_number=10,
            scores=[4, 5, 5, 6, 5, 5, 4, 5, 5],
        )

        # Runde 11 (Verwendet das gleiche Course-Objekt wie für Runde 10)
        round_11 = RoundOut(
            round_id=11,
            course=course_10,
            round_number=11,
            scores=[5, 6, 6, 7, 6, 6, 5, 6, 6],
        )

        # Runde 12 (Verwendet das gleiche Course-Objekt wie für Runde 3, 4, 9 und 10)
        round_12 = RoundOut(
            round_id=12,
            course=course_3,
            round_number=12,
            scores=[6, 7, 7, 8, 7, 7, 6, 7, 10, 8, 7, 7, 6, 7, 7, 8, 7, 7],
        )

        # Liste aller Runden
        cls.rounds = [
            round_1, round_2, round_3, round_4, round_5,
            round_6, round_7, round_8, round_9, round_10,
            round_11, round_12
        ]

        cls.course = course_1
        cls.handicap_results = [35.4, 27.6, 24.1, 23.1, 18.8, 20.45, 20.45, 20.25, 18.633333, 18.63333, 18.63333, 19.4]
        cls.score_difs = [37.4, 29.6, 24.1, 28.4, 18.8, 31.1, 36, 21.7, 15.4, 21.7, 28.6, 46.7]

    def test_convert_to_GBE_score(self):
        test_scores = [4, 5, 5, 6, 6, 5, 6, 9, 5, 5, 6, 6, 5, 6, 6, 6, 5, 6]
        result = 101

        self.assertEqual(convert_to_GBE_score(test_scores, course=self.course), result)

    def test_convert_to_GBE_score_first_round(self):
        test_scores = [5, 6, 8, 7, 6, 6, 6, 6, 6, 7, 6, 6, 5, 6, 6, 6, 5, 6]
        result = 108

        self.assertEqual(convert_to_GBE_score_first_round(test_scores, course = self.course), result)
    

    def test_calculate_whs_handicap(self):
        for n, round in enumerate(self.rounds):
            with self.subTest(n=n):
                if n >= 1:
                    HCPI = self.rounds[n - 1].calc_result_2021
                else:
                    HCPI = 54
                sliced_list = self.rounds[:n]
                sD = []
                for round in sliced_list:
                    sD.append(round.score_differential)

                exp_result = self.handicap_results[n]
                calc_result = calculate_whs_handicap(round, sD, HCPI)
                self.assertEqual(calc_result, exp_result, f"Handicap calculator failed for {n} rounds. calculated result was {calc_result}, but should be {exp_result}")

    def test_get_SD_for_9_holes(self):
        test_values = [-6.0, 4.0, 30.1]
        test_result = [-1.92, 3.28, 16.8]

        for value, result in test_values, test_result:
            self.assertEqual(get_SD_9_holes_for_HCPI(value), result, f"test failed for value {value} with expected result {result}, but was {get_SD_9_holes_for_HCPI(value)}")

if __name__ == "__main__":
    unittest.main()
