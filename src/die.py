from random import randint

class Die:
    def __init__(self):
        self._face = 1
        self._frozen = False
        self.throw()
        self._y = 0
        self._x = 0

    def setPosition(self, pos: tuple):
        self._y = pos[0]
        self._x = pos[1]

    def getPosition(self):
        return (self._y, self._x)

    def getFace(self):
        return self._face

    def throw(self):
        if not self._frozen:
            self._face = randint(1,6)

    def changeFreezeState(self):
        self._frozen = not self._frozen