class ResultChecker:
    """Luokka tulosten tarkistamiselle
    """

    def get_functions():
        """Palauttaa tarkistajafunktiot listana

        Returns:
            [list]: lista käytettävissä olevista funktioista
        """
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
        """Tarkistaa "yläkerran", ts. ruudut "Ykköset ... Kuutoset"

        Args:
            target (int): Tarkistettava ruutu 1..6
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: Nopista saatava tulos haluttuun ruutuun
        """
        total = 0

        for die in dice:
            if die.face == target:
                total += target
        return total

    def check_pair(self, dice: list):
        """Tarkistaa parin

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: Suurin mahdollinen pari annetuista nopista
        """
        faces = [0 for _ in range(7)]

        for die in dice:
            faces[die.face] += 1
        for face in range(6, 0, -1):
            if faces[face] >= 2:
                return 2*face
        return 0

    def check_two_pair(self, dice: list):
        """Tarkistaa 2 paria

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: 2 parin summa jos 2 paria, muuten 0
        """
        faces = [0 for _ in range(7)]
        total = 0
        for die in dice:
            faces[die.face] += 1

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
        """Tarkistaa 3 samaa kutsuen check_n_kind

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: Kolmen saman summa jos 3 samaa, 0 muuten
        """

        return self.check_n_kind(dice, 3)

    def check_four_kind(self, dice: list):
        """Tarkistaa 4 samaa kutsuen check_n_kind

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: Neljän saman summa jos 4 samaa, muuten 0
        """

        return self.check_n_kind(dice, 4)

    def check_n_kind(self, dice: list, n_to_find: int):
        """Tarkistaa n samaa

        Args:
            dice (list): Käytössä olevat nopat
            n (int): Tarkistettava samojen määrä

        Returns:
            int: saatu tulos
        """
        faces = [0 for _ in range(7)]

        for die in dice:
            faces[die.face] += 1
            if faces[die.face] == n_to_find:
                return n_to_find*die.face

        return 0

    def check_small_straight(self, dice: list):
        """Tarkistaa pienen suoran

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: 15 jos pieni suora, 0 muuten
        """
        faces = []
        for die in dice:
            faces.append(die.face)
        if sorted(faces) == [1, 2, 3, 4, 5]:
            return 15

        return 0

    def check_large_straight(self, dice: list):
        """Tarkistaa suuren suoran

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: 20 jos suuri suora, 0 muuten
        """
        faces = []
        for die in dice:
            faces.append(die.face)
        if sorted(faces) == [2, 3, 4, 5, 6]:
            return 20

        return 0

    def check_full_house(self, dice: list):
        """Tarkistaa täyskäden

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: Nopista muodostuva täyskäsi, muuten 0
        """
        faces_count = [0 for _ in range(7)]
        total = 0
        for die in dice:
            faces_count[die.face] += 1

        if 2 in faces_count and 3 in faces_count:
            for die in dice:
                total += die.face
            return total

        return 0

    def check_chance(self, dice: list):
        """Tarkistaa sattuman

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: Kaikkien noppien summa
        """
        total = 0
        for die in dice:
            total += die.face
        return total

    def check_yatzy(self, dice: list):
        """Tarkistaa yatzyn

        Args:
            dice (list): Käytössä olevat nopat

        Returns:
            [int]: 50 jos yatzy, 0 muuten
        """
        if sorted(dice)[0] == sorted(dice)[4]:
            return 50

        return 0
