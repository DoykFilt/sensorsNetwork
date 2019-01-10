from Modele.Noeud import Noeud


class Capteur(Noeud):
    def __init__(self, _pos, _vie_batterie):
        super().__init__(_pos)
        self.N_vie_batterie = _vie_batterie

    @property
    def N_vie_batterie(self):
        return self.__N_vie_batterie

    @N_vie_batterie.setter
    def N_vie_batterie(self, _vie_vatterie):
        self.__N_vie_batterie = _vie_vatterie
