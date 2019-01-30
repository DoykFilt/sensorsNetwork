

class Noeud:
    def __init__(self, _pos):
        self.pos = _pos

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, _pos):
        self.__pos = _pos