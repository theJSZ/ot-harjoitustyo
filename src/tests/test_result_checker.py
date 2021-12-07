import unittest
from entities.result_checker import ResultChecker
from entities.die import Die

class TestResultChecker(unittest.TestCase):
    def setUp(self):
        self.result_checker = ResultChecker()
        self.dice = [Die() for _ in range(5)]

    def test_check_upstairs(self):
        for die in self.dice:
            die.set_face(2)
        self.assertEqual(self.result_checker.check_upstairs(2, self.dice), 10)
        self.assertEqual(self.result_checker.check_upstairs(3, self.dice), 0)

        for die in self.dice:
            die.set_face(4)
        self.assertEqual(self.result_checker.check_upstairs(2, self.dice), 0)
        self.assertEqual(self.result_checker.check_upstairs(4, self.dice), 20)

    def test_check_downstairs(self):
        self.dice[0].set_face(1)
        self.dice[1].set_face(2)
        self.dice[2].set_face(3)
        self.dice[3].set_face(4)
        self.dice[4].set_face(5)

        self.assertEqual(self.result_checker.check_pair(self.dice), 0)
        self.assertEqual(self.result_checker.check_two_pair(self.dice), 0)
        self.assertEqual(self.result_checker.check_three_kind(self.dice), 0)
        self.assertEqual(self.result_checker.check_four_kind(self.dice), 0)
        self.assertEqual(self.result_checker.check_small_straight(self.dice), 15)
        self.assertEqual(self.result_checker.check_large_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_full_house(self.dice), 0)
        self.assertEqual(self.result_checker.check_chance(self.dice), 15)
        self.assertEqual(self.result_checker.check_yatzy(self.dice), 0)

        self.dice[0].set_face(1)
        self.dice[1].set_face(1)
        self.dice[2].set_face(3)
        self.dice[3].set_face(3)
        self.dice[4].set_face(5)

        self.assertEqual(self.result_checker.check_pair(self.dice), 6)
        self.assertEqual(self.result_checker.check_two_pair(self.dice), 8)
        self.assertEqual(self.result_checker.check_three_kind(self.dice), 0)
        self.assertEqual(self.result_checker.check_four_kind(self.dice), 0)
        self.assertEqual(self.result_checker.check_small_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_large_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_full_house(self.dice), 0)
        self.assertEqual(self.result_checker.check_chance(self.dice), 13)
        self.assertEqual(self.result_checker.check_yatzy(self.dice), 0)

        self.dice[0].set_face(1)
        self.dice[1].set_face(1)
        self.dice[2].set_face(1)
        self.dice[3].set_face(5)
        self.dice[4].set_face(5)

        self.assertEqual(self.result_checker.check_pair(self.dice), 10)
        self.assertEqual(self.result_checker.check_two_pair(self.dice), 12)
        self.assertEqual(self.result_checker.check_three_kind(self.dice), 3)
        self.assertEqual(self.result_checker.check_four_kind(self.dice), 0)
        self.assertEqual(self.result_checker.check_small_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_large_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_full_house(self.dice), 13)
        self.assertEqual(self.result_checker.check_chance(self.dice), 13)
        self.assertEqual(self.result_checker.check_yatzy(self.dice), 0)

        self.dice[0].set_face(2)
        self.dice[1].set_face(2)
        self.dice[2].set_face(2)
        self.dice[3].set_face(2)
        self.dice[4].set_face(5)

        self.assertEqual(self.result_checker.check_pair(self.dice), 4)
        self.assertEqual(self.result_checker.check_two_pair(self.dice), 0)
        self.assertEqual(self.result_checker.check_three_kind(self.dice), 6)
        self.assertEqual(self.result_checker.check_four_kind(self.dice), 8)
        self.assertEqual(self.result_checker.check_small_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_large_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_full_house(self.dice), 0)
        self.assertEqual(self.result_checker.check_chance(self.dice), 13)
        self.assertEqual(self.result_checker.check_yatzy(self.dice), 0)

        self.dice[0].set_face(6)
        self.dice[1].set_face(2)
        self.dice[2].set_face(3)
        self.dice[3].set_face(4)
        self.dice[4].set_face(5)

        self.assertEqual(self.result_checker.check_pair(self.dice), 0)
        self.assertEqual(self.result_checker.check_two_pair(self.dice), 0)
        self.assertEqual(self.result_checker.check_three_kind(self.dice), 0)
        self.assertEqual(self.result_checker.check_four_kind(self.dice), 0)
        self.assertEqual(self.result_checker.check_small_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_large_straight(self.dice), 20)
        self.assertEqual(self.result_checker.check_full_house(self.dice), 0)
        self.assertEqual(self.result_checker.check_chance(self.dice), 20)
        self.assertEqual(self.result_checker.check_yatzy(self.dice), 0)

        self.dice[0].set_face(5)
        self.dice[1].set_face(5)
        self.dice[2].set_face(5)
        self.dice[3].set_face(5)
        self.dice[4].set_face(5)

        self.assertEqual(self.result_checker.check_pair(self.dice), 10)
        self.assertEqual(self.result_checker.check_two_pair(self.dice), 0)
        self.assertEqual(self.result_checker.check_three_kind(self.dice), 15)
        self.assertEqual(self.result_checker.check_four_kind(self.dice), 20)
        self.assertEqual(self.result_checker.check_small_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_large_straight(self.dice), 0)
        self.assertEqual(self.result_checker.check_full_house(self.dice), 0)
        self.assertEqual(self.result_checker.check_chance(self.dice), 25)
        self.assertEqual(self.result_checker.check_yatzy(self.dice), 50)


