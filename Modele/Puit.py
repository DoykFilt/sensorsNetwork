from Modele.Noeud import Noeud
from Modele.Roles import Roles


class Puit(Noeud):
    def __init__(self, _pos):
        super().__init__(_pos, Roles._PUIT)
