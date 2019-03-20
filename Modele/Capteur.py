"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Capteur

    Possède la classe Capteur qui modélise le capteur d'un graphe
"""


from Modele.Noeud import Noeud


class Capteur(Noeud):
    """
        class Capteur

        Modélise le capteur d'un graphe, hérite de la classe Noeud

        :var self.C_vie_batterie : int
    """

    def __init__(self, _pos, _vie_batterie, _role, _route):
        """
            Constructeur de la classe

            :param _pos : tuple de float, les positions sur les composantes x et y du capteur
            :param _vie_batterie : float, vie batterie
            :param _role : Enum Roles, le rôle du capteur
            :param _route : int, le noeud vers lequel envoyer les données
        """

        super().__init__(_pos, _role, _route)
        self.C_vie_batterie = _vie_batterie
