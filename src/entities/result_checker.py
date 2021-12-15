class ResultChecker:

    def get_functions():
        return [ResultChecker.check_pair,
                ResultChecker.check_two_pair,
                ResultChecker.check_three_kind,
                ResultChecker.check_four_kind,
                ResultChecker.check_small_straight,
                ResultChecker.check_large_straight,
                ResultChecker.check_full_house,
                ResultChecker.check_chance,
                ResultChecker.check_yatzy]

    def check_upstairs(self, target: int, dice: list):
        total = 0

        for die in dice:
            if die.get_face() == target:
                total += target
        return total

    def check_pair(self, dice: list):
        faces = [0 for _ in range(7)]

        for die in dice:
            faces[die.get_face()] += 1
        for face in range(6, 0, -1):
            if faces[face] >= 2:
                return 2*face
        return 0

    def check_two_pair(self, dice: list):
        faces = [0 for _ in range(7)]
        total = 0
        for die in dice:
            faces[die.get_face()] += 1

        pairs = set()
        for face in range(6, 0, -1):
            if faces[face] >= 2:
                pairs.add(face)
        if len(pairs) < 2:
            return 0

        total = 0
        total += max(pairs)*2
        pairs.remove(max(pairs))
        total += max(pairs)*2
        return total

    def check_three_kind(self, dice: list):
        faces = [0 for _ in range(7)]
        total = 0

        for die in dice:
            faces[die.get_face()] += 1
            if faces[die.get_face()] == 3:
                total = 3*die.get_face()

        return total

    def check_four_kind(self, dice: list):
        faces = [0 for _ in range(7)]

        for die in dice:
            faces[die.get_face()] += 1
            if faces[die.get_face()] == 4:
                return 4*die.get_face()

        return 0

    def check_small_straight(self, dice: list):
        faces = []
        for die in dice:
            faces.append(die.get_face())
        if sorted(faces) == [1, 2, 3, 4, 5]:
            return 15

        return 0

    def check_large_straight(self, dice: list):
        faces = []
        for die in dice:
            faces.append(die.get_face())
        if sorted(faces) == [2, 3, 4, 5, 6]:
            return 20

        return 0

    def check_full_house(self, dice: list):
        faces_count = [0 for _ in range(7)]
        total = 0
        for die in dice:
            faces_count[die.get_face()] += 1

        if 2 in faces_count and 3 in faces_count:
            for die in dice:
                total += die.get_face()
            return total

        return 0

    def check_chance(self, dice: list):
        total = 0
        for die in dice:
            total += die.get_face()
        return total

    def check_yatzy(self, dice: list):
        if sorted(dice)[0] == sorted(dice)[4]:
            return 50

        return 0
