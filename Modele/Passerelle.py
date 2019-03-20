"""@package docstring
    Auteur : Beaufils Thibaud
    V 1.0
    PRD 20/03/2019

    Module Passerelle

    Possède la classe Passerelle qui modélise une passerelle (ou puit) d'un réseau
"""


from Modele.Noeud import Noeud
from Modele.Roles import Roles


class Passerelle(Noeud):
    """
        class Passerelle

        Modélise une passerelle (ou puit) d'un réseau

    """
    def __init__(self, _pos):
        """
            Constructeur de la classe

            :param _pos : tuple de float (x, y)

        """
        super().__init__(_pos, Roles.PUIT, -1)

