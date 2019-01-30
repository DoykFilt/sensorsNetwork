from Modele.Noeud import Noeud


class Capteur(Noeud):
    def __init__(self, _pos, _vie_batterie, _role):
        super().__init__(_pos, _role)
        self.C_vie_batterie = _vie_batterie

