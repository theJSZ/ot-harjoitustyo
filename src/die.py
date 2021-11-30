from random import randint

class Die:
    def __init__(self, face = None):
        self._frozen = False
        self._y = 0
        self._x = 0
        if face == None:
            self.throw()
        else:
            self._face = face

    def set_position(self, pos: tuple):
        self._y = pos[0]
        self._x = pos[1]

    def get_position(self):
        return (self._y, self._x)

    def get_face(self):
        return self._face

    def set_face(self, number):
        self._face = number

    def throw(self):
        if not self._frozen:
            self._face = randint(1,6)

    def change_freeze_state(self):
        self._frozen = not self._frozen

    def __gt__(self, other):
        return self.get_face() > other.get_face()

    def __eq__(self, other):
        return self.get_face() == other.get_face()
