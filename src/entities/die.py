from random import randint

class Die:
    def __init__(self, face: int = None):
        """Alustaa nopan annettuun arvoon tai satunnaiseen arvoon jos ei annettu

        Args:
            face (int, optional): haluttu arvo. Default: None.
        """
        self._frozen = False
        self._y = 0
        self._x = 0
        if face is None:
            self.throw()
        else:
            self.face = face

    def set_position(self, pos: tuple):
        """Määrittää nopan sijainnin käyttöliittymässä

        Args:
            pos (tuple): koordinaatit (y, x)
        """
        self._y = pos[0]
        self._x = pos[1]

    def get_position(self):
        """Palauttaa nopan sijainnin käyttöliittymässä

        Returns:
            tuple: koordinaatit (y, x)
        """
        return (self._y, self._x)

    def in_area(self, mouse_pos: tuple):
        """Tarkistaa onko hiiren osoitin nopan alueella

        Args:
            mouse_pos (tuple): osoittimen koordinaatit (y, x)

        Returns:
            True / False
        """
        return (self._x < mouse_pos[1] < self._x + 65) and (self._y < mouse_pos[0] < self._y + 65)

    # def get_face(self):
    #     """Palauttaa nopan arvon

    #     Returns:
    #         int: arvo
    #     """
    #     return self._face

    # def set_face(self, number: int):
    #     """Asettaa nopan haluttuun arvoon

    #     Args:
    #         number (int): haluttu arvo
    #     """
    #     self._face = number

    def throw(self):
        """Jos noppa ei jäädytetty, arpoo uuden arvon
        """
        if not self._frozen:
            self.face = randint(1, 6)

    def change_freeze_state(self):
        """Muuttaa nopan jäädytys-statuksen päinvastaiseksi
        """
        self._frozen = not self._frozen

    def get_freeze_state(self):
        """Palauttaa nopan jäädytys-statuksen

        Returns:
            True / False
        """
        return self._frozen

    def __gt__(self, other):
        """Tarkistaa onko nopan arvo isompi kuin toisella nopalla,
        tarvitaan noppien järjestämiseen

        Args:
            other (Die): toinen noppa

        Returns:
            True / False
        """
        return self.face > other.face

    def __eq__(self, other):
        """Tarkistaa onko nopan arvo sama kuin toisella nopalla,
        tarvitaan jossain tulosten toteamisessa

        Args:
            other (Die): toinen noppa

        Returns:
            True / False
        """
        return self.face == other.face
